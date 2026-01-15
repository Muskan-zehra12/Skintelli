"""
Skin Disease/Infection Analyzer
Detects and marks areas of potential skin conditions in images.
"""
import cv2
import numpy as np
from typing import Tuple, Dict, List, Optional
from pathlib import Path

try:
    from tensorflow.keras.models import load_model
    import tensorflow as tf
except Exception:  # tensorflow not installed or import error
    load_model = None
    tf = None


class SkinAnalyzer:
    """Analyzes skin images for potential infections, injuries, or abnormalities."""
    
    def __init__(self, model_path: Optional[str] = None, class_names: Optional[List[str]] = None):
        self.confidence_threshold = 0.5
        self.model = None
        # Default labels (update if you have the exact set from training)
        self.class_names = class_names or [
            "Eczema / Dermatitis",
            "Psoriasis",
            "Acne / Folliculitis",
            "Fungal Infection",
            "Benign Lesion",
            "Malignant Lesion"
        ]
        # Auto-load model if available
        model_file = model_path or "src/models/final_model_best.keras"
        if load_model and tf and Path(model_file).exists():
            try:
                self.model = load_model(model_file)
            except Exception:
                self.model = None
        
    def analyze_image(self, image: np.ndarray) -> Dict:
        """
        Analyze skin image for abnormalities.
        
        Args:
            image: BGR image from OpenCV
            
        Returns:
            Dictionary containing:
            - heatmap: Visualization showing affected areas
            - diagnosis: Text description of findings
            - severity: Low/Medium/High
            - affected_percentage: Percentage of image affected
            - regions: List of detected issue regions
        """
        # Convert to RGB for processing
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detect abnormal regions
        abnormal_mask, severity_map = self._detect_abnormalities(rgb_image)
        
        # Generate heatmap overlay
        heatmap = self._create_heatmap(image, severity_map)
        
        # Analyze findings (normalize mask to binary to avoid 0-255 inflation)
        affected_pixels = (abnormal_mask > 0).sum()
        affected_percentage = (affected_pixels / abnormal_mask.size) * 100
        mean_severity = severity_map[severity_map > 0].mean() if (severity_map > 0).any() else 0
        severity = self._calculate_severity(affected_percentage, severity_map)
        condition = self._infer_condition(severity)
        confidence = self._estimate_confidence(mean_severity, affected_percentage, severity)

        # If a trained model is available, use it for condition/confidence override
        if self.model is not None:
            model_condition, model_confidence = self._predict_model(rgb_image)
            if model_condition:
                condition = model_condition
            if model_confidence is not None:
                confidence = model_confidence

        diagnosis = self._generate_diagnosis(affected_percentage, severity, condition, confidence)
        regions = self._find_regions(abnormal_mask)
        
        return {
            'heatmap': heatmap,
            'diagnosis': diagnosis,
            'severity': severity,
            'condition': condition,
            'confidence': round(confidence * 100, 1),
            'top_conditions': getattr(self, "_last_top_conditions", []),
            'affected_percentage': round(affected_percentage, 2),
            'regions': regions,
            'has_issues': affected_percentage > 1.0
        }
    
    def _detect_abnormalities(self, rgb_image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect abnormal skin regions based on color, texture, and patterns.
        
        Returns:
            Tuple of (binary_mask, severity_map)
        """
        h, w = rgb_image.shape[:2]
        
        # Convert to different color spaces for analysis
        hsv = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)
        lab = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2LAB)
        
        # Initialize severity map (0-255, higher = more severe)
        severity_map = np.zeros((h, w), dtype=np.float32)
        
        # 1. Detect redness (inflammation, irritation, wounds)
        red_mask = self._detect_redness(rgb_image, hsv)
        severity_map += red_mask * 0.8
        
        # 2. Detect unusual darkness (bruising, necrosis, hyperpigmentation)
        dark_mask = self._detect_dark_spots(lab)
        severity_map += dark_mask * 0.6
        
        # 3. Detect unusual lightness (vitiligo, scars, depigmentation)
        light_mask = self._detect_light_spots(lab)
        severity_map += light_mask * 0.5
        
        # 4. Detect texture irregularities (rashes, rough patches)
        texture_mask = self._detect_texture_abnormalities(rgb_image)
        severity_map += texture_mask * 0.7
        
        # Normalize severity map
        if severity_map.max() > 0:
            severity_map = (severity_map / severity_map.max() * 255).astype(np.uint8)
        else:
            severity_map = severity_map.astype(np.uint8)
        
        # Create binary mask of abnormal regions
        _, binary_mask = cv2.threshold(severity_map, 30, 255, cv2.THRESH_BINARY)
        
        # Clean up mask with morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)
        binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, kernel)
        
        return binary_mask, severity_map
    
    def _detect_redness(self, rgb_image: np.ndarray, hsv: np.ndarray) -> np.ndarray:
        """Detect red areas indicating inflammation or wounds."""
        r, g, b = rgb_image[:, :, 0], rgb_image[:, :, 1], rgb_image[:, :, 2]
        
        # Red channel dominance
        red_dominance = np.zeros_like(r, dtype=np.float32)
        safe_sum = g.astype(np.float32) + b.astype(np.float32) + 1
        red_dominance = (r.astype(np.float32) - (g.astype(np.float32) + b.astype(np.float32)) / 2) / safe_sum
        red_dominance = np.clip(red_dominance * 255, 0, 255).astype(np.uint8)
        
        # HSV-based red detection (two ranges for red in HSV)
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        hsv_red = cv2.bitwise_or(mask1, mask2)
        
        # Combine both methods
        combined = cv2.bitwise_or(red_dominance, hsv_red)
        return combined
    
    def _detect_dark_spots(self, lab: np.ndarray) -> np.ndarray:
        """Detect unusually dark areas (bruising, hyperpigmentation)."""
        l_channel = lab[:, :, 0]
        
        # Find areas significantly darker than average
        mean_l = l_channel.mean()
        std_l = l_channel.std()
        threshold = max(mean_l - 1.5 * std_l, 0)
        
        dark_mask = (l_channel < threshold).astype(np.uint8) * 255
        return dark_mask
    
    def _detect_light_spots(self, lab: np.ndarray) -> np.ndarray:
        """Detect unusually light areas (scars, depigmentation)."""
        l_channel = lab[:, :, 0]
        
        # Find areas significantly lighter than average
        mean_l = l_channel.mean()
        std_l = l_channel.std()
        threshold = min(mean_l + 1.5 * std_l, 255)
        
        light_mask = (l_channel > threshold).astype(np.uint8) * 255
        return light_mask
    
    def _detect_texture_abnormalities(self, rgb_image: np.ndarray) -> np.ndarray:
        """Detect texture irregularities using edge detection and variance."""
        gray = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)
        
        # Calculate local variance (texture roughness)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        variance = cv2.Laplacian(blur, cv2.CV_64F)
        variance = np.abs(variance)
        
        # Normalize
        if variance.max() > 0:
            variance = (variance / variance.max() * 255).astype(np.uint8)
        else:
            variance = variance.astype(np.uint8)
        
        # Threshold high-variance areas
        mean_var = variance.mean()
        std_var = variance.std()
        _, texture_mask = cv2.threshold(variance, int(mean_var + std_var), 255, cv2.THRESH_BINARY)
        
        return texture_mask
    
    def _create_heatmap(self, original_image: np.ndarray, severity_map: np.ndarray) -> np.ndarray:
        """Create heatmap overlay showing affected areas."""
        # Apply colormap to severity map (red = severe, yellow = moderate, green = mild)
        heatmap_colored = cv2.applyColorMap(severity_map, cv2.COLORMAP_JET)
        
        # Blend with original image
        alpha = 0.5
        overlay = cv2.addWeighted(original_image, 1 - alpha, heatmap_colored, alpha, 0)
        
        # Draw contours around detected regions
        _, binary = cv2.threshold(severity_map, 30, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(overlay, contours, -1, (0, 255, 0), 2)
        
        return overlay
    
    def _calculate_severity(self, affected_percentage: float, severity_map: np.ndarray) -> str:
        """Calculate overall severity level."""
        if affected_percentage < 1.0:
            return "None"
        elif affected_percentage < 5.0:
            avg_severity = severity_map[severity_map > 0].mean() if (severity_map > 0).any() else 0
            if avg_severity < 100:
                return "Low"
            else:
                return "Medium"
        elif affected_percentage < 15.0:
            return "Medium"
        else:
            return "High"

    def _infer_condition(self, severity: str) -> str:
        """Map severity to a human-readable condition guess."""
        if severity == "None":
            return "No significant abnormality"
        if severity == "Low":
            return "Mild irritation / dermatitis"
        if severity == "Medium":
            return "Moderate dermatitis / rash"
        return "Severe inflammation / possible infection"

    def _estimate_confidence(self, mean_severity: float, affected_percentage: float, severity: str) -> float:
        """Estimate confidence (0-1) from severity map strength and affected area."""
        # Normalize inputs
        sev_score = min(mean_severity / 255.0, 1.0)
        area_score = min(affected_percentage / 20.0, 1.0)
        base = (sev_score * 0.6) + (area_score * 0.4)
        # Slight bump for higher severity labels
        if severity == "High":
            base = min(base + 0.1, 1.0)
        elif severity == "Medium":
            base = min(base + 0.05, 1.0)
        elif severity == "None":
            base = max(base * 0.2, 0.05)
        return round(base, 3)

    def _predict_model(self, rgb_image: np.ndarray) -> Tuple[Optional[str], Optional[float]]:
        """Run the loaded Keras model and return (condition, confidence). Also stores top-5 list."""
        if self.model is None or tf is None:
            self._last_top_conditions = []
            return None, None
        try:
            img_resized = cv2.resize(rgb_image, (224, 224))
            img_norm = img_resized.astype("float32") / 255.0
            input_tensor = np.expand_dims(img_norm, axis=0)
            preds = self.model.predict(input_tensor)
            preds = np.array(preds)
            if preds.ndim == 2:
                probs = preds[0]
            elif preds.ndim == 1:
                probs = preds
            else:
                probs = preds.reshape(-1)

            # Softmax if needed
            if probs.max() > 1.0:
                probs = tf.nn.softmax(probs).numpy() if tf is not None else probs
            # Top-5 sorting
            top_indices = np.argsort(probs)[::-1][:5] if probs.size else []
            top_list = []
            for idx in top_indices:
                name = self.class_names[idx] if idx < len(self.class_names) else f"Class {idx}"
                top_list.append((name, float(probs[idx]) * 100.0))
            self._last_top_conditions = top_list

            top_idx = int(top_indices[0]) if len(top_indices) > 0 else 0
            conf = float(probs[top_idx]) if probs.size else 0.0

            if self.class_names and top_idx < len(self.class_names):
                condition = self.class_names[top_idx]
            else:
                condition = f"Class {top_idx}"
            return condition, conf
        except Exception:
            self._last_top_conditions = []
            return None, None
    
    def _generate_diagnosis(self, affected_percentage: float, severity: str, condition: str, confidence: float) -> str:
        """Generate human-readable diagnosis with condition and confidence."""
        confidence_pct = confidence * 100
        if severity == "None":
            return (
                f"Condition: {condition} (Confidence: {confidence_pct:.1f}%)\n"
                "✓ No significant skin abnormalities detected. Skin appears healthy."
            )
        
        diagnosis = (
            f"Condition: {condition} (Confidence: {confidence_pct:.1f}%)\n"
            f"⚠ Detected potential skin abnormalities in {affected_percentage:.1f}% of the examined area.\n\n"
        )
        
        if severity == "Low":
            diagnosis += "Severity: LOW\n"
            diagnosis += "Findings: Minor irregularities detected. May include:\n"
            diagnosis += "- Slight redness or irritation\n"
            diagnosis += "- Minor discoloration\n"
            diagnosis += "- Small blemishes or spots\n\n"
            diagnosis += "Recommendation: Monitor the area. Consult a dermatologist if symptoms persist or worsen."
        
        elif severity == "Medium":
            diagnosis += "Severity: MEDIUM\n"
            diagnosis += "Findings: Moderate abnormalities detected. May include:\n"
            diagnosis += "- Inflammation or redness\n"
            diagnosis += "- Texture irregularities\n"
            diagnosis += "- Visible lesions or rash\n"
            diagnosis += "- Color variations\n\n"
            diagnosis += "Recommendation: Medical evaluation recommended. Please consult a dermatologist."
        
        else:  # High
            diagnosis += "Severity: HIGH\n"
            diagnosis += "Findings: Significant abnormalities detected. May include:\n"
            diagnosis += "- Extensive inflammation\n"
            diagnosis += "- Large affected areas\n"
            diagnosis += "- Multiple concerning features\n\n"
            diagnosis += "Recommendation: URGENT - Seek immediate medical attention from a dermatologist."
        
        diagnosis += "\n\n⚕️ Note: This is an AI-assisted preliminary analysis. Always consult qualified healthcare professionals for proper diagnosis and treatment."
        
        return diagnosis
    
    def _find_regions(self, binary_mask: np.ndarray) -> List[Dict]:
        """Find and describe individual affected regions."""
        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        regions = []
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 100:  # Ignore very small regions
                x, y, w, h = cv2.boundingRect(contour)
                regions.append({
                    'id': i + 1,
                    'bbox': (x, y, w, h),
                    'area': area
                })
        
        return regions
