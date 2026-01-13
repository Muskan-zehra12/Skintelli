import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QStackedWidget, QMessageBox, QTabWidget, QLineEdit, QTextEdit, 
                             QGridLayout, QCheckBox, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from ui.widgets.dual_panel import DualPanelWidget
from core.auth import UserManager
from core.usage_tracker import GuestUsageTracker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Skintelli - Intelligent Skin Disease Detection")
        self.setMinimumSize(1200, 800)
        
        # Initialize auth and usage tracking
        self.user_manager = UserManager()
        self.guest_tracker = GuestUsageTracker()
        self.is_guest = False
        
        # Central Widget and Main Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Main Stacked Widget (screens)
        self.main_stack = QStackedWidget()
        self.main_layout.addWidget(self.main_stack)
        
        # Create all screens
        self.auth_screen = self.create_auth_screen()
        self.analysis_screen = self.create_analysis_screen()
        self.paywall_screen = self.create_paywall_screen()
        
        # Add screens to stack
        self.main_stack.addWidget(self.auth_screen)      # Index 0
        self.main_stack.addWidget(self.analysis_screen)   # Index 1
        self.main_stack.addWidget(self.paywall_screen)    # Index 2
        
        # Show appropriate screen on startup
        if self.user_manager.is_logged_in():
            self.show_analysis_screen()
        else:
            self.show_auth_screen()
        
        # Status Bar
        self.statusBar().showMessage("Ready")
    
    def create_auth_screen(self) -> QWidget:
        """Create authentication screen with signup/signin tabs."""
        auth_widget = QWidget()
        layout = QVBoxLayout(auth_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("Skintelli")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Intelligent Skin Disease Detection")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Tab Widget
        self.auth_tabs = QTabWidget()
        
        # Sign In Tab
        signin_widget = self.create_signin_tab()
        self.auth_tabs.addTab(signin_widget, "Sign In")
        
        # Sign Up Tab
        signup_widget = self.create_signup_tab()
        self.auth_tabs.addTab(signup_widget, "Sign Up")
        
        layout.addWidget(self.auth_tabs)
        
        # Guest Button
        guest_btn = QPushButton("Continue as Guest (3 free attempts)")
        guest_btn.setMinimumHeight(40)
        guest_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        guest_btn.clicked.connect(self.handle_guest_login)
        layout.addWidget(guest_btn)
        
        return auth_widget
    
    def create_signin_tab(self) -> QWidget:
        """Create sign in tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Email
        email_label = QLabel("📧 Email:")
        email_label.setStyleSheet("font-weight: bold; color: #333;")
        self.signin_email = QLineEdit()
        self.signin_email.setPlaceholderText("your@email.com")
        self.signin_email.setMinimumHeight(40)
        self.signin_email.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 6px;
                padding: 8px;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: #f0f8ff;
            }
        """)
        layout.addWidget(email_label)
        layout.addWidget(self.signin_email)
        
        # Password
        password_label = QLabel("🔐 Password:")
        password_label.setStyleSheet("font-weight: bold; color: #333;")
        self.signin_password = QLineEdit()
        self.signin_password.setPlaceholderText("Enter your password")
        self.signin_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.signin_password.setMinimumHeight(40)
        self.signin_password.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 6px;
                padding: 8px;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: #f0f8ff;
            }
        """)
        layout.addWidget(password_label)
        layout.addWidget(self.signin_password)
        
        layout.addSpacing(10)
        
        # Sign In Button
        signin_btn = QPushButton("🔓 Sign In")
        signin_btn.setMinimumHeight(45)
        signin_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1e5a7a;
            }
        """)
        signin_btn.clicked.connect(self.handle_signin)
        layout.addWidget(signin_btn)
        
        layout.addStretch()
        return widget
    
    def create_signup_tab(self) -> QWidget:
        """Create sign up tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Full Name
        name_label = QLabel("👤 Full Name:")
        name_label.setStyleSheet("font-weight: bold; color: #333;")
        self.signup_name = QLineEdit()
        self.signup_name.setPlaceholderText("Your full name")
        self.signup_name.setMinimumHeight(40)
        self.signup_name.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 6px;
                padding: 8px;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 2px solid #27ae60;
                background-color: #f0fff4;
            }
        """)
        layout.addWidget(name_label)
        layout.addWidget(self.signup_name)
        
        # Email
        email_label = QLabel("📧 Email:")
        email_label.setStyleSheet("font-weight: bold; color: #333;")
        self.signup_email = QLineEdit()
        self.signup_email.setPlaceholderText("your@email.com")
        self.signup_email.setMinimumHeight(40)
        self.signup_email.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 6px;
                padding: 8px;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 2px solid #27ae60;
                background-color: #f0fff4;
            }
        """)
        layout.addWidget(email_label)
        layout.addWidget(self.signup_email)
        
        # Password
        password_label = QLabel("🔐 Password:")
        password_label.setStyleSheet("font-weight: bold; color: #333;")
        self.signup_password = QLineEdit()
        self.signup_password.setPlaceholderText("Create a password (min. 6 chars)")
        self.signup_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.signup_password.setMinimumHeight(40)
        self.signup_password.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 6px;
                padding: 8px;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 2px solid #27ae60;
                background-color: #f0fff4;
            }
        """)
        layout.addWidget(password_label)
        layout.addWidget(self.signup_password)
        
        # Confirm Password
        confirm_label = QLabel("🔐 Confirm Password:")
        confirm_label.setStyleSheet("font-weight: bold; color: #333;")
        self.signup_confirm = QLineEdit()
        self.signup_confirm.setPlaceholderText("Confirm password")
        self.signup_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.signup_confirm.setMinimumHeight(40)
        self.signup_confirm.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 6px;
                padding: 8px;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 2px solid #27ae60;
                background-color: #f0fff4;
            }
        """)
        layout.addWidget(confirm_label)
        layout.addWidget(self.signup_confirm)
        
        layout.addSpacing(10)
        
        # Sign Up Button
        signup_btn = QPushButton("✨ Create Account")
        signup_btn.setMinimumHeight(45)
        signup_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e5a7a;
            }
        """)
        signup_btn.clicked.connect(self.handle_signup)
        layout.addWidget(signup_btn)
        
        layout.addStretch()
        return widget
    
    def create_analysis_screen(self) -> QWidget:
        """Create analysis screen with camera and results."""
        analysis_widget = QWidget()
        layout = QVBoxLayout(analysis_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header with user info
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 10, 15, 10)
        
        self.user_label = QLabel(self.get_user_display_text())
        self.user_label.setStyleSheet("font-weight: bold; color: #333; font-size: 12px;")
        header_layout.addWidget(self.user_label)
        
        header_layout.addStretch()
        
        self.btn_logout = QPushButton("Logout")
        self.btn_logout.setMaximumWidth(100)
        self.btn_logout.clicked.connect(self.handle_logout)
        header_layout.addWidget(self.btn_logout)
        
        layout.addWidget(header)
        
        # Dual Panel (Camera + Analysis)
        self.analysis_view = DualPanelWidget(self)
        layout.addWidget(self.analysis_view)
        
        return analysis_widget
    
    def create_paywall_screen(self) -> QWidget:
        """Create paywall screen for upgrade."""
        paywall_widget = QWidget()
        layout = QVBoxLayout(paywall_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("Upgrade to Pro")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # Features Grid
        features_layout = QGridLayout()
        
        free_features = [
            ("Free Tier", ["3 guest attempts", "15 analyses/month", "Basic detection"])
        ]
        
        pro_features = [
            ("Pro Tier - Unlock Now", [
                "✓ Unlimited analyses",
                "✓ Priority support",
                "✓ Advanced detection",
                "✓ Export reports",
                "✓ History tracking"
            ])
        ]
        
        # Free column
        free_title = QLabel("Free Tier")
        free_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        features_layout.addWidget(free_title, 0, 0)
        
        free_text = QLabel("\n".join([
            "• 15 analyses per month",
            "• Basic skin detection",
            "• Standard quality"
        ]))
        features_layout.addWidget(free_text, 1, 0)
        
        # Pro column
        pro_title = QLabel("Pro Tier")
        pro_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        pro_title.setStyleSheet("color: #27ae60;")
        features_layout.addWidget(pro_title, 0, 1)
        
        pro_text = QLabel("\n".join([
            "• Unlimited analyses",
            "• Advanced detection",
            "• Priority support",
            "• Export reports",
            "• History tracking"
        ]))
        features_layout.addWidget(pro_text, 1, 1)
        
        layout.addLayout(features_layout)
        layout.addSpacing(20)
        
        # Pricing
        pricing_layout = QHBoxLayout()
        pricing_layout.addStretch()
        
        monthly = QLabel("$4.99/month")
        monthly.setFont(QFont("Arial", 12))
        pricing_layout.addWidget(monthly)
        
        pricing_layout.addSpacing(30)
        
        yearly = QLabel("$39.99/year")
        yearly.setFont(QFont("Arial", 12))
        pricing_layout.addWidget(yearly)
        
        pricing_layout.addStretch()
        layout.addLayout(pricing_layout)
        
        layout.addSpacing(20)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        upgrade_btn = QPushButton("Upgrade to Pro")
        upgrade_btn.setMinimumWidth(150)
        upgrade_btn.setMinimumHeight(40)
        upgrade_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        upgrade_btn.clicked.connect(self.handle_upgrade)
        button_layout.addWidget(upgrade_btn)
        
        button_layout.addSpacing(10)
        
        maybe_btn = QPushButton("Maybe Later")
        maybe_btn.setMinimumWidth(150)
        maybe_btn.setMinimumHeight(40)
        maybe_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        maybe_btn.clicked.connect(self.show_analysis_screen)
        button_layout.addWidget(maybe_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        layout.addStretch()
        
        return paywall_widget
    
    def show_auth_screen(self):
        """Switch to authentication screen."""
        self.main_stack.setCurrentIndex(0)
    
    def show_analysis_screen(self):
        """Switch to analysis screen."""
        self.main_stack.setCurrentIndex(1)
        self.update_user_display()
    
    def show_paywall_screen(self):
        """Switch to paywall screen."""
        self.main_stack.setCurrentIndex(2)
    
    def handle_signin(self):
        """Handle sign in button."""
        email = self.signin_email.text().strip()
        password = self.signin_password.text()
        
        if not email or not password:
            QMessageBox.warning(self, "Validation Error", "Please enter email and password.")
            return
        
        success, msg = self.user_manager.login(email, password)
        if success:
            QMessageBox.information(self, "Success", "Logged in successfully!")
            self.signin_email.clear()
            self.signin_password.clear()
            self.show_analysis_screen()
        else:
            QMessageBox.warning(self, "Login Failed", msg)
    
    def handle_signup(self):
        """Handle sign up button."""
        name = self.signup_name.text().strip()
        email = self.signup_email.text().strip()
        password = self.signup_password.text()
        confirm = self.signup_confirm.text()
        
        if not name or not email or not password:
            QMessageBox.warning(self, "Validation Error", "Please fill in all fields.")
            return
        
        if password != confirm:
            QMessageBox.warning(self, "Validation Error", "Passwords do not match.")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Validation Error", "Password must be at least 6 characters.")
            return
        
        success, msg = self.user_manager.signup(email, password, name)
        if success:
            QMessageBox.information(self, "Success", "Account created! Please sign in.")
            self.signup_name.clear()
            self.signup_email.clear()
            self.signup_password.clear()
            self.signup_confirm.clear()
            self.auth_tabs.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Signup Failed", msg)
    
    def handle_guest_login(self):
        """Handle guest login."""
        self.is_guest = True
        self.show_analysis_screen()
    
    def handle_upgrade(self):
        """Handle upgrade button."""
        # TODO: Integrate with Stripe/PayPal
        QMessageBox.information(
            self,
            "Upgrade",
            "Payment gateway integration coming soon!\n\n"
            "For now, please contact support to upgrade to Pro."
        )
    
    def handle_logout(self):
        """Handle logout button."""
        self.user_manager.logout()
        self.is_guest = False
        self.analysis_view.reset_ui()
        self.show_auth_screen()
    
    def get_user_display_text(self) -> str:
        """Get user display text for header."""
        if self.user_manager.is_logged_in():
            user = self.user_manager.get_current_user()
            return (f"👤 {user['full_name']} | "
                   f"Tier: {user['tier'].upper()} | "
                   f"Analyses: {user['analyses_used']}/{user['max_analyses']}")
        else:
            remaining = self.guest_tracker.get_remaining_attempts()
            return f"👤 Guest User | Attempts Remaining: {remaining}/3"
    
    def update_user_display(self):
        """Update user info display."""
        if hasattr(self, 'user_label'):
            self.user_label.setText(self.get_user_display_text())
    
    def check_usage_limit(self) -> bool:
        """Check if user can perform analysis."""
        if self.user_manager.is_logged_in():
            user = self.user_manager.get_current_user()
            if user['tier'] == 'free':
                if user['analyses_used'] >= user['max_analyses']:
                    self.show_paywall_screen()
                    return False
            return True
        else:
            # Guest user
            if self.guest_tracker.is_limit_reached():
                QMessageBox.warning(
                    self,
                    "Guest Limit Reached",
                    "You've used all 3 free guest attempts.\n\n"
                    "Sign up for a free account to get 15 analyses!"
                )
                self.show_auth_screen()
                return False
            return True
    
    def record_analysis_usage(self):
        """Record that user performed an analysis."""
        if self.user_manager.is_logged_in():
            allowed, msg = self.user_manager.increment_usage()
            if not allowed:
                self.show_paywall_screen()
            else:
                remaining = self.user_manager.get_current_user()['max_analyses'] - self.user_manager.get_current_user()['analyses_used']
                if remaining <= 0 and self.user_manager.get_current_user()['tier'] == 'free':
                    self.show_paywall_screen()
                else:
                    self.statusBar().showMessage(msg)
        else:
            allowed, msg = self.guest_tracker.attempt_analysis()
            self.statusBar().showMessage(msg)
            if self.guest_tracker.is_limit_reached():
                QMessageBox.information(
                    self,
                    "Sign Up for More",
                    "You've used all 3 free attempts.\n\n"
                    "Sign up now to get 15 free analyses!"
                )
                self.show_auth_screen()
        
        self.update_user_display()


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
