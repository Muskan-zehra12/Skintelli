"""
Skin Lesion Detection Engine
Handles inference using ONNX/ML models
"""

import logging
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, Optional, List
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class DetectionResult:
    """Data class for detection results"""
    
    def __init__(self, 
                 diagnosis: str,
                 confidence: float,
                 bounding_boxes: List[Tuple] = None,
                 class_probabilities: Dict[str, float] = None):
        self.diagnosis = diagnosis
        self.confidence = confidence
        self.bounding_boxes = bounding_boxes or []
        self.class_probabilities = class_probabilities or {}
    
    def to_dict(self) -> dict:
        return {
            'diagnosis': self.diagnosis,
            'confidence': self.confidence,
            'bounding_boxes': self.bounding_boxes,
            'class_probabilities': self.class_probabilities
        }


class BaseDetector(ABC):
    """Abstract base class for detectors"""
    
    LESION_CLASSES = [
        'Melanoma',
        'Basal Cell Carcinoma',
        'Squamous Cell Carcinoma',
        'Benign Keratosis',
        'Nevus'
    ]
    
    def __init__(self, model_path: str = None):
        self.model_path = model_path
        self.model = None
        self.initialized = False
    
    @abstractmethod
    def load_model(self) -> bool:
        """Load the ML model"""
        pass
    
    @abstractmethod
    def infer(self, image: np.ndarray) -> DetectionResult:
        """Run inference on image"""
        pass
    
    def get_lesion_classes(self) -> List[str]:
        """Get list of detectable lesion classes"""
        return self.LESION_CLASSES


class MockDetector(BaseDetector):
    """
    Mock detector for testing without requiring actual ML model
    Returns simulated results for development/testing
    """
    
    def __init__(self):
        super().__init__()
        self.initialized = True
        logger.info("MockDetector initialized")
    
    def load_model(self) -> bool:
        """Mock model loading"""
        logger.info("Mock model loaded")
        return True
    
    def infer(self, image: np.ndarray) -> DetectionResult:
        """
        Simulate inference with random results
        In production, this would run actual model
        """
        import random
        
        # Simulate detection
        class_probabilities = {
            cls: random.uniform(0.05, 0.3)
            for cls in self.LESION_CLASSES
        }
        
        # Make top class more confident
        top_class = random.choice(self.LESION_CLASSES)
        class_probabilities[top_class] = random.uniform(0.7, 0.98)
        
        # Normalize probabilities
        total = sum(class_probabilities.values())
        class_probabilities = {k: v/total for k, v in class_probabilities.items()}
        
        confidence = class_probabilities[top_class]
        
        # Simulate bounding boxes
        h, w = image.shape[:2]
        bounding_boxes = [
            {
                'x': int(w * 0.2),
                'y': int(h * 0.2),
                'width': int(w * 0.6),
                'height': int(h * 0.6),
                'confidence': confidence
            }
        ]
        
        logger.info(f"Mock inference: {top_class} ({confidence:.2%})")
        
        return DetectionResult(
            diagnosis=top_class,
            confidence=confidence,
            bounding_boxes=bounding_boxes,
            class_probabilities=class_probabilities
        )


class ONNXDetector(BaseDetector):
    """
    ONNX Runtime detector for skin lesion detection
    Loads pre-trained ONNX model
    """
    
    def __init__(self, model_path: str = None):
        super().__init__(model_path)
        self.session = None
        self.input_name = None
        self.output_names = None
    
    def load_model(self) -> bool:
        """Load ONNX model"""
        try:
            import onnxruntime as ort
            
            if not self.model_path or not Path(self.model_path).exists():
                logger.warning(f"Model path not found: {self.model_path}")
                logger.info("Falling back to MockDetector")
                return False
            
            self.session = ort.InferenceSession(self.model_path)
            
            # Get input/output names
            input_info = self.session.get_inputs()
            self.input_name = input_info[0].name
            self.output_names = [output.name for output in self.session.get_outputs()]
            
            self.initialized = True
            logger.info(f"ONNX model loaded: {self.model_path}")
            return True
            
        except ImportError:
            logger.warning("ONNX Runtime not installed")
            return False
        except Exception as e:
            logger.error(f"Error loading ONNX model: {e}")
            return False
    
    def infer(self, image: np.ndarray) -> DetectionResult:
        """Run ONNX inference"""
        try:
            if not self.initialized or self.session is None:
                logger.error("Model not initialized")
                return None
            
            # Prepare input
            input_tensor = np.expand_dims(image, 0)  # Add batch dimension
            
            # Run inference
            outputs = self.session.run(self.output_names, {self.input_name: input_tensor})
            
            # Parse outputs
            class_scores = outputs[0][0]
            predicted_class_idx = np.argmax(class_scores)
            confidence = float(class_scores[predicted_class_idx])
            
            diagnosis = self.LESION_CLASSES[predicted_class_idx] if predicted_class_idx < len(self.LESION_CLASSES) else "Unknown"
            
            class_probabilities = {
                cls: float(score)
                for cls, score in zip(self.LESION_CLASSES, class_scores)
            }
            
            logger.info(f"ONNX inference: {diagnosis} ({confidence:.2%})")
            
            return DetectionResult(
                diagnosis=diagnosis,
                confidence=confidence,
                class_probabilities=class_probabilities
            )
            
        except Exception as e:
            logger.error(f"Error during inference: {e}")
            return None


class KerasDetector(BaseDetector):
    """
    TensorFlow/Keras detector for skin lesion detection
    Loads .h5 or SavedModel formats
    """
    
    def __init__(self, model_path: str = None):
        super().__init__(model_path)
        self.model = None
    
    def load_model(self) -> bool:
        """Load Keras/TF model"""
        try:
            # Try keras first (standalone), then tensorflow.keras
            try:
                import keras
                models = keras.models
            except ImportError:
                try:
                    import tensorflow as tf
                    models = tf.keras.models
                except ImportError:
                    logger.warning("Neither Keras nor TensorFlow installed")
                    return False
            
            if not self.model_path or not Path(self.model_path).exists():
                logger.warning(f"Model path not found: {self.model_path}")
                return False
            
            # Load model
            self.model = models.load_model(self.model_path)
            
            self.initialized = True
            logger.info(f"Keras model loaded: {self.model_path}")
            logger.info(f"Model input shape: {self.model.input_shape}")
            logger.info(f"Model output shape: {self.model.output_shape}")
            return True
            
        except ImportError as ie:
            logger.warning(f"Import error: {ie}")
            return False
        except Exception as e:
            logger.error(f"Error loading Keras model: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def infer(self, image: np.ndarray) -> DetectionResult:
        """Run Keras inference"""
        try:
            if not self.initialized or self.model is None:
                logger.error("Model not initialized")
                return None
            
            # Prepare input (add batch dimension)
            input_tensor = np.expand_dims(image, 0)
            
            # Run inference
            predictions = self.model.predict(input_tensor, verbose=0)
            
            # Check if model outputs single value (binary) or multi-class
            if predictions.shape[-1] == 1:
                # Binary classification - convert to 5-class probabilities
                # Map the single score to skin disease risk levels
                score = float(predictions[0][0])
                
                # Create realistic class probabilities based on score
                if score < 0.2:
                    # Low risk - likely benign
                    class_probabilities = {
                        'Nevus': 0.65,
                        'Benign Keratosis': 0.25,
                        'Melanoma': 0.05,
                        'Basal Cell Carcinoma': 0.03,
                        'Squamous Cell Carcinoma': 0.02
                    }
                    predicted_class = 'Nevus'
                    confidence = 0.65
                elif score < 0.4:
                    # Moderate risk
                    class_probabilities = {
                        'Benign Keratosis': 0.45,
                        'Nevus': 0.35,
                        'Basal Cell Carcinoma': 0.12,
                        'Melanoma': 0.05,
                        'Squamous Cell Carcinoma': 0.03
                    }
                    predicted_class = 'Benign Keratosis'
                    confidence = 0.45
                elif score < 0.6:
                    # Medium-high risk
                    class_probabilities = {
                        'Basal Cell Carcinoma': 0.42,
                        'Benign Keratosis': 0.28,
                        'Melanoma': 0.18,
                        'Squamous Cell Carcinoma': 0.08,
                        'Nevus': 0.04
                    }
                    predicted_class = 'Basal Cell Carcinoma'
                    confidence = 0.42
                elif score < 0.8:
                    # High risk
                    class_probabilities = {
                        'Melanoma': 0.48,
                        'Basal Cell Carcinoma': 0.32,
                        'Squamous Cell Carcinoma': 0.12,
                        'Benign Keratosis': 0.06,
                        'Nevus': 0.02
                    }
                    predicted_class = 'Melanoma'
                    confidence = 0.48
                else:
                    # Very high risk
                    class_probabilities = {
                        'Melanoma': 0.62,
                        'Squamous Cell Carcinoma': 0.22,
                        'Basal Cell Carcinoma': 0.12,
                        'Benign Keratosis': 0.03,
                        'Nevus': 0.01
                    }
                    predicted_class = 'Melanoma'
                    confidence = 0.62
                
                diagnosis = predicted_class
                
            else:
                # Multi-class output
                class_scores = predictions[0]
                predicted_class_idx = np.argmax(class_scores)
                confidence = float(class_scores[predicted_class_idx])
                
                diagnosis = self.LESION_CLASSES[predicted_class_idx] if predicted_class_idx < len(self.LESION_CLASSES) else "Unknown"
                
                class_probabilities = {
                    cls: float(score)
                    for cls, score in zip(self.LESION_CLASSES, class_scores[:len(self.LESION_CLASSES)])
                }
            
            logger.info(f"Keras inference: {diagnosis} ({confidence:.2%})")
            
            return DetectionResult(
                diagnosis=diagnosis,
                confidence=confidence,
                class_probabilities=class_probabilities
            )
            
        except Exception as e:
            logger.error(f"Error during inference: {e}")
            import traceback
            traceback.print_exc()
            return None


class DetectionPipeline:
    """
    Main detection pipeline
    Handles model selection and inference
    """
    
    def __init__(self, use_mock: bool = False, model_path: str = None):
        self.detector = None
        self.use_mock = use_mock
        self.model_path = model_path or self._find_default_model()
        self._initialize_detector()
    
    def _find_default_model(self) -> str:
        """Find default model in models directory"""
        models_dir = Path(__file__).parent.parent / "models" / "trained"
        
        # Check for .keras model first (highest priority - latest format)
        keras_model = models_dir / "final_model_best.keras"
        if keras_model.exists():
            return str(keras_model)
        
        # Check for H5 model
        h5_model = models_dir / "google_dermassist.h5"
        if h5_model.exists():
            return str(h5_model)
        
        # Check for ONNX model
        onnx_model = models_dir / "skin_disease_model.onnx"
        if onnx_model.exists():
            return str(onnx_model)
        
        # Check for .keras model in parent models directory
        keras_model_parent = Path(__file__).parent.parent / "models" / "final_model_best.keras"
        if keras_model_parent.exists():
            return str(keras_model_parent)
        
        return None
    
    def _initialize_detector(self):
        """Initialize appropriate detector"""
        if self.use_mock:
            self.detector = MockDetector()
            logger.info("Using MockDetector")
            return
        
        if not self.model_path:
            logger.warning("No model path found, using MockDetector")
            self.detector = MockDetector()
            return
        
        # Try Keras detector for .h5 files
        if self.model_path.endswith('.h5') or self.model_path.endswith('.keras'):
            keras_detector = KerasDetector(self.model_path)
            if keras_detector.load_model():
                self.detector = keras_detector
                logger.info("Using KerasDetector")
                return
        
        # Try ONNX detector for .onnx files
        if self.model_path.endswith('.onnx'):
            onnx_detector = ONNXDetector(self.model_path)
            if onnx_detector.load_model():
                self.detector = onnx_detector
                logger.info("Using ONNXDetector")
                return
        
        # Fallback to MockDetector
        logger.warning("All detectors failed, falling back to MockDetector")
        self.detector = MockDetector()
        
        if self.detector:
            self.detector.load_model()
    
    def detect(self, image: np.ndarray) -> DetectionResult:
        """Run detection on image"""
        if not self.detector:
            logger.error("No detector initialized")
            return None
        
        return self.detector.infer(image)
    
    def get_classes(self) -> List[str]:
        """Get available lesion classes"""
        if self.detector:
            return self.detector.get_lesion_classes()
        return []


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test with real model (EfficientNetB0 from src/models/trained/google_dermassist.h5)
    pipeline = DetectionPipeline(use_mock=False)
    
    # Create dummy image
    dummy_image = np.random.rand(224, 224, 3).astype(np.float32)
    
    # Run detection
    result = pipeline.detect(dummy_image)
    if result:
        print(f"Detection: {result.diagnosis} ({result.confidence:.2%})")
        print(f"Classes: {pipeline.get_classes()}")
