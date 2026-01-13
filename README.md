# Skintelli - Intelligent Skin Disease Detection System

An AI-powered desktop application for detecting skin diseases, infections, and abnormalities using computer vision and advanced image analysis. The system captures images via camera or upload, analyzes them for potential skin conditions, and provides visual heatmaps with detailed diagnoses.

## 🎯 Features

### 🔐 Complete Authentication System
- **User Registration**: Create accounts with email and password
- **Secure Login**: Persistent session management
- **Guest Mode**: 3 free analysis attempts without login
- **Freemium Model**:
  - 👤 **Guest Tier**: 3 analyses per session
  - 🎁 **Free Tier**: 15 analyses per month
  - ⭐ **Pro Tier**: Unlimited analyses

### 🎨 Modern Single-Window Interface
- **Unified Design**: All features in one cohesive window
- **Tabbed Authentication**: Sign In & Sign Up tabs in main window
- **Seamless Navigation**: Instant transitions between screens
- **Responsive Layout**: Adapts to different screen sizes
- **Professional Styling**: Color-coded buttons with emoji indicators

### 📷 Interactive Live Camera Capture
- **HD Resolution**: 1920x1080 full HD camera capture
- **Real-Time Controls**:
  - 🔆 **Brightness Slider**: Adjust -50 to +50 in real-time
  - 🎨 **Contrast Slider**: Adjust -50 to +50 in real-time
- **Distance Indicator**: Real-time feedback with color coding
  - 🟢 **Green "Fit"**: Perfect positioning
  - 🔴 **Red "Too Near"**: Move camera back
  - 🟡 **Yellow "Too Far"**: Move camera closer
- **ROI Guide**: Central guide box showing capture area
- **One-Click Capture**: Capture button with visual feedback

### 🔬 Intelligent Skin Analysis
- **Multi-Feature Detection**:
  - 🔴 **Redness Detection**: Identifies inflammation, irritation, wounds
  - ⚫ **Dark Spot Detection**: Finds bruising, hyperpigmentation, necrosis
  - ⚪ **Light Spot Detection**: Detects scars, vitiligo, depigmentation
  - 📐 **Texture Analysis**: Identifies rashes, rough patches, irregularities

### 📊 Visual Heatmap Output
- **Color-Coded Visualization**: Red/yellow zones indicate problem areas
- **Contour Outlines**: Green contours mark affected regions
- **Overlay Blending**: Original image with analysis overlay for comparison
- **Live Feedback**: Loading indicators and progress messages

### ✅ Comprehensive Diagnosis
- **Severity Indicators**: 
  - ✅ **None**: No issues detected
  - 🟡 **Low**: Minor abnormalities
  - 🟠 **Medium**: Moderate concerns
  - 🔴 **High**: Significant findings
- **Affected Percentage**: Shows what % of examined area has issues
- **Detailed Findings**: Lists specific abnormalities detected
- **Medical Recommendations**: Guidance based on severity
- **Professional Disclaimer**: Reminds users to consult healthcare professionals

### 🎬 Image Quality
- **Natural HD Capture**: Images remain exactly as camera captures them
- **No Artificial Processing**: True representation for accurate diagnosis
- **High-Quality Scaling**: Smooth rendering at all sizes
- **File Info Display**: Shows file name and size after upload

## 📁 Project Structure

```
FYP1-muskan/
├── desktop/
│   ├── src/
│   │   ├── main.py                    # Application entry point
│   │   ├── ui/
│   │   │   ├── main_window.py         # Main window with auth, analysis, paywall
│   │   │   ├── dialogs.py             # Authentication and paywall dialogs
│   │   │   └── widgets/
│   │   │       └── dual_panel.py      # Image capture and analysis UI
│   │   └── core/
│   │       ├── auth.py                # User management and authentication
│   │       ├── usage_tracker.py       # Guest attempt tracking
│   │       └── skin_analyzer.py       # AI analysis engine
│   ├── tests/
│   └── requirements.txt               # Python dependencies
├── specs/
│   ├── 001-skin-disease-detection/
│   └── 002-skin-disease-detection/
├── history/
└── README.md                          # This file
```

## 🛠️ Technology Stack

- **Python 3.11+**
- **PyQt6**: Cross-platform desktop GUI with modern styling
- **OpenCV (cv2)**: Image processing, camera capture, and analysis
- **NumPy**: Numerical computations
- **SciPy**: Scientific computing
- **JSON**: User data persistence

## 📋 Installation

### Prerequisites
- Python 3.11 or higher
- Virtual environment (recommended)
- Git
- Camera (for live capture, optional)

### Setup Steps

1. **Clone the repository**:
```bash
git clone https://github.com/Muskan-zehra12/Skintelli.git
cd Skintelli
```

2. **Create virtual environment**:
```bash
python -m venv .venv
```

3. **Activate virtual environment**:

**Windows (PowerShell)**:
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD)**:
```cmd
.venv\Scripts\activate.bat
```

**Linux/Mac**:
```bash
source .venv/bin/activate
```

4. **Install dependencies**:
```bash
pip install -r desktop/requirements.txt
```

Required packages:
- PyQt6 (6.10+)
- opencv-python (4.8+)
- numpy (2.0+)

## 🚀 Running the Application

### Quick Start
```bash
# Navigate to desktop directory
cd desktop/src

# Run the application
python main.py
```

Or from the project root:
```bash
python desktop/src/main.py
```

### With Virtual Environment (Recommended)
```powershell
# Windows PowerShell
& ".\.venv\Scripts\python.exe" "desktop/src/main.py"
```

## 📖 Usage Guide

### 1. **Authentication**

**First Time Users**:
- App launches with **Sign In / Sign Up tabs**
- Click **"Sign Up"** tab to create new account
- Enter full name, email, password (min. 6 characters)
- Click **"✨ Create Account"**
- Account created! Sign in to start analyzing

**Existing Users**:
- Click **"Sign In"** tab
- Enter email and password
- Click **"🔓 Sign In"**

**Try Without Signing Up**:
- Click **"Continue as Guest (3 free attempts)"**
- Get 3 free analyses in current session
- After 3 attempts, prompted to sign up

### 2. **Capture Image**

**Option A: Use Camera**
- Click **"📷 Use Camera"** to start live camera feed
- Camera control panel appears with brightness/contrast sliders
- Position body part in the central guide box
- Adjust **Brightness** and **Contrast** sliders for optimal view
- Watch the distance indicator:
  - 🔴 **Red "Too Near"**: Move camera back
  - 🟡 **Yellow "Too Far"**: Move camera closer
  - 🟢 **Green "Fit"**: Perfect positioning
- Click **"📸 Capture Image"** when indicator shows "Fit"
- Click **"❌ Stop Camera"** to exit camera mode

**Option B: Upload Image**
- Click **"📁 Upload Image"**
- Select a JPG, PNG, or JPEG image from your device
- File info (name, size) displayed in status area
- Image will appear in the left panel

### 3. **Analyze Image**
- After capturing/uploading, click **"🔬 Analyze"** button
- Wait for analysis to complete
- "🔄 Analyzing..." message shows processing status
- Right panel updates with heatmap visualization

### 4. **View Results**
- **Left Panel**: Original captured image
- **Right Panel**: Heatmap visualization
  - Green contours = affected areas
  - Color intensity = severity level
- **Diagnosis Section**: 
  - Severity level with emoji (✅/🟡/🟠/🔴)
  - Affected percentage
  - Specific findings
  - Medical recommendations

### 5. **Usage Limits**
- **Free Users**: 15 analyses per month
- **Pro Users**: Unlimited analyses
- Limit reached → Paywall screen appears
- Click **"Upgrade to Pro"** for unlimited access
- or **"Maybe Later"** to continue with restrictions

### 6. **Logout**
- Click **"Logout"** button in top right
- Returns to authentication screen
- Session ends and data is saved

## 🔬 How Analysis Works

### Detection Process

1. **Color Space Analysis**
   - Converts image to RGB, HSV, and LAB color spaces
   - Analyzes color distributions for abnormalities

2. **Redness Detection**
   - Identifies red channel dominance
   - Detects HSV-based red zones
   - Flags inflammation, wounds, irritation

3. **Dark Spot Detection**
   - Compares brightness to average
   - Finds areas significantly darker than surrounding skin
   - Indicates bruising, hyperpigmentation

4. **Light Spot Detection**
   - Identifies unusually light areas
   - Detects scars and depigmentation

5. **Texture Analysis**
   - Applies Laplacian edge detection
   - Calculates local variance
   - Identifies rough patches and rashes

6. **Heatmap Generation**
   - Combines all findings into severity map
   - Applies morphological operations for cleanup
   - Creates color-coded overlay visualization

### Severity Calculation

- **None**: < 1% affected area
- **Low**: 1-5% affected, low average severity
- **Medium**: 5-15% affected or higher severity score
- **High**: > 15% affected area

## ⚠️ Important Notes

### Camera Permissions (Windows)

If camera access is denied:

1. Open **Settings > Privacy & security > Camera**
2. Enable "Camera access"
3. Enable "Let desktop apps access your camera"
4. Close other apps using camera (Teams, Zoom, etc.)
5. Try again

The app will show a helpful dialog with an "Open Camera Settings" button if camera fails.

### Authentication Data

- User accounts stored locally in `users.json`
- Passwords encrypted with SHA256 hashing
- Session persists between app launches
- Click **Logout** to clear session

### Medical Disclaimer

**This is an AI-assisted preliminary analysis tool, NOT a medical diagnosis tool.**

- Always consult qualified healthcare professionals
- This tool provides visual guidance only
- Results should never replace professional medical evaluation
- Early consultation is recommended for any suspected abnormalities

## 📊 Example Diagnoses

### Healthy Skin
```
✅ Analysis Complete

✅ Severity: None
📊 Affected Area: 0.5%

📝 Diagnosis:
No significant skin abnormalities detected. Skin appears healthy.
Recommendation: Maintain regular skin care routine.
```

### Low Severity
```
✅ Analysis Complete

🟡 Severity: Low
📊 Affected Area: 2.3%

📝 Diagnosis:
Detected potential skin abnormalities. May include:
- Minor irregularities detected
- Slight redness or irritation
- Minor discoloration or small blemishes
Recommendation: Monitor and apply appropriate skincare.
```

### Medium Severity
```
✅ Analysis Complete

🟠 Severity: Medium
📊 Affected Area: 8.5%

📝 Diagnosis:
Detected moderate abnormalities. May include:
- Inflammation or visible redness
- Texture irregularities
- Visible lesions or rash patterns
Recommendation: Medical evaluation recommended. Please consult a dermatologist.
```

## 🔧 Troubleshooting

### Camera Not Working
- Check Windows privacy settings for camera access
- Ensure no other app is using the camera (Teams, Zoom, etc.)
- Try restarting the application
- Check if your webcam is properly connected

### "Unknown property transform" warnings
- These are safe PyQt6 CSS warnings
- App functions normally despite warnings
- Can be ignored

### Image Quality Issues
- Ensure adequate lighting
- Keep camera steady while capturing
- Maintain proper distance (distance indicator will guide)
- Use brightness/contrast sliders to optimize view
- Use a high-quality camera for best results

### Analysis Taking Too Long
- This is normal for first analysis (may take 5-10 seconds)
- Subsequent analyses are faster
- Close other CPU-intensive applications

### Cannot Sign In
- Verify email and password are correct
- Check that account was created successfully
- Clear app cache if issues persist

### Usage Limit Exceeded
- Upgrade to Pro for unlimited analyses
- Or create a new account for 15 more free analyses
- Payment gateway integration coming soon

### Python Module Not Found
```bash
# Reinstall dependencies
pip install -r desktop/requirements.txt --upgrade
```

## 📈 Future Enhancements

- [x] Authentication system
- [x] Single unified window interface
- [x] Interactive camera controls
- [x] Freemium monetization model
- [ ] Real payment gateway integration (Stripe/PayPal)
- [ ] Email verification for signups
- [ ] Password reset functionality
- [ ] Machine learning model integration with trained datasets
- [ ] Disease classification (eczema, psoriasis, acne, etc.)
- [ ] Report generation and PDF export
- [ ] Analysis history and comparison
- [ ] Multi-image batch processing
- [ ] Mobile app version
- [ ] Cloud-based analysis backend
- [ ] User profiles and medical history

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear descriptions

## 📝 License

This project is part of the FYP (Final Year Project) initiative.

## 👤 Author

Developed by Muskan - FYP1 Skin Disease Detection Project

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [Your contact information]

## 🔗 Links

- **GitHub Repository**: https://github.com/Muskan-zehra12/Skintelli
- **Project Specs**: See `/specs/` directory
- **Development History**: See `/history/` directory

---

**Last Updated**: January 13, 2026  
**Version**: 1.1.0  
**Status**: Active Development - Single Window UI with Authentication & Monetization



## 📋 Installation

### Prerequisites
- Python 3.11 or higher
- Virtual environment (recommended)
- Git

### Setup Steps

1. **Clone the repository**:
```bash
git clone https://github.com/Muskan-zehra12/Skintelli.git
cd Skintelli
```

2. **Create virtual environment**:
```bash
python -m venv .venv
```

3. **Activate virtual environment**:

**Windows (PowerShell)**:
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD)**:
```cmd
.venv\Scripts\activate.bat
```

**Linux/Mac**:
```bash
source .venv/bin/activate
```

4. **Install dependencies**:
```bash
pip install -r desktop/requirements.txt
```

Required packages:
- PyQt6 (6.10+)
- opencv-python (4.8+)
- numpy (2.0+)

## 🚀 Running the Application

### Quick Start
```bash
# Navigate to desktop directory
cd desktop/src

# Run the application
python main.py
```

Or from the project root:
```bash
python desktop/src/main.py
```

### With Virtual Environment (Recommended)
```powershell
# Windows PowerShell
& ".\.venv\Scripts\python.exe" "desktop/src/main.py"
```

## 📖 Usage Guide

### 1. **Authentication**

**First Time Users**:
- App launches with **Sign In / Sign Up tabs**
- Click **"Sign Up"** tab to create new account
- Enter full name, email, password (min. 6 characters)
- Click **"✨ Create Account"**
- Account created! Sign in to start analyzing

**Existing Users**:
- Click **"Sign In"** tab
- Enter email and password
- Click **"🔓 Sign In"**

**Try Without Signing Up**:
- Click **"Continue as Guest (3 free attempts)"**
- Get 3 free analyses in current session
- After 3 attempts, prompted to sign up

### 2. **Capture Image**

**Option A: Use Camera**
- Click **"📷 Use Camera"** to start live camera feed
- Camera control panel appears with brightness/contrast sliders
- Position body part in the central guide box
- Adjust **Brightness** and **Contrast** sliders for optimal view
- Watch the distance indicator:
  - 🔴 **Red "Too Near"**: Move camera back
  - 🟡 **Yellow "Too Far"**: Move camera closer
  - 🟢 **Green "Fit"**: Perfect positioning
- Click **"📸 Capture Image"** when indicator shows "Fit"
- Click **"❌ Stop Camera"** to exit camera mode

**Option B: Upload Image**
- Click **"📁 Upload Image"**
- Select a JPG, PNG, or JPEG image from your device
- File info (name, size) displayed in status area
- Image will appear in the left panel

### 3. **Analyze Image**
- After capturing/uploading, click **"🔬 Analyze"** button
- Wait for analysis to complete
- "🔄 Analyzing..." message shows processing status
- Right panel updates with heatmap visualization

### 4. **View Results**
- **Left Panel**: Original captured image
- **Right Panel**: Heatmap visualization
  - Green contours = affected areas
  - Color intensity = severity level
- **Diagnosis Section**: 
  - Severity level with emoji (✅/🟡/🟠/🔴)
  - Affected percentage
  - Specific findings
  - Medical recommendations

### 5. **Usage Limits**
- **Free Users**: 15 analyses per month
- **Pro Users**: Unlimited analyses
- Limit reached → Paywall screen appears
- Click **"Upgrade to Pro"** for unlimited access
- or **"Maybe Later"** to continue with restrictions

### 6. **Logout**
- Click **"Logout"** button in top right
- Returns to authentication screen
- Session ends and data is saved

## 🔬 How Analysis Works

### Detection Process

1. **Color Space Analysis**
   - Converts image to RGB, HSV, and LAB color spaces
   - Analyzes color distributions for abnormalities

2. **Redness Detection**
   - Identifies red channel dominance
   - Detects HSV-based red zones
   - Flags inflammation, wounds, irritation

3. **Dark Spot Detection**
   - Compares brightness to average
   - Finds areas significantly darker than surrounding skin
   - Indicates bruising, hyperpigmentation

4. **Light Spot Detection**
   - Identifies unusually light areas
   - Detects scars and depigmentation

5. **Texture Analysis**
   - Applies Laplacian edge detection
   - Calculates local variance
   - Identifies rough patches and rashes

6. **Heatmap Generation**
   - Combines all findings into severity map
   - Applies morphological operations for cleanup
   - Creates color-coded overlay visualization

### Severity Calculation

- **None**: < 1% affected area
- **Low**: 1-5% affected, low average severity
- **Medium**: 5-15% affected or higher severity score
- **High**: > 15% affected area

## ⚠️ Important Notes

### Camera Permissions (Windows)

If camera access is denied:

1. Open **Settings > Privacy & security > Camera**
2. Enable "Camera access"
3. Enable "Let desktop apps access your camera"
4. Close other apps using camera (Teams, Zoom, etc.)
5. Try again

The app will show a helpful dialog with an "Open Camera Settings" button if camera fails.

### Authentication Data

- User accounts stored locally in `users.json`
- Passwords encrypted with SHA256 hashing
- Session persists between app launches
- Click **Logout** to clear session

### Medical Disclaimer

**This is an AI-assisted preliminary analysis tool, NOT a medical diagnosis tool.**

- Always consult qualified healthcare professionals
- This tool provides visual guidance only
- Results should never replace professional medical evaluation
- Early consultation is recommended for any suspected abnormalities

## 📊 Example Diagnoses

### Healthy Skin
```
✅ Analysis Complete

✅ Severity: None
📊 Affected Area: 0.5%

📝 Diagnosis:
No significant skin abnormalities detected. Skin appears healthy.
Recommendation: Maintain regular skin care routine.
```

### Low Severity
```
✅ Analysis Complete

🟡 Severity: Low
📊 Affected Area: 2.3%

📝 Diagnosis:
Detected potential skin abnormalities. May include:
- Minor irregularities detected
- Slight redness or irritation
- Minor discoloration or small blemishes
Recommendation: Monitor and apply appropriate skincare.
```

### Medium Severity
```
✅ Analysis Complete

🟠 Severity: Medium
📊 Affected Area: 8.5%

📝 Diagnosis:
Detected moderate abnormalities. May include:
- Inflammation or visible redness
- Texture irregularities
- Visible lesions or rash patterns
Recommendation: Medical evaluation recommended. Please consult a dermatologist.
```

## 🔧 Troubleshooting

### Camera Not Working
- Check Windows privacy settings for camera access
- Ensure no other app is using the camera (Teams, Zoom, etc.)
- Try restarting the application
- Check if your webcam is properly connected

### "Unknown property transform" warnings
- These are safe PyQt6 CSS warnings
- App functions normally despite warnings
- Can be ignored

### Image Quality Issues
- Ensure adequate lighting
- Keep camera steady while capturing
- Maintain proper distance (distance indicator will guide)
- Use brightness/contrast sliders to optimize view
- Use a high-quality camera for best results

### Analysis Taking Too Long
- This is normal for first analysis (may take 5-10 seconds)
- Subsequent analyses are faster
- Close other CPU-intensive applications

### Cannot Sign In
- Verify email and password are correct
- Check that account was created successfully
- Clear app cache if issues persist

### Usage Limit Exceeded
- Upgrade to Pro for unlimited analyses
- Or create a new account for 15 more free analyses
- Payment gateway integration coming soon

### Python Module Not Found
```bash
# Reinstall dependencies
pip install -r desktop/requirements.txt --upgrade
```

## 📈 Future Enhancements

- [x] Authentication system
- [x] Single unified window interface
- [x] Interactive camera controls
- [x] Freemium monetization model
- [ ] Real payment gateway integration (Stripe/PayPal)
- [ ] Email verification for signups
- [ ] Password reset functionality
- [ ] Machine learning model integration with trained datasets
- [ ] Disease classification (eczema, psoriasis, acne, etc.)
- [ ] Report generation and PDF export
- [ ] Analysis history and comparison
- [ ] Multi-image batch processing
- [ ] Mobile app version
- [ ] Cloud-based analysis backend
- [ ] User profiles and medical history

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear descriptions

## 📝 License

This project is part of the FYP (Final Year Project) initiative.

## 👤 Author

Developed by Muskan - FYP1 Skin Disease Detection Project

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [Your contact information]

## 🔗 Links

- **GitHub Repository**: https://github.com/Muskan-zehra12/Skintelli
- **Project Specs**: See `/specs/` directory
- **Development History**: See `/history/` directory

---

**Last Updated**: January 13, 2026  
**Version**: 1.1.0  
**Status**: Active Development - Single Window UI with Authentication & Monetization
