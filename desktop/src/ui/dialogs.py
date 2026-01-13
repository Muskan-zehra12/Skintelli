"""
Login and Authentication UI Dialogs
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QTabWidget, QWidget, QMessageBox)
from PyQt6.QtCore import Qt


class AuthDialog(QDialog):
    """Dialog for user authentication (signup/signin)."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Skintelli - Sign In / Sign Up")
        self.setMinimumWidth(400)
        self.result_data = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Skintelli Authentication")
        title_font = title.font()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Tabs for Sign In and Sign Up
        tabs = QTabWidget()
        
        # Sign In Tab
        signin_tab = QWidget()
        signin_layout = QVBoxLayout(signin_tab)
        
        signin_layout.addWidget(QLabel("Email:"))
        self.signin_email = QLineEdit()
        signin_layout.addWidget(self.signin_email)
        
        signin_layout.addWidget(QLabel("Password:"))
        self.signin_password = QLineEdit()
        self.signin_password.setEchoMode(QLineEdit.EchoMode.Password)
        signin_layout.addWidget(self.signin_password)
        
        signin_btn = QPushButton("Sign In")
        signin_btn.clicked.connect(self.handle_signin)
        signin_layout.addWidget(signin_btn)
        
        signin_layout.addWidget(QLabel(
            "New user? Go to Sign Up tab to create an account."
        ))
        signin_layout.addStretch()
        
        # Sign Up Tab
        signup_tab = QWidget()
        signup_layout = QVBoxLayout(signup_tab)
        
        signup_layout.addWidget(QLabel("Full Name:"))
        self.signup_name = QLineEdit()
        signup_layout.addWidget(self.signup_name)
        
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
        
        signup_btn = QPushButton("Sign Up")
        signup_btn.clicked.connect(self.handle_signup)
        signup_layout.addWidget(signup_btn)
        
        signup_layout.addWidget(QLabel(
            "After signup, use your email and password to sign in."
        ))
        signup_layout.addStretch()
        
        # Add tabs
        tabs.addTab(signin_tab, "Sign In")
        tabs.addTab(signup_tab, "Sign Up")
        layout.addWidget(tabs)
        
        # Continue as Guest button
        guest_btn = QPushButton("Continue as Guest (3 free attempts)")
        guest_btn.clicked.connect(self.handle_guest)
        layout.addWidget(guest_btn)
    
    def handle_signin(self):
        """Handle sign in button."""
        email = self.signin_email.text().strip()
        password = self.signin_password.text()
        
        if not email or not password:
            QMessageBox.warning(self, "Input Error", "Please enter email and password.")
            return
        
        self.result_data = {'action': 'signin', 'email': email, 'password': password}
        self.accept()
    
    def handle_signup(self):
        """Handle sign up button."""
        name = self.signup_name.text().strip()
        email = self.signup_email.text().strip()
        password = self.signup_password.text()
        confirm = self.signup_confirm.text()
        
        if not name or not email or not password or not confirm:
            QMessageBox.warning(self, "Input Error", "Please fill all fields.")
            return
        
        if password != confirm:
            QMessageBox.warning(self, "Password Mismatch", "Passwords do not match.")
            return
        
        self.result_data = {
            'action': 'signup',
            'email': email,
            'password': password,
            'full_name': name
        }
        self.accept()
    
    def handle_guest(self):
        """Handle guest login."""
        self.result_data = {'action': 'guest'}
        self.accept()


class PaywallDialog(QDialog):
    """Dialog showing upgrade prompt when free limit is reached."""
    
    def __init__(self, parent=None, remaining: int = 0):
        super().__init__(parent)
        self.setWindowTitle("Upgrade to Pro")
        self.setMinimumWidth(450)
        self.upgrade_clicked = False
        self.init_ui(remaining)
    
    def init_ui(self, remaining: int):
        """Initialize paywall UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("🎉 Upgrade to Pro")
        title_font = title.font()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Content
        if remaining <= 0:
            message = """
            You've used all your free analyses (15/15).
            
            Upgrade to Pro to get:
            ✓ Unlimited skin disease analyses
            ✓ Priority support
            ✓ Advanced detection features
            ✓ Export analysis reports
            ✓ Medical recommendations
            
            Pro Subscription:
            💰 $4.99/month or $39.99/year
            
            Start your free trial today!
            """
        else:
            message = f"""
            You have {remaining} analyses remaining on your free plan.
            
            Upgrade to Pro now to get:
            ✓ Unlimited skin disease analyses
            ✓ Priority support
            ✓ Advanced detection features
            ✓ Export analysis reports
            ✓ Medical recommendations
            
            Pro Subscription:
            💰 $4.99/month or $39.99/year
            
            Start your free trial today!
            """
        
        content = QLabel(message)
        content.setWordWrap(True)
        layout.addWidget(content)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        upgrade_btn = QPushButton("Upgrade to Pro")
        upgrade_btn.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
        """)
        upgrade_btn.clicked.connect(self.handle_upgrade)
        button_layout.addWidget(upgrade_btn)
        
        later_btn = QPushButton("Maybe Later")
        later_btn.clicked.connect(self.reject)
        button_layout.addWidget(later_btn)
        
        layout.addLayout(button_layout)
    
    def handle_upgrade(self):
        """Handle upgrade button."""
        self.upgrade_clicked = True
        # In real app, this would redirect to payment gateway
        QMessageBox.information(
            self,
            "Payment",
            "In production, this would redirect to payment gateway.\n\n"
            "For demo, use payment ID: DEMO_123456"
        )
        self.accept()
