# Quick Start Guide - Skintelli Testing

## Running the Application

### Step 1: Navigate to Project
```bash
cd d:\IT initiative\FYP1-muskan
.\.venv\Scripts\Activate.ps1
cd desktop
```

### Step 2: Start Application
```bash
python run.py
```

## First Time Setup

### Create Test Account
1. **Click "Sign Up" tab**
2. **Enter credentials:**
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `password123`
3. **Click "Sign Up"**
4. **Switch to "Login" tab** and login

## Testing Analysis Feature

### Create Test Image
```python
# In a separate terminal:
cd d:\IT initiative\FYP1-muskan\desktop
python

# Then run:
import numpy as np
import cv2

img = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
cv2.imwrite("test_lesion.jpg", img)
exit()
```

### Upload and Analyze
1. **In main application window:**
2. Click **"Upload Image"**
3. Select the test image `test_lesion.jpg`
4. **Wait for analysis** (usually <1 second)

### View Results
- **Left panel**: Original image
- **Right panel**: Heatmap visualization
- **Bottom area**: Diagnosis and explanation

### Check History
1. Click **"View History"**
2. See all past analyses for your account
3. Go back to upload more images

## Expected Behavior

### Successful Analysis Shows:
- ✅ Diagnosis (e.g., "Melanoma", "Nevus")
- ✅ Confidence percentage (e.g., "87%")
- ✅ Detailed explanation with characteristics and recommendations
- ✅ Heatmap showing regions the AI focused on
- ✅ Analysis saved to history

### Performance
- **Total time**: < 1 second (target: < 10 seconds)
- **UI remains responsive**
- **No freezing or hanging**

## Testing Different Scenarios

### Test 1: Valid Image Upload
**Expected**: Successful analysis, diagnosis shown

### Test 2: Invalid File
**Try**: Upload a text file or PDF
**Expected**: Error message "Unsupported format"

### Test 3: Multiple Analyses
**Try**: Upload several different test images
**Expected**: All appear in history

### Test 4: User History
**Try**: Login with different accounts
**Expected**: Each user sees only their own analyses

### Test 5: Logout/Relogin
**Try**: Logout and login again
**Expected**: Previous analyses still available

## Database Verification

### Check Database Contents
```bash
# In desktop directory
python -c "
from src.database.models import UserManager, AnalysisManager
um = UserManager()
am = AnalysisManager()

users = um.connection.execute('SELECT COUNT(*) FROM users').fetchone()
analyses = am.connection.execute('SELECT COUNT(*) FROM analyses').fetchone()

print(f'Users: {users[0]}')
print(f'Analyses: {analyses[0]}')
"
```

## Checking Logs

### View Application Log
```bash
# Most recent log file
Get-Content skintelli.log -Tail 50
```

### Common Log Messages
- `INFO - Starting Skintelli application...` - App starting
- `INFO - Database initialized` - DB ready
- `INFO - User logged in` - Authentication successful
- `INFO - Analysis saved` - Result stored
- `WARNING - Knowledge base not found` - Normal (auto-creates)

## Features to Test

### Fully Implemented ✅
- [x] User signup/login
- [x] Image upload
- [x] Detection & classification
- [x] Heatmap generation
- [x] Explanation generation
- [x] History tracking
- [x] Analysis storage

### In Progress 🔄
- [ ] Camera capture
- [ ] PDF export
- [ ] Real ONNX model integration
- [ ] Advanced LLM

## Troubleshooting

### "Username already exists"
**Solution**: Use a different username or delete database:
```bash
Remove-Item data\skintelli.db
```

### "Image validation failed"
**Check**: Image is JPG/PNG, size between 64x64 and 4096x4096

### Application doesn't start
**Try**:
```bash
# Clear cache
Remove-Item -Recurse src\__pycache__

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Run again
python run.py
```

### Database locked error
**Solution**: Close any other instances and restart:
```bash
Remove-Item data\skintelli.db
python run.py
```

## Demo Workflow

1. **Start app**: `python run.py`
2. **Sign up**: Create new user account
3. **Generate test image**:
   ```bash
   # In Python:
   import numpy as np, cv2
   cv2.imwrite('test.jpg', np.random.randint(0,256,(224,224,3),dtype=np.uint8))
   ```
4. **Upload**: Click "Upload Image", select test.jpg
5. **View results**: Diagnosis appears in explanation area
6. **Check history**: Click "View History" to see saved analyses
7. **Logout**: Click "Logout" to test session persistence

## Next: Production Testing

When ready for production:

1. **Integrate real YOLOv8 model**
   - Download pre-trained model
   - Update `detection.py` to use ONNXDetector
   - Test with medical dataset

2. **Implement camera capture**
   - Add OpenCV camera feed
   - Capture and analyze in real-time

3. **Complete PDF export**
   - Generate professional reports
   - Include all analysis data

4. **Performance optimization**
   - Profile for bottlenecks
   - Optimize image processing
   - Cache common operations

## Resources

- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [OpenCV Python](https://docs.opencv.org/master/d6/d00/tutorial_py_root.html)
- [ONNX Runtime](https://onnxruntime.ai/)
- [Medical AI Resources](docs/medical_knowledge_base.json)

---

**Application Status**: ✅ RUNNING AND TESTABLE
**Last Updated**: January 15, 2026
