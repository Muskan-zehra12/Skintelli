# Changelog

All notable changes to the Skintelli project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-15

### Added
- **Single-Window Interface**: Complete UI refactor with unified window design
  - Authentication screen with Sign In/Sign Up tabs integrated directly
  - Seamless screen transitions (Auth → Analysis → Paywall)
  - No more popup dialogs - everything in one cohesive window
  
- **Complete Authentication System**
  - User registration with email validation and SHA256 password hashing
  - Persistent session management with JSON-based storage
  - Guest mode with 3 free analysis attempts per session
  - Logout functionality with session cleanup
  
- **Freemium Monetization Model**
  - Guest tier: 3 analyses per session (no account required)
  - Free tier: 15 analyses per month for registered users
  - Pro tier: Unlimited analyses (paywall ready for payment gateway)
  - Usage tracking and limit enforcement across all features
  
- **Interactive Camera Controls**
  - Real-time brightness adjustment slider (-50 to +50)
  - Real-time contrast adjustment slider (-50 to +50)
  - Live preview of adjustments while camera is active
  - Camera controls appear/disappear based on camera state
  
- **Enhanced Visual Design**
  - Emoji indicators on all buttons (📁📷📸🔬🔐✨)
  - Color-coded input fields with focus effects
  - Severity indicators with emojis (✅🟡🟠🔴)
  - Professional button styling with hover states
  - Improved panel borders and rounded corners
  - Better spacing and padding throughout UI
  
- **Live Analysis Feedback**
  - Loading indicators during image analysis
  - Progress messages with animated text
  - Severity-based color coding for results
  - Detailed file information display on upload
  - Real-time status updates in status bar
  
- **New Core Modules**
  - `core/auth.py` - UserManager class for authentication
  - `core/usage_tracker.py` - GuestUsageTracker for attempt tracking
  - `ui/dialogs.py` - AuthDialog and PaywallDialog components
  - `users.json` - Local user database with encrypted passwords

### Changed
- **Main Window Architecture**: Complete refactor from dialog-based to screen-based navigation
- **UI Components**: All buttons now have enhanced styling and emoji icons
- **Analysis Display**: Results now show severity level with color-coded formatting
- **Camera Distance Indicator**: Enhanced with better color coding and styling
- **Requirements**: Simplified to core dependencies (PyQt6, OpenCV, NumPy)
- **Project Metadata**: Updated pyproject.toml to reflect current state

### Improved
- **User Experience**: Seamless navigation without context switching
- **Visual Feedback**: Better loading states and progress indicators
- **Error Messages**: More descriptive and helpful error dialogs
- **Documentation**: Comprehensive README update with all new features
- **Code Organization**: Better separation of concerns with new modules

### Technical
- Window resizable with minimum size of 1200x800
- Session persistence between app launches
- Automatic usage tracking per user tier
- Password encryption with SHA256 hashing
- JSON-based user data storage

## [1.0.0] - 2026-01-13

### Added
- **Live Camera Capture**
  - HD 1920x1080 resolution capture
  - Distance indicator with real-time feedback (Too Far/Near/Fit)
  - ROI (Region of Interest) guide box
  - One-click image capture
  
- **Intelligent Skin Analysis Engine**
  - Multi-feature detection:
    - Redness detection for inflammation and wounds
    - Dark spot detection for bruising and hyperpigmentation
    - Light spot detection for scars and depigmentation
    - Texture analysis for rashes and irregularities
  - Severity calculation (None/Low/Medium/High)
  - Affected area percentage calculation
  
- **Visual Heatmap Output**
  - Color-coded visualization with red/yellow problem areas
  - Green contour outlines around affected regions
  - Overlay blending with original image
  
- **Dual-Panel Interface**
  - Left panel: Original captured/uploaded image
  - Right panel: Analysis heatmap visualization
  - Bottom section: Detailed diagnosis and recommendations
  
- **Image Input Methods**
  - Upload images (JPG, PNG, JPEG formats)
  - Live camera capture with preview
  
- **Core Modules**
  - `core/skin_analyzer.py` - AI analysis engine
  - `ui/main_window.py` - Main application window
  - `ui/widgets/dual_panel.py` - Image capture and display
  
- **Documentation**
  - Comprehensive README with installation guide
  - Usage instructions with screenshots references
  - Technical explanation of analysis process
  - Troubleshooting section

### Technical
- Python 3.11+ support
- PyQt6 for cross-platform GUI
- OpenCV for image processing and camera
- NumPy for numerical computations
- Natural HD image quality without artificial enhancement

## [0.1.0] - 2026-01-12

### Added
- Initial project setup
- Project structure with specs and documentation
- GitHub repository initialization
- Basic requirements file

---

## Legend
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security vulnerability fixes
- **Improved**: Enhancements to existing features
- **Technical**: Technical details and infrastructure changes
