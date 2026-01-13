# Implementation Plan: Skintelli - Intelligent Skin Disease Detection

**Branch**: `001-skin-disease-detection` | **Date**: 2026-01-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-skin-disease-detection/spec.md`

## Summary
This plan outlines the development of the Skintelli desktop application, a tool for offline skin disease screening. The system will use YOLOv8 for lesion detection, Grad-CAM for explainability, and a local LLM with RAG for generating natural language explanations. The development will be phased, prioritizing the core AI engine before the user interface.

## Technical Context
**Language/Version**: Python 3.11+
**Primary Dependencies**: PyTorch, Ultralytics (for YOLOv8), OpenCV, a local LLM library (e.g., llama-cpp-python), a vector store library (e.g., FAISS), and a GUI framework (Tkinter or PyQt).
**Storage**: Filesystem for images and a local database (e.g., SQLite) for user data and analysis history.
**Testing**: Pytest
**Target Platform**: Desktop (Windows, macOS, Linux)
**Project Type**: Single project
**Performance Goals**: Total analysis time under 10 seconds.
**Constraints**: Must operate fully offline.

## Project Structure

### Documentation (this feature)
```text
specs/001-skin-disease-detection/
├── plan.md              # This file
├── spec.md              # The feature specification
└── checklists/
    └── requirements.md
```

### Source Code (repository root)
```text
src/
├── core/
│   ├── detection.py      # YOLOv8 inference
│   ├── explainability.py # Grad-CAM implementation
│   ├── interpretation.py # LLM and RAG logic
│   └── orchestrator.py   # Main agentic workflow
├── data/
│   ├── ham10000/         # Dataset (placeholder)
│   └── knowledge_base/   # Medical context for RAG
├── ui/
│   ├── main.py           # Main GUI application
│   └── widgets/          # Custom UI components
├── models/               # Pre-trained model files
└── database/
    └── users.db          # User and history database
tests/
├── unit/
│   ├── test_detection.py
│   ├── test_explainability.py
│   └── test_interpretation.py
└── integration/
    └── test_orchestrator.py
```
**Structure Decision**: A single project structure is chosen for simplicity and because the application is a self-contained desktop tool.

## Development Phases

### Phase 1: Environment & Data Setup
1.  **Initialize Project**: Set up a virtual environment and a `pyproject.toml` file with `uv` for package management.
2.  **Install Dependencies**: Add and install core dependencies: `torch`, `ultralytics`, `opencv-python`, `faiss-cpu`, `llama-cpp-python` (or a mock), and `PyQt6` (or `Tkinter`).
3.  **Data Preparation**: Write a script to download the HAM10000 dataset (or a subset) and organize it into a directory structure suitable for training/testing.

### Phase 2: Core Detection Module
1.  **Implement Inference Script**: In `src/core/detection.py`, create a function that takes an image path as input.
2.  **Load Model**: Load the pre-trained YOLOv8 model.
3.  **Perform Inference**: Preprocess the image and run it through the model.
4.  **Return Results**: Return a JSON object with the classification and confidence score (e.g., `{'class': 'Melanoma', 'confidence': 0.85}`).

### Phase 3: Explainability Integration
1.  **Grad-CAM Wrapper**: In `src/core/explainability.py`, develop a wrapper class for the YOLOv8 model to apply Grad-CAM.
2.  **Generate Heatmap**: The wrapper should have a method that takes an image and a target class, and returns a heatmap image.
3.  **Overlay Heatmap**: Add a utility function to overlay the heatmap on the original image.

### Phase 4: RAG & LLM Engine
1.  **Setup Vector Store**: In `src/core/interpretation.py`, initialize a FAISS vector store.
2.  **Knowledge Base Ingestion**: Create a script to process a local medical knowledge base (e.g., text files or a CSV) and ingest it into the vector store.
3.  **LLM Interface**: Implement a function to query a local LLM. For initial development, this can be a mock that returns a hardcoded explanation.
4.  **RAG Implementation**: Create a function that takes a classification result, retrieves relevant context from the vector store, and uses the LLM to generate a natural language explanation.

### Phase 5: Backend Orchestrator
1.  **Create Orchestrator**: In `src/core/orchestrator.py`, create a main function that takes an image path as input.
2.  **Chain Modules**: This function will call the modules from Phases 2, 3, and 4 in sequence.
3.  **Data Flow**: Manage the data flow between the modules (e.g., pass the classification result to the RAG module).
4.  **Return Final Output**: Return a consolidated object with the classification, heatmap image path, and natural language explanation.

### Phase 6: GUI Implementation
1.  **Main Window**: In `src/ui/main.py`, create the main application window with a dual-panel layout.
2.  **UI Components**: Add buttons for "Upload Image" and "Capture from Camera", and display areas for the images and text.
3.  **Connect to Orchestrator**: Wire the UI events to the backend orchestrator function.
4.  **Display Results**: Display the results from the orchestrator in the UI.
5.  **User Authentication and History**: Implement the login/signup, history view, and PDF export features.

### Phase 7: Testing & Optimization
1.  **Unit Tests**: Write `pytest` tests for each function in the `core` modules.
2.  **Integration Test**: Write an integration test that runs the full pipeline from image input to final output.
3.  **Performance Profiling**: Use a profiler to measure the execution time of the orchestrator and identify any bottlenecks.
4.  **Offline Test**: Ensure the application works as expected with no internet connection.
