# SecurePass : Password-Generator-and-Text-Editor
SecurePass is a lightweight, multi-functional PyQt6 desktop application that combines a **password generator**, **password manager**, **simple text editor**, and **theme settings**.  
It helps you securely generate, save, and manage passwords, and includes a mini text editor for notes or documents.

---

## Features

- **Password Generator**
  - Choose password length (4–32 characters).
  - Options to include: uppercase letters, lowercase letters, digits, special characters.
  - Copy generated passwords to clipboard.
  - Save passwords with timestamps locally (`passwords.json`).

- **Saved Password Viewer**
  - View and manage previously saved passwords.
  - Click a password entry to instantly copy it to clipboard.

- **Text Editor**
  - Write and edit plain text documents.
  - Change font family and font size.
  - Apply formatting (Bold, Italic).
  - Open, save, and clear `.txt` files.
  - Basic copy-paste functionality.

- **Settings**
  - Toggle between Light and Dark Mode.
  - Settings are saved automatically (`config.json`) and restored on startup.

---

## Installation

**1. Download the source files**
   - Click the green `Code` button at the top right of the repository page.
   - Select `Download ZIP`.
   - Extract the ZIP file to your desired location.

**2. Install dependencies**
   ```bash
   pip install -r requirements
   ```

**3. Run the application**
   ```bash
   python main.py
   ```

---

## Requirements
- Python 3.7+
- Modules:
  - PyQt6
  - sys (standard library)
  - random (standard library)
  - string (standard library)
  - os (standard library)
  - json (standard library)
  - datetime (standard library)

---

## How to Use

- **Password Generator**: 
  - Set the password length and character options.
  - Click **Generate** to create a password.
  - Click **Copy** to copy the generated password.
  - Click **Save** to store it with a timestamp.

- **Saved Passwords**:
  - View all previously saved passwords.
  - Click any item to copy the password to the clipboard.

- **Text Editor**:
  - Type notes or text.
  - Select font family and size.
  - Use **Bold**/**Italic** buttons for formatting.
  - Open and save text files.

- **Settings**:
  - Enable/disable Dark Mode with a checkbox.
  - Settings are saved automatically.
