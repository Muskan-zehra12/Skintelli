# Contributing to Skintelli

Thank you for your interest in contributing to Skintelli! This document provides guidelines and instructions for contributing to the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)

## Code of Conduct

By participating in this project, you agree to:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites
- Python 3.11 or higher
- Git installed and configured
- GitHub account
- Basic knowledge of PyQt6, OpenCV, and Python

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Skintelli.git
   cd Skintelli
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/Muskan-zehra12/Skintelli.git
   ```

## Development Setup

1. **Create virtual environment**:
   ```bash
   python -m venv .venv
   ```

2. **Activate virtual environment**:
   - Windows: `.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`

3. **Install dependencies**:
   ```bash
   pip install -r desktop/requirements.txt
   ```

4. **Run the application**:
   ```bash
   python desktop/src/main.py
   ```

## Making Changes

### Branch Naming Convention
Create a feature branch with a descriptive name:
```bash
git checkout -b feature/your-feature-name
git checkout -b bugfix/issue-description
git checkout -b docs/documentation-update
```

Examples:
- `feature/add-pdf-export`
- `bugfix/fix-camera-crash`
- `docs/update-installation-guide`

### Commit Message Guidelines

Use clear, descriptive commit messages:

**Format**:
```
<type>: <short summary>

<detailed description if needed>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat: Add PDF export functionality for analysis reports

fix: Resolve camera initialization issue on Windows 11

docs: Update README with new authentication features

refactor: Simplify skin analysis algorithm
```

### Development Workflow

1. **Keep your fork updated**:
   ```bash
   git fetch upstream
   git merge upstream/main
   ```

2. **Make your changes**:
   - Write clean, documented code
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation as needed

3. **Test your changes**:
   - Run the application and test manually
   - Ensure no existing functionality breaks
   - Test edge cases

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

## Submitting Changes

### Pull Request Process

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request** on GitHub:
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

3. **PR Description should include**:
   - What changes were made
   - Why the changes were necessary
   - How to test the changes
   - Screenshots (if UI changes)
   - Related issues (if any)

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
How to test these changes:
1. Step 1
2. Step 2
3. Expected result

## Screenshots (if applicable)
Add screenshots here

## Checklist
- [ ] Code follows project style guidelines
- [ ] Changes have been tested
- [ ] Documentation updated
- [ ] No breaking changes
```

## Coding Standards

### Python Style Guide
- Follow [PEP 8](https://pep8.org/) style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Code Organization
```python
# Imports: stdlib, third-party, local
import sys
from typing import Optional

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

from core.auth import UserManager


# Class definition
class MyWidget(QWidget):
    """Brief description of the class.
    
    Detailed description if needed.
    """
    
    def __init__(self):
        """Initialize the widget."""
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        # UI setup code
        pass
    
    def process_data(self, data: str) -> Optional[dict]:
        """Process input data and return results.
        
        Args:
            data: Input data to process
            
        Returns:
            Dictionary with results or None if processing fails
        """
        # Processing logic
        return None
```

### Documentation Standards

**Module Docstrings**:
```python
"""Module for skin disease analysis.

This module contains classes and functions for analyzing
skin images and detecting abnormalities.
"""
```

**Function Docstrings**:
```python
def analyze_image(image: np.ndarray, threshold: float = 0.5) -> dict:
    """Analyze skin image for abnormalities.
    
    Args:
        image: Input image as numpy array
        threshold: Detection threshold (0.0 to 1.0)
        
    Returns:
        Dictionary containing:
            - severity: str (None/Low/Medium/High)
            - affected_percentage: float
            - diagnosis: str
            
    Raises:
        ValueError: If image is invalid or empty
    """
```

### UI/UX Guidelines
- Follow existing design patterns
- Maintain consistent styling
- Use emoji indicators appropriately
- Provide clear user feedback
- Handle errors gracefully

## Testing Guidelines

### Manual Testing Checklist
Before submitting a PR, test:

- [ ] Application launches without errors
- [ ] All existing features work correctly
- [ ] New feature works as expected
- [ ] Edge cases are handled
- [ ] Error messages are clear
- [ ] UI is responsive
- [ ] Camera functionality works (if applicable)
- [ ] Authentication flows work (if applicable)

### Future: Automated Testing
When we add automated tests:
- Write unit tests for new functions
- Update integration tests
- Ensure all tests pass before submitting PR

## Areas for Contribution

### High Priority
- [ ] Analysis history tracking and database
- [ ] PDF report generation
- [ ] Payment gateway integration
- [ ] Email verification system
- [ ] Password reset functionality

### Medium Priority
- [ ] Unit and integration tests
- [ ] Performance optimizations
- [ ] Additional image filters
- [ ] Dark mode UI theme
- [ ] Multi-language support

### Low Priority
- [ ] Advanced statistics dashboard
- [ ] Export to different formats (CSV, JSON)
- [ ] Keyboard shortcuts
- [ ] Accessibility improvements

## Questions or Issues?

If you have questions or run into issues:
1. Check existing [GitHub Issues](https://github.com/Muskan-zehra12/Skintelli/issues)
2. Create a new issue with detailed description
3. Tag with appropriate labels (bug, question, enhancement)

## Recognition

Contributors will be recognized in:
- README.md Contributors section
- Release notes
- Project documentation

Thank you for contributing to Skintelli! 🎉
