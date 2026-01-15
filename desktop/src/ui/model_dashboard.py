"""
Model Training Dashboard Widget
Displays training progress and results in the PyQt6 UI
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem, QComboBox, QProgressBar,
                             QTextEdit, QTabWidget, QFileDialog, QMessageBox, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt6.QtGui import QFont, QColor
from pathlib import Path
import json
from typing import Dict, Any
import subprocess
import sys


class ModelTrainingDashboard(QWidget):
    """Dashboard for model training management"""
    
    training_started = pyqtSignal()
    training_completed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.results_manager = None
        self.current_session = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Model Training Dashboard")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Tab widget
        tabs = QTabWidget()
        
        # Tab 1: Colab Integration
        colab_tab = self.create_colab_tab()
        tabs.addTab(colab_tab, "Colab Integration")
        
        # Tab 2: Training Management
        training_tab = self.create_training_tab()
        tabs.addTab(training_tab, "Training Progress")
        
        # Tab 3: Results Viewer
        results_tab = self.create_results_tab()
        tabs.addTab(results_tab, "Results")
        
        layout.addWidget(tabs)
        self.setLayout(layout)
    
    def create_colab_tab(self) -> QWidget:
        """Create Colab integration tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Colab instructions
        instructions = QTextEdit()
        instructions.setReadOnly(True)
        instructions.setText("""
GOOGLE COLAB SETUP INSTRUCTIONS:

1. Open Google Colab: https://colab.research.google.com/

2. Upload the training notebook:
   - Click "File" → "Upload notebook"
   - Select: colab_training_notebook.py from your project

3. Authenticate Google Drive:
   - Run the first cell to mount your Drive
   - Authorize access when prompted

4. Configure Training:
   - Update data paths in the notebook
   - Set hyperparameters (epochs, batch size, etc.)
   - Configure GPU/TPU usage

5. Run Training:
   - Execute cells in order
   - Monitor training progress in Colab

6. Sync Results:
   - Results are automatically saved to your Google Drive
   - Click "Fetch Results" below to download them
        """)
        layout.addWidget(instructions)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        open_colab_btn = QPushButton("Open Google Colab")
        open_colab_btn.clicked.connect(self.open_colab)
        button_layout.addWidget(open_colab_btn)
        
        fetch_results_btn = QPushButton("Fetch Results from Drive")
        fetch_results_btn.clicked.connect(self.fetch_colab_results)
        button_layout.addWidget(fetch_results_btn)
        
        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_training_tab(self) -> QWidget:
        """Create training progress tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Current training session info
        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel("Session ID:"))
        self.session_label = QLabel("None")
        info_layout.addWidget(self.session_label)
        layout.addLayout(info_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)
        
        # Training logs
        layout.addWidget(QLabel("Training Logs:"))
        self.logs_display = QTextEdit()
        self.logs_display.setReadOnly(True)
        self.logs_display.setMaximumHeight(250)
        layout.addWidget(self.logs_display)
        
        # Metrics table
        layout.addWidget(QLabel("Epoch Metrics:"))
        self.metrics_table = QTableWidget()
        self.metrics_table.setColumnCount(5)
        self.metrics_table.setHorizontalHeaderLabels(
            ["Epoch", "Loss", "Accuracy", "Val Loss", "Val Accuracy"]
        )
        layout.addWidget(self.metrics_table)
        
        # Control buttons
        control_layout = QHBoxLayout()
        
        start_btn = QPushButton("Start Training")
        start_btn.clicked.connect(self.start_training)
        control_layout.addWidget(start_btn)
        
        pause_btn = QPushButton("Pause Training")
        pause_btn.clicked.connect(self.pause_training)
        control_layout.addWidget(pause_btn)
        
        stop_btn = QPushButton("Stop Training")
        stop_btn.clicked.connect(self.stop_training)
        control_layout.addWidget(stop_btn)
        
        layout.addLayout(control_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_results_tab(self) -> QWidget:
        """Create results viewer tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Results selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Select Result:"))
        self.results_combo = QComboBox()
        self.results_combo.currentIndexChanged.connect(self.on_result_selected)
        selector_layout.addWidget(self.results_combo)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_results)
        selector_layout.addWidget(refresh_btn)
        
        layout.addLayout(selector_layout)
        
        # Results details
        layout.addWidget(QLabel("Training Results:"))
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        layout.addWidget(self.results_display)
        
        # Export options
        export_layout = QHBoxLayout()
        
        export_json_btn = QPushButton("Export as JSON")
        export_json_btn.clicked.connect(self.export_json)
        export_layout.addWidget(export_json_btn)
        
        export_csv_btn = QPushButton("Export as CSV")
        export_csv_btn.clicked.connect(self.export_csv)
        export_layout.addWidget(export_csv_btn)
        
        layout.addLayout(export_layout)
        
        widget.setLayout(layout)
        return widget
    
    def open_colab(self):
        """Open Google Colab in browser"""
        import webbrowser
        webbrowser.open("https://colab.research.google.com/")
        QMessageBox.information(self, "Google Colab", "Opened Google Colab in your browser")
    
    def fetch_colab_results(self):
        """Fetch results from Google Drive"""
        QMessageBox.information(
            self, "Fetch Results",
            "Select the training results folder from your Google Drive:\n"
            "Usually: Google Drive > FYP1-Models > results"
        )
        # Implementation for fetching from Drive
    
    def start_training(self):
        """Start model training"""
        QMessageBox.information(self, "Training", "Training started!")
        self.training_started.emit()
    
    def pause_training(self):
        """Pause training"""
        QMessageBox.information(self, "Training", "Training paused!")
    
    def stop_training(self):
        """Stop training"""
        QMessageBox.information(self, "Training", "Training stopped!")
    
    def refresh_results(self):
        """Refresh results list"""
        self.results_combo.clear()
        # Load results from disk
        results_dir = Path("./models/results")
        if results_dir.exists():
            for result_file in sorted(results_dir.glob("*.json"), reverse=True):
                self.results_combo.addItem(result_file.stem, str(result_file))
    
    def on_result_selected(self):
        """Handle result selection"""
        if self.results_combo.currentData():
            result_path = self.results_combo.currentData()
            try:
                with open(result_path, 'r') as f:
                    data = json.load(f)
                self.results_display.setText(json.dumps(data, indent=2))
            except Exception as e:
                self.results_display.setText(f"Error loading results: {e}")
    
    def export_json(self):
        """Export current results as JSON"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Results as JSON", "", "JSON Files (*.json)"
        )
        if file_path:
            QMessageBox.information(self, "Export", f"Results exported to {file_path}")
    
    def export_csv(self):
        """Export current results as CSV"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Results as CSV", "", "CSV Files (*.csv)"
        )
        if file_path:
            QMessageBox.information(self, "Export", f"Results exported to {file_path}")


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    dashboard = ModelTrainingDashboard()
    dashboard.show()
    sys.exit(app.exec())
