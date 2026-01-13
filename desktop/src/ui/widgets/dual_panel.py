from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QFileDialog, QFrame, QMessageBox, QApplication
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QTimer
import numpy as np

class DualPanelWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.cap = None
        self.timer = None
        self.current_image = None  # Store captured image for analysis
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Controls Layout
        controls_layout = QHBoxLayout()
        self.upload_btn = QPushButton("Upload Image")
        self.camera_btn = QPushButton("Use Camera")
        self.capture_btn = QPushButton("Capture Image")
        self.capture_btn.setEnabled(False)
        self.analyze_btn = QPushButton("Analyze")
        self.analyze_btn.setEnabled(False)
        
        controls_layout.addWidget(self.upload_btn)
        controls_layout.addWidget(self.camera_btn)
        controls_layout.addWidget(self.capture_btn)
        controls_layout.addStretch()
        controls_layout.addWidget(self.analyze_btn)

        self.distance_label = QLabel("Distance: —")
        self.distance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.distance_label.setStyleSheet("padding:4px; border-radius:4px; background:#eee; color:#333;")
        controls_layout.addWidget(self.distance_label)
        
        layout.addLayout(controls_layout)

        # Panels Layout
        panels_layout = QHBoxLayout()
        
        # Left Panel - Original Image
        self.left_panel = QFrame()
        self.left_panel.setFrameShape(QFrame.Shape.StyledPanel)
        left_layout = QVBoxLayout(self.left_panel)
        left_layout.addWidget(QLabel("Original Image"))
        self.original_image_label = QLabel("No image loaded")
        self.original_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_image_label.setMinimumSize(640, 480)
        self.original_image_label.setScaledContents(False)
        left_layout.addWidget(self.original_image_label)
        
        # Right Panel - Analysis/Heatmap
        self.right_panel = QFrame()
        self.right_panel.setFrameShape(QFrame.Shape.StyledPanel)
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.addWidget(QLabel("AI Analysis (Heatmap)"))
        self.analysis_image_label = QLabel("Waiting for analysis...")
        self.analysis_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.analysis_image_label.setMinimumSize(640, 480)
        self.analysis_image_label.setScaledContents(False)
        right_layout.addWidget(self.analysis_image_label)

        panels_layout.addWidget(self.left_panel)
        panels_layout.addWidget(self.right_panel)
        
        layout.addLayout(panels_layout)

        # Explanation Area
        self.explanation_label = QLabel("Diagnosis and explanation will appear here.")
        self.explanation_label.setWordWrap(True)
        self.explanation_label.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(self.explanation_label)

        # Connect signals
        self.upload_btn.clicked.connect(self.load_image)
        self.camera_btn.clicked.connect(self.toggle_camera)
        self.capture_btn.clicked.connect(self.capture_image)
        self.analyze_btn.clicked.connect(self.analyze_skin)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            import cv2
            # Load image using OpenCV to store for analysis
            self.current_image = cv2.imread(file_path)
            if self.current_image is None:
                QMessageBox.warning(self, "Error", "Failed to load image.")
                return
            
            # Enhance image quality
            self.current_image = self._enhance_image(self.current_image)
            
            # Convert to QPixmap for display
            rgb = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            qimg = QImage(rgb.data, w, h, w * ch, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            scaled_pixmap = pixmap.scaled(self.original_image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.original_image_label.setPixmap(scaled_pixmap)
            self.analyze_btn.setEnabled(True)
            self.explanation_label.setText(f"Loaded: {file_path}\nReady for analysis. Click 'Analyze' button.")
            
            # Reset analysis panel
            self.analysis_image_label.setText("Waiting for analysis...")
            self.analysis_image_label.setPixmap(QPixmap())

    def toggle_camera(self):
        try:
            import cv2
        except Exception:
            QMessageBox.warning(
                self,
                "OpenCV Not Installed",
                "Camera requires OpenCV. Please install it with:\n\npython -m pip install opencv-python"
            )
            return

        if self.cap is None:
            try:
                self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                if not self.cap.isOpened():
                    raise RuntimeError("Camera not accessible")
                
                # Set high resolution for better quality
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
                self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
                self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
                
                if self.timer is None:
                    self.timer = QTimer(self)
                    self.timer.timeout.connect(self._update_frame)
                self.timer.start(33)
                self.camera_btn.setText("Stop Camera")
                self.capture_btn.setEnabled(True)
                self.explanation_label.setText("Live camera started. Adjust distance until indicator shows 'Fit'.")
            except Exception as e:
                self._show_camera_error(e)
        else:
            self.timer.stop() if self.timer else None
            try:
                self.cap.release()
            except Exception:
                pass
            self.cap = None
            self.camera_btn.setText("Use Camera")
            self.capture_btn.setEnabled(False)
            self.distance_label.setText("Distance: —")
            self.distance_label.setStyleSheet("padding:4px; border-radius:4px; background:#eee; color:#333;")
            self.explanation_label.setText("Camera stopped.")

    def _update_frame(self):
        import cv2
        if self.cap is None:
            return
        ok, frame = self.cap.read()
        if not ok or frame is None:
            return
        h, w = frame.shape[:2]
        roi_w, roi_h = int(w * 0.6), int(h * 0.6)
        roi_x = (w - roi_w) // 2
        roi_y = (h - roi_h) // 2
        
        # Extract ROI for analysis
        roi = frame[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]
        
        # Analyze ROI content to determine distance
        status, color = self._analyze_roi_distance(roi)
        
        # Draw ROI guide and status
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), color, 2)
        cv2.putText(frame, f"{status}", (roi_x + 10, roi_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA)
        self._set_distance_indicator(status)
        
        # Display frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        qimg = QImage(frame_rgb.data, w, h, w * 3, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        # Use high-quality scaling
        scaled_pixmap = pixmap.scaled(
            self.original_image_label.size(), 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        )
        self.original_image_label.setPixmap(scaled_pixmap)
    
    def _analyze_roi_distance(self, roi):
        """Analyze ROI content to determine if subject is at proper distance."""
        import cv2
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            
            # Calculate edge density using Canny
            edges = cv2.Canny(gray, 50, 150)
            edge_density = (edges > 0).sum() / edges.size
            
            # Calculate brightness variance to detect presence of subject
            variance = gray.var()
            mean_brightness = gray.mean()
            
            # Check if there's meaningful content in ROI
            if edge_density < 0.02 or variance < 200:
                return "No Subject", (255, 255, 0)
            
            # Estimate distance based on edge density and brightness
            # Higher edge density typically means subject is closer (more detail visible)
            # We want moderate edge density for optimal examination
            
            if edge_density < 0.05:
                return "Too Far", (0, 0, 255)
            elif edge_density > 0.20:
                return "Too Near", (255, 0, 0)
            else:
                return "Fit", (0, 200, 0)
                
        except Exception:
            return "Adjust", (255, 255, 0)

    def capture_image(self):
        import cv2
        if self.cap is None:
            QMessageBox.information(self, "Camera", "Start the camera first.")
            return
        ok, frame = self.cap.read()
        if not ok or frame is None:
            QMessageBox.warning(self, "Camera", "Failed to capture frame.")
            return
        h, w = frame.shape[:2]
        roi_w, roi_h = int(w * 0.6), int(h * 0.6)
        roi_x = (w - roi_w) // 2
        roi_y = (h - roi_h) // 2
        crop = frame[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]
        
        # Enhance captured image quality
        crop = self._enhance_image(crop)
        
        # Store cropped image for analysis
        self.current_image = crop.copy()
        
        frame_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
        ch = frame_rgb.shape[2]
        qimg = QImage(frame_rgb.data, crop.shape[1], crop.shape[0], crop.shape[1] * ch, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        scaled_pixmap = pixmap.scaled(self.original_image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.original_image_label.setPixmap(scaled_pixmap)
        self.analyze_btn.setEnabled(True)
        self.explanation_label.setText("Captured ROI from camera.\nReady for analysis. Click 'Analyze' button.")
        self.toggle_camera()
        
        # Reset analysis panel
        self.analysis_image_label.setText("Waiting for analysis...")
        self.analysis_image_label.setPixmap(QPixmap())

    def _set_distance_indicator(self, status: str):
        if status == "Fit":
            self.distance_label.setText("Distance: Fit")
            self.distance_label.setStyleSheet("padding:4px; border-radius:4px; background:#d4edda; color:#155724;")
        elif status == "Too Near":
            self.distance_label.setText("Distance: Too Near")
            self.distance_label.setStyleSheet("padding:4px; border-radius:4px; background:#f8d7da; color:#721c24;")
        elif status == "Too Far":
            self.distance_label.setText("Distance: Too Far")
            self.distance_label.setStyleSheet("padding:4px; border-radius:4px; background:#fff3cd; color:#856404;")
        elif status == "No Subject":
            self.distance_label.setText("Distance: No Subject")
            self.distance_label.setStyleSheet("padding:4px; border-radius:4px; background:#e2e3e5; color:#383d41;")
        else:
            self.distance_label.setText("Distance: Adjust")
            self.distance_label.setStyleSheet("padding:4px; border-radius:4px; background:#eee; color:#333;")

    def _show_camera_error(self, e: Exception):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Camera Access Error")
        msg.setText(
            "Could not access the camera.\n\n"
            "On Windows, ensure: Settings > Privacy & security > Camera >\n"
            "- 'Camera access' is On\n- 'Let desktop apps access your camera' is On\n"
            "Also, close other apps using the camera and try again.\n\n"
            f"Details: {e}"
        )
        open_settings_btn = msg.addButton("Open Camera Settings", QMessageBox.ButtonRole.ActionRole)
        msg.addButton(QMessageBox.StandardButton.Ok)
        msg.exec()
        if msg.clickedButton() is open_settings_btn:
            try:
                import os
                os.startfile("ms-settings:privacy-webcam")
            except Exception:
                pass
    
    def _enhance_image(self, image):
        """Return image as-is without any processing for natural HD capture."""
        return image
    
    def analyze_skin(self):
        """Analyze captured/loaded image for skin abnormalities."""
        if self.current_image is None:
            QMessageBox.warning(self, "No Image", "Please capture or load an image first.")
            return
        
        try:
            from core.skin_analyzer import SkinAnalyzer
            import cv2
            
            # Show processing message
            self.explanation_label.setText("🔄 Analyzing image... Please wait.")
            self.analyze_btn.setEnabled(False)
            
            # Force UI update
            QApplication.processEvents()
            
            # Perform analysis
            analyzer = SkinAnalyzer()
            results = analyzer.analyze_image(self.current_image)
            
            # Display heatmap in right panel
            heatmap = results['heatmap']
            heatmap_rgb = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
            h, w, ch = heatmap_rgb.shape
            qimg = QImage(heatmap_rgb.data, w, h, w * ch, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            # Use high-quality scaling
            scaled_pixmap = pixmap.scaled(
                self.analysis_image_label.size(), 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.analysis_image_label.setPixmap(scaled_pixmap)
            
            # Display diagnosis
            diagnosis_text = f"📊 Analysis Complete\n\n{results['diagnosis']}"
            self.explanation_label.setText(diagnosis_text)
            
            # Re-enable analyze button
            self.analyze_btn.setEnabled(True)
            
        except ImportError as e:
            QMessageBox.critical(self, "Error", f"Failed to load analyzer module:\n{e}")
            self.analyze_btn.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Analysis Error", f"An error occurred during analysis:\n{e}")
            self.explanation_label.setText("❌ Analysis failed. Please try again.")
            self.analyze_btn.setEnabled(True)