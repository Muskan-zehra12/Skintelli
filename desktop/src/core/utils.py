"""
Core Utilities for Skintelli Application
Image validation, logging, and common functions
"""

import logging
import os
from pathlib import Path
from typing import Tuple, Optional
import cv2
import numpy as np
from datetime import datetime

# Configure logging
def setup_logging(log_dir: str = "./logs", log_level=logging.INFO):
    """Setup application-wide logging"""
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    log_file = log_path / f"skintelli_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


logger = logging.getLogger(__name__)


class ImageValidator:
    """Validate and process input images"""
    
    # Supported formats
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
    MIN_IMAGE_SIZE = (64, 64)
    MAX_IMAGE_SIZE = (4096, 4096)
    
    @staticmethod
    def validate_file_format(file_path: str) -> Tuple[bool, str]:
        """
        Validate image file format
        
        Returns:
            (is_valid, message)
        """
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext not in ImageValidator.SUPPORTED_FORMATS:
            return False, f"Unsupported format. Supported: {', '.join(ImageValidator.SUPPORTED_FORMATS)}"
        
        return True, "Format valid"
    
    @staticmethod
    def validate_file_size(file_path: str) -> Tuple[bool, str]:
        """Validate file size"""
        try:
            file_size = os.path.getsize(file_path)
            
            if file_size > ImageValidator.MAX_FILE_SIZE:
                return False, f"File too large. Max size: {ImageValidator.MAX_FILE_SIZE / (1024*1024):.1f} MB"
            
            if file_size == 0:
                return False, "File is empty"
            
            return True, "File size valid"
            
        except OSError as e:
            return False, f"Error reading file: {str(e)}"
    
    @staticmethod
    def validate_image_dimensions(file_path: str) -> Tuple[bool, str]:
        """Validate image dimensions"""
        try:
            image = cv2.imread(file_path)
            
            if image is None:
                return False, "Unable to read image file"
            
            height, width = image.shape[:2]
            
            if (width, height) < ImageValidator.MIN_IMAGE_SIZE:
                return False, f"Image too small. Min: {ImageValidator.MIN_IMAGE_SIZE}"
            
            if (width, height) > ImageValidator.MAX_IMAGE_SIZE:
                return False, f"Image too large. Max: {ImageValidator.MAX_IMAGE_SIZE}"
            
            return True, f"Image dimensions valid: {width}x{height}"
            
        except Exception as e:
            return False, f"Error reading image: {str(e)}"
    
    @staticmethod
    def validate_image_quality(file_path: str) -> Tuple[bool, str]:
        """Validate image quality (check for noise, blur, etc.)"""
        try:
            image = cv2.imread(file_path)
            
            if image is None:
                return False, "Unable to read image"
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Calculate Laplacian variance (indicator of blur)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Threshold for blur detection (lower = blurrier)
            blur_threshold = 100
            
            if laplacian_var < blur_threshold:
                return False, f"Image quality too low (blurry). Score: {laplacian_var:.1f}"
            
            return True, f"Image quality acceptable. Clarity score: {laplacian_var:.1f}"
            
        except Exception as e:
            return False, f"Error analyzing image quality: {str(e)}"
    
    @staticmethod
    def validate_image(file_path: str) -> Tuple[bool, str]:
        """
        Comprehensive image validation
        
        Returns:
            (is_valid, message)
        """
        # Check file format
        valid, msg = ImageValidator.validate_file_format(file_path)
        if not valid:
            return False, f"Format validation failed: {msg}"
        
        # Check file size
        valid, msg = ImageValidator.validate_file_size(file_path)
        if not valid:
            return False, f"Size validation failed: {msg}"
        
        # Check dimensions
        valid, msg = ImageValidator.validate_image_dimensions(file_path)
        if not valid:
            return False, f"Dimension validation failed: {msg}"
        
        # Check quality
        valid, msg = ImageValidator.validate_image_quality(file_path)
        if not valid:
            logger.warning(f"Quality warning: {msg}")
            # Don't fail on quality, just warn
        
        return True, "All validations passed"


class ImageProcessor:
    """Process and normalize images"""
    
    @staticmethod
    def load_image(file_path: str) -> Optional[np.ndarray]:
        """Load image from file"""
        try:
            image = cv2.imread(file_path)
            if image is None:
                logger.error(f"Failed to load image: {file_path}")
                return None
            return image
        except Exception as e:
            logger.error(f"Error loading image: {e}")
            return None
    
    @staticmethod
    def preprocess_image(image: np.ndarray, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
        """
        Preprocess image for model inference
        Resize, normalize, and convert to tensor format
        """
        try:
            # Resize to target size
            resized = cv2.resize(image, target_size)
            
            # Normalize to 0-1 range
            normalized = resized.astype(np.float32) / 255.0
            
            # Convert BGR to RGB
            rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            rgb_normalized = rgb.astype(np.float32) / 255.0
            
            return rgb_normalized
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            return None
    
    @staticmethod
    def save_image(image: np.ndarray, output_path: str) -> bool:
        """Save image to file"""
        try:
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            cv2.imwrite(output_path, image)
            logger.info(f"Image saved: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving image: {e}")
            return False


class PerformanceMonitor:
    """Monitor performance metrics"""
    
    def __init__(self):
        self.timings = {}
    
    def start_timer(self, label: str):
        """Start a timer"""
        self.timings[label] = {'start': datetime.now()}
    
    def stop_timer(self, label: str) -> float:
        """Stop timer and return elapsed time in seconds"""
        if label not in self.timings:
            logger.warning(f"Timer '{label}' not started")
            return 0.0
        
        elapsed = (datetime.now() - self.timings[label]['start']).total_seconds()
        self.timings[label]['elapsed'] = elapsed
        
        logger.info(f"Timer '{label}': {elapsed:.3f}s")
        return elapsed
    
    def get_all_timings(self) -> dict:
        """Get all recorded timings"""
        return {k: v.get('elapsed', 0) for k, v in self.timings.items()}


if __name__ == "__main__":
    logger = setup_logging()
    
    print("Utilities module ready")
