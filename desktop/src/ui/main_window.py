import sys
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
from PyQt6.QtCore import Qt
from ui.widgets.dual_panel import DualPanelWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Skintelli - Intelligent Skin Disease Detection")
        self.setMinimumSize(1000, 700)

        # Central Widget and Main Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Navigation Bar
        self.nav_layout = QHBoxLayout()
        self.btn_analysis = QPushButton("Analysis")
        self.btn_history = QPushButton("History")
        self.btn_logout = QPushButton("Logout")
        
        self.nav_layout.addWidget(self.btn_analysis)
        self.nav_layout.addWidget(self.btn_history)
        self.nav_layout.addStretch()
        self.nav_layout.addWidget(self.btn_logout)
        
        self.main_layout.addLayout(self.nav_layout)

        # Content Area (Stacked Widget to switch between Analysis and History)
        self.content_stack = QStackedWidget()
        self.main_layout.addWidget(self.content_stack)

        # Analysis View
        self.analysis_view = DualPanelWidget()
        self.content_stack.addWidget(self.analysis_view)

        # History View (Placeholder)
        self.history_view = QLabel("History View - Coming Soon")
        self.history_view.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_stack.addWidget(self.history_view)

        # Connect Navigation
        self.btn_analysis.clicked.connect(lambda: self.content_stack.setCurrentIndex(0))
        self.btn_history.clicked.connect(lambda: self.content_stack.setCurrentIndex(1))

        # Status Bar
        self.statusBar().showMessage("Ready")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
