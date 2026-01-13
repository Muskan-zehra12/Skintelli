# Data Model

This document describes the data entities for the Skintelli application.

## User

Represents a user of the application.

**Fields**:
- `username` (string, primary key): The user's unique username.
- `password_hash` (string): The hashed password for the user.

**Validation**:
- `username` must be unique and between 3 and 50 characters.
- `password` must be at least 8 characters long.

## Analysis

Represents a single skin lesion analysis performed by a user.

**Fields**:
- `id` (integer, primary key): A unique identifier for the analysis.
- `user_username` (string, foreign key): The username of the user who performed the analysis.
- `timestamp` (datetime): The date and time when the analysis was performed.
- `input_image_path` (string): The path to the input image file.
- `heatmap_image_path` (string): The path to the generated heatmap image.
- `diagnosis` (string): The classification result from the model (e.g., "Melanoma", "Benign").
- `explanation` (text): The natural language explanation of the diagnosis.

**Relationships**:
- A `User` can have multiple `Analysis` records.
- An `Analysis` belongs to one and only one `User`.
