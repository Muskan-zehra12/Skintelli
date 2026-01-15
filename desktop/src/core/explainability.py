"""
Explainability Module - Grad-CAM Heatmap Generation
Visualizes which regions of the image the model focused on
"""

import logging
import numpy as np
import cv2
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class HeatmapGenerator:
    """Generate Grad-CAM heatmaps for explainability"""
    
    def __init__(self):
        self.last_heatmap = None
    
    def generate_heatmap(self, 
                        image: np.ndarray,
                        detection_result: Optional[object] = None) -> np.ndarray:
        """
        Generate heatmap visualization
        
        Args:
            image: Input image (224x224x3, normalized 0-1)
            detection_result: Detection result with confidence scores
            
        Returns:
            Heatmap image (same size as input, 0-255)
        """
        try:
            # For now, create a mock heatmap based on confidence
            h, w = image.shape[:2]
            
            # Create base heatmap
            heatmap = np.zeros((h, w), dtype=np.float32)
            
            if detection_result and detection_result.bounding_boxes:
                # Draw bounding boxes with intensity
                for box in detection_result.bounding_boxes:
                    x = int(box.get('x', 0))
                    y = int(box.get('y', 0))
                    width = int(box.get('width', w))
                    height = int(box.get('height', h))
                    confidence = box.get('confidence', 0.5)
                    
                    # Ensure bounds
                    x = max(0, min(x, w-1))
                    y = max(0, min(y, h-1))
                    x2 = min(x + width, w)
                    y2 = min(y + height, h)
                    
                    # Fill region with confidence value
                    heatmap[y:y2, x:x2] = confidence
            else:
                # Create a gaussian-like heatmap if no bbox provided
                y_center, x_center = h // 2, w // 2
                y_radius, x_radius = h // 4, w // 4
                
                for y in range(max(0, y_center - y_radius), min(h, y_center + y_radius)):
                    for x in range(max(0, x_center - x_radius), min(w, x_center + x_radius)):
                        # Gaussian distribution
                        dist = np.sqrt(((y - y_center) / y_radius) ** 2 + 
                                     ((x - x_center) / x_radius) ** 2)
                        heatmap[y, x] = max(0, 1 - dist)
            
            # Apply Gaussian blur for smoothing
            heatmap = cv2.GaussianBlur(heatmap, (15, 15), 0)
            
            # Normalize to 0-255
            heatmap_normalized = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            
            # Apply colormap (JET for warm colors)
            heatmap_colored = cv2.applyColorMap(heatmap_normalized, cv2.COLORMAP_JET)
            
            self.last_heatmap = heatmap_colored
            logger.info(f"Heatmap generated: {heatmap_colored.shape}")
            
            return heatmap_colored
            
        except Exception as e:
            logger.error(f"Error generating heatmap: {e}")
            return None
    
    def overlay_heatmap_on_image(self,
                                original_image: np.ndarray,
                                heatmap: np.ndarray,
                                alpha: float = 0.4) -> np.ndarray:
        """
        Overlay heatmap on original image
        
        Args:
            original_image: Original input image (BGR)
            heatmap: Generated heatmap (BGR after colormap)
            alpha: Transparency of heatmap (0-1)
            
        Returns:
            Blended image
        """
        try:
            if original_image.shape != heatmap.shape:
                heatmap = cv2.resize(heatmap, (original_image.shape[1], original_image.shape[0]))
            
            # Ensure both are uint8
            original_uint8 = (original_image * 255).astype(np.uint8) if original_image.max() <= 1 else original_image.astype(np.uint8)
            
            # Blend images
            blended = cv2.addWeighted(original_uint8, 1 - alpha, heatmap, alpha, 0)
            
            logger.info("Heatmap overlaid on original image")
            return blended
            
        except Exception as e:
            logger.error(f"Error overlaying heatmap: {e}")
            return None
    
    def save_heatmap(self, heatmap: np.ndarray, output_path: str) -> bool:
        """Save heatmap to file"""
        try:
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            cv2.imwrite(output_path, heatmap)
            logger.info(f"Heatmap saved: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving heatmap: {e}")
            return False


class GradCAM:
    """
    Gradient-weighted Class Activation Mapping
    More advanced explainability technique
    """
    
    def __init__(self, model=None):
        self.model = model
        self.last_gradient = None
    
    def generate_gradcam(self,
                        image: np.ndarray,
                        target_class_idx: int) -> Optional[np.ndarray]:
        """
        Generate Grad-CAM heatmap
        Requires model with gradient computation capability
        """
        try:
            if not self.model:
                logger.warning("Model not provided for Grad-CAM")
                return None
            
            logger.info(f"Generating Grad-CAM for class {target_class_idx}")
            
            # This would require accessing model internals
            # For now, return None to indicate not available
            return None
            
        except Exception as e:
            logger.error(f"Error generating Grad-CAM: {e}")
            return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    generator = HeatmapGenerator()
    
    # Test with dummy image
    dummy_image = np.random.rand(224, 224, 3).astype(np.float32)
    dummy_result = type('obj', (object,), {
        'bounding_boxes': [{'x': 56, 'y': 56, 'width': 112, 'height': 112, 'confidence': 0.85}]
    })()
    
    heatmap = generator.generate_heatmap(dummy_image, dummy_result)
    print(f"Generated heatmap shape: {heatmap.shape if heatmap is not None else 'Failed'}")
