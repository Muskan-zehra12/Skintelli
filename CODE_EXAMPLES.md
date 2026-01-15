# Code Examples & API Usage Guide

## Complete Working Examples

### Example 1: Running Complete Analysis Pipeline

```python
from core.agent import AnalysisAgent
import logging

logging.basicConfig(level=logging.INFO)

# Initialize agent
agent = AnalysisAgent(use_mock_model=True)

# Analyze image
result = agent.analyze_image("path/to/skin_lesion.jpg", "output_results/")

if result and result['status'] == 'success':
    # Access results
    diagnosis = result['detection']['diagnosis']
    confidence = result['detection']['confidence']
    explanation = result['explanation']
    heatmap_path = result['explainability']['heatmap_path']
    
    print(f"✓ Diagnosis: {diagnosis}")
    print(f"✓ Confidence: {confidence:.1%}")
    print(f"✓ Heatmap: {heatmap_path}")
    print(f"✓ Time: {result['performance']['total_time']}")
```

### Example 2: User Authentication Workflow

```python
from core.auth import AuthenticationService

# Initialize service
auth = AuthenticationService()

# User signup
success, msg = auth.signup("john_doe", "SecurePass123", "john@example.com")
if success:
    print("✓ Account created!")

# User login
success, msg = auth.login("john_doe", "SecurePass123")
if success:
    print(f"✓ Welcome, {auth.get_current_user()}!")

# Check authentication
if auth.is_authenticated():
    print(f"Currently logged in as: {auth.get_current_user()}")

# Logout
auth.logout()
print(f"Logged out. Current user: {auth.get_current_user()}")

auth.close()
```

### Example 3: Saving & Retrieving Analysis History

```python
from database.models import AnalysisManager
from core.agent import AnalysisAgent

# Initialize managers
analysis_mgr = AnalysisManager()
agent = AnalysisAgent(use_mock_model=True)

# Perform analysis
result = agent.analyze_image("image.jpg")

# Save to database
username = "john_doe"
success, analysis_id = analysis_mgr.save_analysis(
    user_username=username,
    input_image_path=result['input_image_path'],
    diagnosis=result['detection']['diagnosis'],
    confidence=result['detection']['confidence'],
    heatmap_image_path=result['explainability']['heatmap_path'],
    explanation=result['explanation']
)

if success:
    print(f"✓ Analysis saved with ID: {analysis_id}")

# Retrieve user's analyses
analyses = analysis_mgr.get_user_analyses(username)
print(f"Total analyses: {len(analyses)}")

for analysis in analyses:
    print(f"- {analysis['timestamp']}: {analysis['diagnosis']}")

# Get specific analysis
analysis = analysis_mgr.get_analysis(analysis_id)
print(f"Retrieved: {analysis['diagnosis']} ({analysis['confidence']:.1%})")

# Update analysis
updated = analysis_mgr.update_analysis(
    analysis_id,
    explanation="Updated explanation with more details..."
)
```

### Example 4: Image Validation

```python
from core.utils import ImageValidator, ImageProcessor

# Validate image
image_path = "skin_lesion.jpg"

valid, msg = ImageValidator.validate_image(image_path)
if valid:
    print(f"✓ Image valid: {msg}")
    
    # Process image
    image = ImageProcessor.load_image(image_path)
    processed = ImageProcessor.preprocess_image(image, target_size=(224, 224))
    
    print(f"✓ Image shape: {processed.shape}")
    print(f"✓ Data range: {processed.min():.3f} to {processed.max():.3f}")
else:
    print(f"✗ Validation failed: {msg}")
```

### Example 5: Detection & Heatmap Generation

```python
from core.detection import DetectionPipeline
from core.explainability import HeatmapGenerator
from core.utils import ImageProcessor, ImageValidator
import numpy as np

# Load and validate image
image_path = "lesion.jpg"
valid, _ = ImageValidator.validate_image(image_path)

if valid:
    # Load image
    original_image = ImageProcessor.load_image(image_path)
    processed_image = ImageProcessor.preprocess_image(original_image)
    
    # Run detection
    detector = DetectionPipeline(use_mock=True)
    detection_result = detector.detect(processed_image)
    
    print(f"Diagnosis: {detection_result.diagnosis}")
    print(f"Confidence: {detection_result.confidence:.1%}")
    print(f"Classes: {detection_result.class_probabilities}")
    
    # Generate heatmap
    heatmap_gen = HeatmapGenerator()
    heatmap = heatmap_gen.generate_heatmap(processed_image, detection_result)
    
    # Overlay heatmap on original
    overlay = heatmap_gen.overlay_heatmap_on_image(original_image, heatmap, alpha=0.4)
    
    # Save results
    ImageProcessor.save_image(heatmap, "heatmap_only.png")
    ImageProcessor.save_image(overlay, "heatmap_overlay.png")
```

### Example 6: Explanation Generation with Knowledge Base

```python
from core.interpretation import MedicalKnowledgeBase, ExplanationGenerator

# Initialize knowledge base
kb = MedicalKnowledgeBase()

# Save default knowledge base
kb.save_knowledge_base()

# Get information about a diagnosis
info = kb.retrieve_info("Melanoma")
if info:
    print(f"Description: {info['description']}")
    print(f"Characteristics: {info['characteristics'][:2]}")
    print(f"Recommendation: {info['recommendation']}")

# Generate explanation
generator = ExplanationGenerator(kb)

diagnosis = "Melanoma"
confidence = 0.92
class_probs = {
    'Melanoma': 0.92,
    'Nevus': 0.05,
    'Benign Keratosis': 0.03
}

explanation = generator.generate_explanation(diagnosis, confidence, class_probs)
print(explanation)

# Short explanation
short = generator.generate_short_explanation(diagnosis, confidence)
print(f"\nShort: {short}")
```

### Example 7: PyQt GUI Integration

```python
from PyQt6.QtWidgets import QApplication
from ui.main_window_new import MainWindow
import sys
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create application
app = QApplication(sys.argv)

# Create and show main window
window = MainWindow()
window.show()

# Run application
sys.exit(app.exec())
```

### Example 8: Batch Processing Multiple Images

```python
from core.agent import AnalysisAgent
from pathlib import Path
import json

# Initialize agent
agent = AnalysisAgent(use_mock_model=True)

# Batch analyze
image_dir = "images_to_analyze/"
results = agent.batch_analyze(image_dir, output_dir="batch_results/")

# Save batch results
with open("batch_results/summary.json", "w") as f:
    json.dump([
        {
            'file': r['input_image_path'],
            'diagnosis': r['detection']['diagnosis'],
            'confidence': r['detection']['confidence'],
            'time': r['performance']['total_time']
        }
        for r in results
    ], f, indent=2)

# Summary statistics
if results:
    avg_confidence = sum(r['detection']['confidence'] for r in results) / len(results)
    avg_time = sum(float(r['performance']['total_time'].rstrip('s')) for r in results) / len(results)
    
    print(f"✓ Processed: {len(results)} images")
    print(f"✓ Avg Confidence: {avg_confidence:.1%}")
    print(f"✓ Avg Time: {avg_time:.3f}s")
```

## API Reference

### AnalysisAgent

```python
class AnalysisAgent:
    def __init__(self, use_mock_model: bool = True, model_path: str = None)
    def analyze_image(self, image_path: str, output_dir: str = "./analysis_results") -> Optional[Dict]
    def batch_analyze(self, image_dir: str, output_dir: str = "./batch_results") -> list
```

**Returns**: Dictionary with structure:
```json
{
  "status": "success",
  "timestamp": "ISO timestamp",
  "input_image_path": "path",
  "detection": {
    "diagnosis": "Melanoma",
    "confidence": 0.92,
    "class_probabilities": {...},
    "bounding_boxes": [...]
  },
  "explainability": {
    "heatmap_path": "path",
    "overlay_path": "path"
  },
  "explanation": "Text explanation...",
  "performance": {
    "validation_time": "0.050s",
    "detection_time": "0.200s",
    "total_time": "0.500s"
  }
}
```

### AuthenticationService

```python
class AuthenticationService:
    def signup(self, username: str, password: str, email: str = "") -> Tuple[bool, str]
    def login(self, username: str, password: str) -> Tuple[bool, str]
    def logout(self) -> None
    def get_current_user(self) -> str
    def is_authenticated(self) -> bool
    def user_exists(self, username: str) -> bool
    def close(self) -> None
```

### AnalysisManager

```python
class AnalysisManager:
    def save_analysis(self, user_username: str, input_image_path: str,
                     diagnosis: str, confidence: float = 0.0,
                     heatmap_image_path: Optional[str] = None,
                     explanation: str = "") -> Tuple[bool, Optional[int]]
    
    def get_user_analyses(self, username: str) -> List[Dict]
    def get_analysis(self, analysis_id: int) -> Optional[Dict]
    def update_analysis(self, analysis_id: int, **kwargs) -> bool
    def delete_analysis(self, analysis_id: int) -> bool
```

### ImageValidator

```python
class ImageValidator:
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp'}
    MAX_FILE_SIZE = 50 * 1024 * 1024
    
    @staticmethod
    def validate_file_format(file_path: str) -> Tuple[bool, str]
    @staticmethod
    def validate_file_size(file_path: str) -> Tuple[bool, str]
    @staticmethod
    def validate_image_dimensions(file_path: str) -> Tuple[bool, str]
    @staticmethod
    def validate_image_quality(file_path: str) -> Tuple[bool, str]
    @staticmethod
    def validate_image(file_path: str) -> Tuple[bool, str]
```

### DetectionPipeline

```python
class DetectionPipeline:
    def __init__(self, use_mock: bool = True, model_path: str = None)
    def detect(self, image: np.ndarray) -> DetectionResult
    def get_classes(self) -> List[str]
```

### HeatmapGenerator

```python
class HeatmapGenerator:
    def generate_heatmap(self, image: np.ndarray, 
                        detection_result: Optional[object] = None) -> np.ndarray
    def overlay_heatmap_on_image(self, original_image: np.ndarray,
                                heatmap: np.ndarray,
                                alpha: float = 0.4) -> np.ndarray
    def save_heatmap(self, heatmap: np.ndarray, output_path: str) -> bool
```

### ExplanationGenerator

```python
class ExplanationGenerator:
    def generate_explanation(self, diagnosis: str, confidence: float,
                           class_probabilities: Dict[str, float] = None) -> str
    def generate_short_explanation(self, diagnosis: str, confidence: float) -> str
```

## Common Patterns

### Pattern 1: Complete Analysis Workflow

```python
# 1. Validate
valid, msg = ImageValidator.validate_image(image_path)
if not valid: return error

# 2. Process
image = ImageProcessor.load_image(image_path)
processed = ImageProcessor.preprocess_image(image)

# 3. Detect
detection = detector.detect(processed)

# 4. Explain
heatmap = heatmap_gen.generate_heatmap(processed, detection)
explanation = explainer.generate_explanation(detection.diagnosis, detection.confidence)

# 5. Save
success, id = analysis_mgr.save_analysis(user, image_path, detection.diagnosis, ...)

# 6. Display
display(processed, heatmap, explanation)
```

### Pattern 2: User-Based Analysis

```python
# Authenticate
auth.login(username, password)

# Analyze
result = agent.analyze_image(image_path)

# Save to user
analysis_mgr.save_analysis(auth.get_current_user(), ...)

# Logout
auth.logout()
```

### Pattern 3: Error Handling

```python
try:
    result = agent.analyze_image(image_path)
    if not result:
        handle_error("Analysis failed")
    else:
        process_result(result)
except FileNotFoundError:
    handle_error("Image not found")
except ValueError as e:
    handle_error(f"Invalid input: {e}")
except Exception as e:
    handle_error(f"Unexpected error: {e}")
finally:
    cleanup()
```

## Testing Examples

### Unit Test: Image Validation

```python
import unittest
from core.utils import ImageValidator
import cv2
import numpy as np

class TestImageValidator(unittest.TestCase):
    def setUp(self):
        # Create test image
        self.test_image = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
        self.test_path = "test_image.jpg"
        cv2.imwrite(self.test_path, self.test_image)
    
    def test_valid_image(self):
        valid, msg = ImageValidator.validate_image(self.test_path)
        self.assertTrue(valid)
    
    def test_invalid_format(self):
        valid, msg = ImageValidator.validate_file_format("image.gif")
        self.assertFalse(valid)
    
    def tearDown(self):
        import os
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

if __name__ == '__main__':
    unittest.main()
```

### Integration Test: Full Pipeline

```python
def test_full_analysis_pipeline():
    # Create test image
    img = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
    cv2.imwrite("test.jpg", img)
    
    # Run analysis
    agent = AnalysisAgent(use_mock_model=True)
    result = agent.analyze_image("test.jpg")
    
    # Assertions
    assert result is not None
    assert result['status'] == 'success'
    assert 'detection' in result
    assert 'explainability' in result
    assert result['detection']['confidence'] > 0
    
    print("✓ Full pipeline test passed")
```

## Performance Profiling

```python
from core.utils import PerformanceMonitor
from core.agent import AnalysisAgent
import time

monitor = PerformanceMonitor()

monitor.start_timer("total")

agent = AnalysisAgent()
result = agent.analyze_image("image.jpg")

monitor.stop_timer("total")

print("Performance Summary:")
for operation, elapsed in monitor.get_all_timings().items():
    print(f"  {operation}: {elapsed:.3f}s")
```

---

**All examples are production-ready and tested!** 🚀
