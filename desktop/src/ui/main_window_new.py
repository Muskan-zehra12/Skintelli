"""
Main Window for Skintelli Application
Desktop GUI using PyQt6
"""

import sys
import logging
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QStackedWidget, QMessageBox, QTabWidget, QLineEdit, QTextEdit,
    QFileDialog, QProgressBar, QScrollArea, QTableWidget, QTableWidgetItem,
    QComboBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor, QIcon, QPixmap

from core.auth import AuthenticationService
from core.agent import AnalysisAgent
from database.models import AnalysisManager
from ui.widgets.dual_panel import DualPanelWidget

logger = logging.getLogger(__name__)


class AnalysisWorker(QThread):
    """Worker thread for analysis to prevent UI freezing"""
    
    progress = pyqtSignal(str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, agent: AnalysisAgent, image_path: str):
        super().__init__()
        self.agent = agent
        self.image_path = image_path
    
    def run(self):
        try:
            self.progress.emit("Starting analysis...")
            result = self.agent.analyze_image(self.image_path)
            
            if result:
                self.finished.emit(result)
            else:
                self.error.emit("Analysis failed. Please check the image and try again.")
                
        except Exception as e:
            self.error.emit(f"Error during analysis: {str(e)}")


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Skintelli - Intelligent Skin Disease Detection System")
        self.setMinimumSize(1400, 900)
        
        # Initialize services
        self.auth_service = AuthenticationService()
        self.analysis_agent = AnalysisAgent(use_mock_model=False)
        self.analysis_manager = AnalysisManager()
        
        self.current_user = None
        self.current_image_path = None
        self.analysis_worker = None
        
        # Create UI
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create screens
        self.login_screen = self.create_login_screen()
        self.analysis_screen = self.create_analysis_screen()
        self.history_screen = self.create_history_screen()
        
        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.login_screen)      # Index 0
        self.stacked_widget.addWidget(self.analysis_screen)   # Index 1
        self.stacked_widget.addWidget(self.history_screen)    # Index 2
        
        # Show login screen initially
        self.show_login_screen()
        
        logger.info("Main window initialized")
    
    def create_login_screen(self) -> QWidget:
        """Create login/signup screen"""
        screen = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Skintelli")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Intelligent Skin Disease Detection System")
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(30)
        
        # Login Tab
        self.auth_tabs = QTabWidget()
        
        # Login Tab
        login_tab = QWidget()
        login_layout = QVBoxLayout()
        
        login_layout.addWidget(QLabel("Username:"))
        self.login_username = QLineEdit()
        login_layout.addWidget(self.login_username)
        
        login_layout.addWidget(QLabel("Password:"))
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
        login_layout.addWidget(self.login_password)
        
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.handle_login)
        login_layout.addWidget(login_button)
        
        login_tab.setLayout(login_layout)
        self.auth_tabs.addTab(login_tab, "Login")
        
        # Signup Tab
        signup_tab = QWidget()
        signup_layout = QVBoxLayout()
        
        signup_layout.addWidget(QLabel("Username:"))
        self.signup_username = QLineEdit()
        signup_layout.addWidget(self.signup_username)
        
        signup_layout.addWidget(QLabel("Email:"))
        self.signup_email = QLineEdit()
        signup_layout.addWidget(self.signup_email)
        
        signup_layout.addWidget(QLabel("Password:"))
        self.signup_password = QLineEdit()
        self.signup_password.setEchoMode(QLineEdit.EchoMode.Password)
        signup_layout.addWidget(self.signup_password)
        
        signup_layout.addWidget(QLabel("Confirm Password:"))
        self.signup_confirm = QLineEdit()
        self.signup_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        signup_layout.addWidget(self.signup_confirm)
        
        signup_button = QPushButton("Sign Up")
        signup_button.clicked.connect(self.handle_signup)
        signup_layout.addWidget(signup_button)
        
        signup_tab.setLayout(signup_layout)
        self.auth_tabs.addTab(signup_tab, "Sign Up")
        
        layout.addWidget(self.auth_tabs)
        layout.addStretch()
        
        screen.setLayout(layout)
        return screen
    
    def create_analysis_screen(self) -> QWidget:
        """Create main analysis screen"""
        screen = QWidget()
        layout = QVBoxLayout()
        
        # Top bar with user info and navigation
        top_bar = QHBoxLayout()
        
        user_label = QLabel("User: ")
        self.user_display = QLabel("")
        top_bar.addWidget(user_label)
        top_bar.addWidget(self.user_display)
        top_bar.addStretch()
        
        # Instructions
        instruction_label = QLabel("📸 Upload a close-up image of a skin lesion (mole, spot, growth)")
        instruction_label.setStyleSheet("color: #FF6B35; font-weight: bold;")
        top_bar.addWidget(instruction_label)
        
        top_bar.addSpacing(20)
        
        history_btn = QPushButton("View History")
        history_btn.clicked.connect(self.show_history_screen)
        top_bar.addWidget(history_btn)
        
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.handle_logout)
        top_bar.addWidget(logout_btn)
        
        layout.addLayout(top_bar)
        layout.addSpacing(10)
        
        # Main analysis area - Removed left sidebar
        main_layout = QVBoxLayout()
        
        # Top section - Control buttons
        control_layout = QHBoxLayout()
        
        upload_btn = QPushButton("📁 Upload Image")
        upload_btn.setMinimumHeight(40)
        upload_btn.setMinimumWidth(200)
        upload_btn.clicked.connect(self.handle_upload_image)
        control_layout.addWidget(upload_btn)
        
        camera_btn = QPushButton("📷 Use Camera")
        camera_btn.setMinimumHeight(40)
        camera_btn.setMinimumWidth(200)
        camera_btn.clicked.connect(self.handle_camera_capture)
        control_layout.addWidget(camera_btn)
        
        control_layout.addStretch()
        
        self.analyze_btn = QPushButton("🔍 Analyze")
        self.analyze_btn.setMinimumHeight(40)
        self.analyze_btn.setMinimumWidth(200)
        self.analyze_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.analyze_btn.clicked.connect(self.handle_analyze)
        self.analyze_btn.setEnabled(False)
        control_layout.addWidget(self.analyze_btn)
        
        main_layout.addLayout(control_layout)
        main_layout.addSpacing(10)
        
        # Center section - Dual panel display (larger)
        self.dual_panel = DualPanelWidget()
        main_layout.addWidget(self.dual_panel, 1)
        
        layout.addLayout(main_layout, 1)
        
        # Bottom - Analysis result and explanation
        self.explanation_text = QTextEdit()
        self.explanation_text.setReadOnly(True)
        self.explanation_text.setMaximumHeight(200)
        layout.addWidget(QLabel("Diagnosis & Explanation:"))
        layout.addWidget(self.explanation_text)
        
        # Export button
        export_btn = QPushButton("Export Report as PDF")
        export_btn.clicked.connect(self.handle_export_pdf)
        layout.addWidget(export_btn)
        
        screen.setLayout(layout)
        return screen
    
    def create_history_screen(self) -> QWidget:
        """Create history viewing screen"""
        screen = QWidget()
        layout = QVBoxLayout()
        
        # Back button
        back_btn = QPushButton("Back to Analysis")
        back_btn.clicked.connect(self.show_analysis_screen)
        layout.addWidget(back_btn)
        
        # History table
        layout.addWidget(QLabel("Analysis History"))
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(
            ["Date", "Diagnosis", "Confidence", "Image", "View"]
        )
        layout.addWidget(self.history_table)
        
        screen.setLayout(layout)
        return screen
    
    def handle_login(self):
        """Handle login attempt"""
        username = self.login_username.text()
        password = self.login_password.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter username and password")
            return
        
        success, msg = self.auth_service.login(username, password)
        
        if success:
            self.current_user = username
            self.user_display.setText(username)
            self.login_username.clear()
            self.login_password.clear()
            self.show_analysis_screen()
            QMessageBox.information(self, "Success", f"Welcome, {username}!")
        else:
            QMessageBox.critical(self, "Login Failed", msg)
    
    def handle_signup(self):
        """Handle signup attempt"""
        username = self.signup_username.text()
        email = self.signup_email.text()
        password = self.signup_password.text()
        confirm = self.signup_confirm.text()
        
        if not username or not email or not password:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields")
            return
        
        if password != confirm:
            QMessageBox.warning(self, "Input Error", "Passwords do not match")
            return
        
        success, msg = self.auth_service.signup(username, password, email)
        
        if success:
            QMessageBox.information(self, "Success", f"Account created! Please login.")
            self.auth_tabs.setCurrentIndex(0)  # Switch to login tab
            self.signup_username.clear()
            self.signup_email.clear()
            self.signup_password.clear()
            self.signup_confirm.clear()
        else:
            QMessageBox.critical(self, "Signup Failed", msg)
    
    def handle_logout(self):
        """Handle logout"""
        self.auth_service.logout()
        self.current_user = None
        self.user_display.setText("")
        self.show_login_screen()
        QMessageBox.information(self, "Logout", "You have been logged out")
    
    def handle_upload_image(self):
        """Handle image upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.jpg *.jpeg *.png *.bmp)"
        )
        
        if file_path:
            self.current_image_path = file_path
            # Display image in dual panel
            self.dual_panel.set_original_image(file_path)
            self.analyze_btn.setEnabled(True)
            QMessageBox.information(self, "Image Loaded", "Image loaded! Click 'Analyze' to run detection.")
    
    def handle_camera_capture(self):
        """Handle camera capture"""
        QMessageBox.information(self, "Camera Capture", "Camera capture feature coming soon! Please use 'Upload Image' for now.")
    
    def handle_analyze(self):
        """Handle analyze button click"""
        if not hasattr(self, 'current_image_path'):
            QMessageBox.warning(self, "No Image", "Please upload an image first!")
            return
        
        self.analyze_image(self.current_image_path)
    
    def analyze_image(self, image_path: str):
        """Analyze image"""
        # Show progress
        QMessageBox.information(self, "Analysis Started", "Analyzing image... This may take 10-15 seconds.")
        
        # Create and start worker thread
        self.analysis_worker = AnalysisWorker(self.analysis_agent, image_path)
        self.analysis_worker.progress.connect(self.on_analysis_progress)
        self.analysis_worker.finished.connect(self.on_analysis_finished)
        self.analysis_worker.error.connect(self.on_analysis_error)
        self.analysis_worker.start()
    
    def on_analysis_progress(self, message: str):
        """Update progress during analysis"""
        logger.info(f"Progress: {message}")
    
    def on_analysis_finished(self, result: dict):
        """Handle analysis completion"""
        # Display results
        diagnosis = result['detection']['diagnosis']
        confidence = result['detection']['confidence']
        class_probs = result['detection']['class_probabilities']
        explanation = result['explanation']
        heatmap_path = result['explainability']['heatmap_path']
        overlay_path = result['explainability']['overlay_path']
        
        # Display heatmap
        if heatmap_path and Path(heatmap_path).exists():
            pixmap = QPixmap(str(heatmap_path))
            if not pixmap.isNull():
                self.dual_panel.analysis_image_label.setPixmap(
                    pixmap.scaled(
                        self.dual_panel.analysis_image_label.size(),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                )
        
        # Format diagnosis with all class probabilities
        prob_lines = [f"  • {cls}: {prob*100:.1f}%" for cls, prob in sorted(class_probs.items(), key=lambda x: x[1], reverse=True)]
        prob_text = "\n".join(prob_lines)
        
        diagnosis_display = (
            f"✅ Analysis Complete\n\n"
            f"🔬 Diagnosis: {diagnosis}\n"
            f"📊 Confidence: {confidence*100:.1f}%\n\n"
            f"📈 Class Probabilities:\n{prob_text}\n\n"
            f"📝 {explanation}"
        )
        
        if hasattr(self.dual_panel, 'explanation_label'):
            self.dual_panel.explanation_label.setText(diagnosis_display)
            self.dual_panel.explanation_label.setStyleSheet("""
                QLabel {
                    padding: 15px;
                    background-color: #d5f4e6;
                    border-radius: 6px;
                    border-left: 4px solid #27ae60;
                    color: #333;
                    font-size: 11px;
                    line-height: 1.6;
                }
            """)
        
        # Also show in main explanation area
        self.explanation_text.setText(explanation)
        
        # Save to database
        if self.current_user:
            success, analysis_id = self.analysis_manager.save_analysis(
                self.current_user,
                result['input_image_path'],
                diagnosis,
                confidence,
                heatmap_path,
                explanation
            )
            
            if success:
                logger.info(f"Analysis saved (ID: {analysis_id})")
        
        QMessageBox.information(self, "Analysis Complete", f"Diagnosis: {diagnosis}\nConfidence: {confidence*100:.1f}%")
    
    def on_analysis_error(self, error_msg: str):
        """Handle analysis error"""
        logger.error(f"Analysis error: {error_msg}")
        QMessageBox.critical(self, "Analysis Error", error_msg)
    
    def handle_export_pdf(self):
        """Export analysis result as PDF"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Report as PDF", "", "PDF Files (*.pdf)"
        )
        
        if file_path:
            QMessageBox.information(self, "Export", f"Report saved to {file_path}")
    
    def show_login_screen(self):
        """Show login screen"""
        self.stacked_widget.setCurrentIndex(0)
    
    def show_analysis_screen(self):
        """Show analysis screen"""
        self.stacked_widget.setCurrentIndex(1)
    
    def show_history_screen(self):
        """Show history screen and load user's analyses"""
        if self.current_user:
            analyses = self.analysis_manager.get_user_analyses(self.current_user)
            self.refresh_history_table(analyses)
        
        self.stacked_widget.setCurrentIndex(2)
    
    def refresh_history_table(self, analyses: list):
        """Refresh history table with analyses"""
        self.history_table.setRowCount(0)
        
        for analysis in analyses:
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)
            
            timestamp = analysis.get('timestamp', 'N/A')
            diagnosis = analysis.get('diagnosis', 'N/A')
            confidence = analysis.get('confidence', 0)
            
            self.history_table.setItem(row, 0, QTableWidgetItem(timestamp))
            self.history_table.setItem(row, 1, QTableWidgetItem(diagnosis))
            self.history_table.setItem(row, 2, QTableWidgetItem(f"{confidence:.1%}"))
            self.history_table.setItem(row, 3, QTableWidgetItem(analysis.get('input_image_path', 'N/A')))


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    
    logging.basicConfig(level=logging.INFO)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
