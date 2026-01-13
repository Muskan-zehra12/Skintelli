# Tasks: Skintelli - Intelligent Skin Disease Detection System

**Input**: Design documents from `/specs/002-skin-disease-detection/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 [P] Create project directory structure as defined in plan.md
- [x] T002 Initialize Python environment and install dependencies (PyQt6, ONNX Runtime, FPDF, pytest) in `requirements.txt`
- [x] T003 [P] Configure `.gitignore` for Python and desktop app artifacts
- [x] T004 [P] Initialize `desktop/src/__init__.py` in all subdirectories

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 [P] Implement SQLite database schema for Users and Analysis in `desktop/src/database/models.py`
- [ ] T006 Implement base AI Detection interface in `desktop/src/core/detection.py`
- [x] T007 [P] Implement base UI MainWindow with dual-panel layout placeholder in `desktop/src/ui/main_window.py`
- [ ] T008 [P] Implement logging infrastructure in `desktop/src/core/utils.py`


**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Skin Lesion Analysis from Image File (Priority: P1) 🎯 MVP

**Goal**: Allow users to upload an image and receive a full AI analysis (Detection + Heatmap + Explanation).

**Independent Test**: Upload a JPG/PNG, verify dual-panel shows original and heatmap, and explanation text appears.

### Implementation for User Story 1

- [ ] T009 [P] [US1] Implement image file validation logic in `desktop/src/core/utils.py`
- [ ] T010 [US1] Implement YOLOv8/ONNX inference in `desktop/src/core/detection.py`
- [ ] T011 [US1] Implement Heatmap generation (Grad-CAM equivalent) in `desktop/src/core/explainability.py`
- [ ] T012 [US1] Implement Local LLM/Mock RAG service in `desktop/src/core/interpretation.py`
- [ ] T013 [US1] Create Orchestrator (Agentic Workflow) in `desktop/src/core/agent.py` to tie detection, explainability, and interpretation
- [ ] T014 [US1] Implement "Image Upload" widget and Dual-Panel display in `desktop/src/ui/widgets/dual_panel.py`
- [ ] T015 [US1] Connect UI to Orchestrator in `desktop/src/ui/main_window.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Skin Lesion Analysis from Live Camera (Priority: P2)

**Goal**: Allow users to capture images directly from a webcam for analysis.

**Independent Test**: Open camera feed, capture image, and verify it triggers the same analysis pipeline as US1.

### Implementation for User Story 2

- [ ] T016 [US2] Implement OpenCV/PyQt camera feed widget in `desktop/src/ui/widgets/camera_feed.py`
- [ ] T017 [US2] Implement image capture logic and pass to US1 pipeline in `desktop/src/ui/main_window.py`
- [ ] T018 [US2] Add toggle between "Upload" and "Camera" modes in UI

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: User Story 3 - User Account and History (Priority: P3)

**Goal**: User authentication and saving/viewing past analysis history with PDF export.

**Independent Test**: Login, perform analysis, view in history tab, and export to PDF.

### Implementation for User Story 3

- [ ] T019 [P] [US3] Implement user login/signup logic in `desktop/src/core/auth.py`
- [ ] T020 [US3] Implement History database operations in `desktop/src/database/models.py`
- [ ] T021 [US3] Create History list view widget in `desktop/src/ui/widgets/history_view.py`
- [ ] T022 [US3] Implement PDF Export service using FPDF in `desktop/src/core/export.py`
- [ ] T023 [US3] Add "View History" and "Export PDF" buttons to UI

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T024 [P] Update `README.md` with installation and usage instructions
- [ ] T025 [P] Create `quickstart.md` for end-to-end test data
- [ ] T026 Perform UI/UX refinement (styles, icons, responsive layout)
- [ ] T027 [P] Implement final integration tests for all stories in `desktop/tests/integration/test_agentic_workflow.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Foundational phase completion.
  - US1 (P1) is the priority.
  - US2 (P2) depends on US1's analysis pipeline.
  - US3 (P3) integrates with all.
- **Polish (Final Phase)**: Depends on all user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Foundation for US2 and US3.
- **User Story 2 (P2)**: Requires US1 analysis pipeline.
- **User Story 3 (P3)**: Requires foundation and US1 analysis for history data.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 & 2.
2. Complete Phase 3 (US1).
3. **STOP and VALIDATE**: Verify offline analysis with image upload.

### Incremental Delivery

1. Foundation ready.
2. Add US1 (Analysis).
3. Add US2 (Camera).
4. Add US3 (History).
5. Final Polish.
