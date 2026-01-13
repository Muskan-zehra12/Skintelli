# Research: GUI Framework for Skintelli

## Decision

We will use **PyQt** for the Skintelli desktop application.

## Rationale

The choice between Tkinter and PyQt depends on the desired balance between simplicity, features, and visual appeal.

- **Tkinter**:
    - **Pros**: Included in the Python standard library, lightweight, easy to learn for simple GUIs.
    - **Cons**: Outdated look and feel, less flexible for complex UIs, requires more manual effort for modern designs.

- **PyQt**:
    - **Pros**: Modern and professional look, extensive set of widgets, powerful and flexible for complex UIs, good community support and documentation. The Qt Designer tool allows for visual UI design, which can speed up development.
    - **Cons**: Not included in the standard library (requires installation), can be more complex to learn than Tkinter. Licensing (GPL/Commercial) needs to be considered, but for an open-source project, GPL is suitable.

Given that the Skintelli application requires a dual-panel display and a polished user interface, **PyQt is the better choice**. It will provide the necessary tools to create a modern and user-friendly application, even if it has a slightly steeper learning curve.

## Alternatives considered

- **Tkinter**: Considered for its simplicity, but rejected due to its limitations in creating a modern UI.
- **Kivy**: A good choice for cross-platform applications (including mobile), but can be overkill for a desktop-only application and has a different design paradigm.
- **wxPython**: Another powerful option, but PyQt is generally considered to have a more modern look and feel.
