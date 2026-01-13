---
id: PHR-001
title: Skintelli Initial Constitution
stage: constitution
date: 2026-01-13
surface: GitHub Copilot CLI
model: claude-sonnet-4.5
feature: N/A
branch: N/A
user: Project Team
command: /sp.constitution
labels: [constitution, initial-setup, medical-ai, explainability]
links:
  spec: N/A
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - path: .specify/memory/constitution.md
    status: created
    lines_changed: 288
tests:
  - type: validation
    status: pass
    description: No remaining placeholder tokens
---

## Prompt

Create the project constitution for Skintelli with the following details:

**Project Name:** Skintelli: Intelligent Skin Disease Detection System with Explainable AI

**Vision & Mission:** To bridge the critical gap of dermatologist shortages in Pakistan (1:180,000 ratio) by providing a desktop-based AI screening tool that prioritizes transparency. Unlike "black box" AI, Skintelli builds user trust by visualizing why a diagnosis was made using Explainable AI (XAI) and providing context via LLMs.

**Core Principles (The "Laws" of this Project):**

1. **Explainability First:** Every AI prediction must be accompanied by a visual justification (Grad-CAM heatmap) and a textual explanation (LLM/RAG). A prediction without an explanation is considered a failure.

2. **Medical Accuracy & Safety:** The RAG (Retrieval-Augmented Generation) system must strictly source information from the provided medical knowledge base to prevent hallucinations.

3. **Accessibility & Simplicity:** The Desktop GUI must be navigable by non-technical users in rural centers. Complex configurations must be hidden behind a "One-Click Analysis" workflow.

4. **Local-First Architecture:** Given the target deployment in areas with unstable internet, the core detection (YOLOv8) and analysis pipeline should function efficiently on local hardware where possible.

**Technology Standards:**
- Detection: YOLOv8 (Optimized for skin lesion classification)
- Explainability: Grad-CAM (Gradient-weighted Class Activation Mapping)
- Interpretation: LLM integrated with RAG for natural language medical reports
- Interface: User-friendly Desktop Application (Python-based)

## Response snapshot

Successfully created Skintelli project constitution v1.0.0 with the following structure:

**Core Principles Established:**
1. **Explainability First** - Mandatory visual (Grad-CAM) + textual (RAG/LLM) justification for every prediction
2. **Medical Accuracy & Safety** - Strict source attribution from medical knowledge base, hallucination prevention
3. **Accessibility & Simplicity** - One-click analysis workflow, <3 clicks for primary tasks, multilingual support
4. **Local-First Architecture** - Core detection runs locally, optional cloud connectivity

**Additional Sections:**
- **Technology Standards** - Detailed specifications for detection (YOLOv8), explainability (Grad-CAM), RAG pipeline, UI framework
- **Development Workflow** - Constitution Check gate, testing requirements, code review standards, quality gates
- **Governance** - Amendment process, versioning policy (semantic versioning), compliance requirements

**Sync Impact Report (embedded in constitution):**
- Version: 1.0.0 (initial ratification)
- Ratified: 2026-01-13
- Template dependencies validated (spec, plan, tasks templates compatible)
- Follow-up actions documented for feature development

## Outcome

- ✅ Impact: Comprehensive constitution established with 4 core principles aligned to medical AI safety and accessibility requirements. Provides clear governance framework for Skintelli development.
- 🧪 Tests: Validation passed - zero remaining placeholder tokens, all bracketed template markers resolved
- 📁 Files: Created `.specify/memory/constitution.md` (288 lines), Sync Impact Report embedded as HTML comment
- 🔁 Next prompts: 
  - Create first feature specification aligned with explainability principles
  - Generate custom checklist for XAI validation
  - Create ADR for RAG architecture decisions (local vs. cloud LLM)
- 🧠 Reflection: Constitution successfully balances medical safety requirements with practical deployment constraints. Local-first architecture principle critical for target environment (Pakistan rural clinics). Explainability as non-negotiable requirement sets strong precedent for trust-building.

## Evaluation notes (flywheel)

- Failure modes observed: None - template placeholders successfully resolved with domain-specific content
- Graders run and results (PASS/FAIL): 
  - Bracket token validation: PASS (0 remaining placeholders)
  - Template consistency check: PASS (plan-template.md Constitution Check gate compatible)
- Prompt variant (if applicable): N/A (initial constitution creation)
- Next experiment (smallest change to try): Monitor first feature specification to validate whether constitution principles are actionable and measurable during planning phase. May need to add specific confidence thresholds or accuracy metrics if principles are too abstract for implementation validation.
