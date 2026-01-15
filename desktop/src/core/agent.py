"""
Agentic Workflow Orchestrator
Coordinates the entire pipeline: Input -> Detection -> Explainability -> Interpretation -> Output
"""

import logging
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import numpy as np

from core.detection import DetectionPipeline
from core.explainability import HeatmapGenerator
from core.interpretation import ExplanationGenerator, MedicalKnowledgeBase
from core.utils import ImageValidator, ImageProcessor, PerformanceMonitor

logger = logging.getLogger(__name__)


class AnalysisAgent:
    """
    Main orchestrator for the analysis pipeline
    Manages the workflow: validate -> detect -> explain -> interpret
    """
    
    def __init__(self, use_mock_model: bool = False, model_path: str = None):
        self.detection_pipeline = DetectionPipeline(use_mock=use_mock_model, model_path=model_path)
        self.heatmap_generator = HeatmapGenerator()
        self.kb = MedicalKnowledgeBase()
        self.explanation_generator = ExplanationGenerator(self.kb)
        self.monitor = PerformanceMonitor()
    
    def analyze_image(self, image_path: str, output_dir: str = "./analysis_results") -> Optional[Dict[str, Any]]:
        """
        Complete analysis pipeline
        
        Args:
            image_path: Path to input image
            output_dir: Directory to save results
            
        Returns:
            Analysis result dictionary or None if failed
        """
        self.monitor.start_timer("total_analysis")
        
        try:
            # Step 1: Validate image
            logger.info(f"Step 1: Validating image: {image_path}")
            self.monitor.start_timer("validation")
            
            valid, msg = ImageValidator.validate_image(image_path)
            if not valid:
                logger.error(f"Image validation failed: {msg}")
                return None
            
            self.monitor.stop_timer("validation")
            logger.info(f"✓ Validation passed: {msg}")
            
            # Step 2: Load and preprocess image
            logger.info("Step 2: Loading and preprocessing image")
            self.monitor.start_timer("loading")
            
            original_image = ImageProcessor.load_image(image_path)
            if original_image is None:
                logger.error("Failed to load image")
                return None
            
            processed_image = ImageProcessor.preprocess_image(original_image)
            if processed_image is None:
                logger.error("Failed to preprocess image")
                return None
            
            self.monitor.stop_timer("loading")
            
            # Step 3: Detection
            logger.info("Step 3: Running detection")
            self.monitor.start_timer("detection")
            
            detection_result = self.detection_pipeline.detect(processed_image)
            if not detection_result:
                logger.error("Detection failed")
                return None
            
            self.monitor.stop_timer("detection")
            logger.info(f"✓ Detection: {detection_result.diagnosis} ({detection_result.confidence:.1%})")
            
            # Step 4: Generate heatmap
            logger.info("Step 4: Generating heatmap")
            self.monitor.start_timer("heatmap")
            
            heatmap = self.heatmap_generator.generate_heatmap(processed_image, detection_result)
            if heatmap is None:
                logger.warning("Heatmap generation failed")
                heatmap = np.zeros_like(original_image)
            
            self.monitor.stop_timer("heatmap")
            
            # Step 5: Generate explanation
            logger.info("Step 5: Generating explanation")
            self.monitor.start_timer("explanation")
            
            explanation = self.explanation_generator.generate_explanation(
                detection_result.diagnosis,
                detection_result.confidence,
                detection_result.class_probabilities
            )
            
            self.monitor.stop_timer("explanation")
            
            # Step 6: Save outputs
            logger.info("Step 6: Saving results")
            self.monitor.start_timer("saving")
            
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save heatmap
            heatmap_path = output_path / f"heatmap_{timestamp}.png"
            ImageProcessor.save_image(heatmap, str(heatmap_path))
            
            # Overlay heatmap on original
            overlay_image = self.heatmap_generator.overlay_heatmap_on_image(original_image, heatmap)
            overlay_path = output_path / f"overlay_{timestamp}.png"
            if overlay_image is not None:
                ImageProcessor.save_image(overlay_image, str(overlay_path))
            
            self.monitor.stop_timer("saving")
            
            # Step 7: Compile results
            logger.info("Step 7: Compiling results")
            
            timings = self.monitor.get_all_timings()
            total_time = timings.get('total_analysis', 0)
            
            if total_time > 10:
                logger.warning(f"Analysis took longer than 10 seconds: {total_time:.2f}s")
            
            analysis_result = {
                'status': 'success',
                'timestamp': datetime.now().isoformat(),
                'input_image_path': str(image_path),
                'detection': {
                    'diagnosis': detection_result.diagnosis,
                    'confidence': float(detection_result.confidence),
                    'class_probabilities': detection_result.class_probabilities,
                    'bounding_boxes': detection_result.bounding_boxes
                },
                'explainability': {
                    'heatmap_path': str(heatmap_path),
                    'overlay_path': str(overlay_path) if overlay_image is not None else None
                },
                'explanation': explanation,
                'performance': {
                    'validation_time': f"{timings.get('validation', 0):.3f}s",
                    'loading_time': f"{timings.get('loading', 0):.3f}s",
                    'detection_time': f"{timings.get('detection', 0):.3f}s",
                    'heatmap_time': f"{timings.get('heatmap', 0):.3f}s",
                    'explanation_time': f"{timings.get('explanation', 0):.3f}s",
                    'total_time': f"{total_time:.3f}s"
                }
            }
            
            self.monitor.stop_timer("total_analysis")
            
            logger.info("✓ Analysis complete")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Unexpected error during analysis: {e}", exc_info=True)
            return None
    
    def batch_analyze(self, image_dir: str, output_dir: str = "./batch_results") -> list:
        """
        Analyze multiple images from a directory
        
        Args:
            image_dir: Directory containing images
            output_dir: Directory to save results
            
        Returns:
            List of analysis results
        """
        image_dir = Path(image_dir)
        results = []
        
        supported_formats = {'.jpg', '.jpeg', '.png', '.bmp'}
        image_files = [f for f in image_dir.iterdir() 
                      if f.suffix.lower() in supported_formats]
        
        logger.info(f"Processing {len(image_files)} images from {image_dir}")
        
        for i, image_file in enumerate(image_files, 1):
            logger.info(f"Processing image {i}/{len(image_files)}: {image_file.name}")
            
            result = self.analyze_image(str(image_file), output_dir)
            if result:
                results.append(result)
        
        logger.info(f"Batch processing complete: {len(results)}/{len(image_files)} successful")
        return results


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create test image
    import cv2
    test_image = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
    test_path = "./test_image.jpg"
    cv2.imwrite(test_path, test_image)
    
    # Test orchestrator
    agent = AnalysisAgent(use_mock_model=False)
    result = agent.analyze_image(test_path)
    
    if result:
        print(f"\n{'='*80}")
        print("ANALYSIS RESULT")
        print(f"{'='*80}")
        print(f"Status: {result['status']}")
        print(f"Diagnosis: {result['detection']['diagnosis']}")
        print(f"Confidence: {result['detection']['confidence']:.1%}")
        print(f"Total Time: {result['performance']['total_time']}")
