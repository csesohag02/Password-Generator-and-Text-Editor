from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QCheckBox, QSpinBox, QTabWidget, QTextEdit, QFileDialog,
    QFontComboBox, QComboBox, QMessageBox, QListWidget
)
from PyQt6.QtGui import QFont, QTextCharFormat, QTextCursor
import sys
import random
import string
import os
import json
from datetime import datetime

PASSWORD_FILE = "passwords.json"

class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Password Length Selection
        length_layout = QHBoxLayout()
        self.length_label = QLabel("Password Length:")
        self.length_spinbox = QSpinBox()
        self.length_spinbox.setRange(4, 32)
        self.length_spinbox.setValue(12)
        length_layout.addWidget(self.length_label)
        length_layout.addWidget(self.length_spinbox)

        # Character Options
        self.uppercase_checkbox = QCheckBox("Uppercase")
        self.uppercase_checkbox.setChecked(True)
        self.lowercase_checkbox = QCheckBox("Lowercase")
        self.lowercase_checkbox.setChecked(True)
        self.digits_checkbox = QCheckBox("Digits")
        self.digits_checkbox.setChecked(True)
        self.special_checkbox = QCheckBox("Special Characters")
        self.special_checkbox.setChecked(True)

        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)

        # Buttons
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_password_action)
        
        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.copy_password)
        
        self.save_button = QPushButton("Save")  # Changed from Load to Save
        self.save_button.clicked.connect(self.save_password)

        action_layout = QHBoxLayout()
        action_layout.addWidget(self.generate_button)
        action_layout.addWidget(self.copy_button)
        action_layout.addWidget(self.save_button)

        layout.addLayout(length_layout)
        layout.addWidget(self.uppercase_checkbox)
        layout.addWidget(self.lowercase_checkbox)
        layout.addWidget(self.digits_checkbox)
        layout.addWidget(self.special_checkbox)
        layout.addWidget(self.password_display)
        layout.addLayout(action_layout)
        self.setLayout(layout)

    def generate_password(self):
        length = self.length_spinbox.value()
        characters = ""
        if self.uppercase_checkbox.isChecked():
            characters += string.ascii_uppercase
        if self.lowercase_checkbox.isChecked():
            characters += string.ascii_lowercase
        if self.digits_checkbox.isChecked():
            characters += string.digits
        if self.special_checkbox.isChecked():
            characters += string.punctuation

        if not characters:
            return "Select at least one option!"

        return ''.join(random.choice(characters) for _ in range(length))

    def generate_password_action(self):
        new_password = self.generate_password()
        self.password_display.setText(new_password)

    def save_password(self):
        password = self.password_display.text()
        if not password:
            QMessageBox.warning(self, "Warning", "No password to save!")
            return

        password_entry = {
            "password": password,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if os.path.exists(PASSWORD_FILE):
            with open(PASSWORD_FILE, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        data.append(password_entry)

        with open(PASSWORD_FILE, "w") as file:
            json.dump(data, file, indent=4)

        QMessageBox.information(self, "Saved", "Password saved successfully!")

    def copy_password(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password_display.text())

class PasswordViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.load_saved_passwords()
        self.list_widget.itemClicked.connect(self.copy_selected_password)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def load_saved_passwords(self):
        self.list_widget.clear()
        if os.path.exists(PASSWORD_FILE):
            with open(PASSWORD_FILE, "r") as file:
                try:
                    data = json.load(file)
                    for entry in data:
                        self.list_widget.addItem(f"{entry['timestamp']}: {entry['password']}")
                except json.JSONDecodeError:
                    self.list_widget.addItem("No saved passwords.")
        else:
            self.list_widget.addItem("No saved passwords.")

    def copy_selected_password(self, item):
        password = item.text().split(": ")[-1]
        clipboard = QApplication.clipboard()
        clipboard.setText(password)
        QMessageBox.information(self, "Copied", "Password copied to clipboard!")

class TextEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 🔹 Text Area
        self.text_area = QTextEdit()

        # 🔹 Font and Size Selectors
        self.font_selector = QFontComboBox()
        self.font_selector.currentFontChanged.connect(self.change_font)

        self.size_selector = QComboBox()
        self.size_selector.addItems([str(i) for i in range(8, 30, 2)])
        self.size_selector.currentIndexChanged.connect(self.change_font_size)

        # 🔹 Action Buttons (Copy, Paste, Bold, Italic)
        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.copy_text)

        self.paste_button = QPushButton("Paste")
        self.paste_button.clicked.connect(self.paste_text)

        self.bold_button = QPushButton("Bold")
        self.bold_button.clicked.connect(self.make_bold)

        self.italic_button = QPushButton("Italic")
        self.italic_button.clicked.connect(self.make_italic)

        # 🔹 File Buttons (Open, Save, Close)
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.open_file)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_file)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close_file)

        # 🔹 Toolbar Layout
        toolbar_layout = QHBoxLayout()
        toolbar_layout.addWidget(self.font_selector)
        toolbar_layout.addWidget(self.size_selector)
        toolbar_layout.addWidget(self.copy_button)
        toolbar_layout.addWidget(self.paste_button)
        toolbar_layout.addWidget(self.bold_button)
        toolbar_layout.addWidget(self.italic_button)
        toolbar_layout.addWidget(self.open_button)
        toolbar_layout.addWidget(self.save_button)
        toolbar_layout.addWidget(self.close_button)

        layout.addLayout(toolbar_layout)
        layout.addWidget(self.text_area)
        self.setLayout(layout)

    # 🔹 Font and Style Functions
    def change_font(self, font):
        format = QTextCharFormat()
        format.setFont(font)
        self.text_area.textCursor().mergeCharFormat(format)

    def change_font_size(self):
        size = int(self.size_selector.currentText())
        format = QTextCharFormat()
        format.setFontPointSize(size)
        self.text_area.textCursor().mergeCharFormat(format)

    def make_bold(self):
        format = QTextCharFormat()
        format.setFontWeight(QFont.Weight.Bold)
        self.text_area.textCursor().mergeCharFormat(format)

    def make_italic(self):
        format = QTextCharFormat()
        format.setFontItalic(True)
        self.text_area.textCursor().mergeCharFormat(format)

    # 🔹 Copy & Paste Functions
    def copy_text(self):
        self.text_area.copy()

    def paste_text(self):
        self.text_area.paste()

    # 🔹 File Operations (Open, Save, Close)
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            with open(file_name, "r") as file:
                self.text_area.setPlainText(file.read())

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            with open(file_name, "w") as file:
                file.write(self.text_area.toPlainText())

    def close_file(self):
        self.text_area.clear()


class SettingsTab(QWidget):
    CONFIG_FILE = "config.json"

    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)
        layout.addWidget(self.dark_mode_checkbox)
        self.setLayout(layout)

        # Load and apply saved setting
        self.load_settings()

    def toggle_dark_mode(self):
        dark_mode = self.dark_mode_checkbox.isChecked()
        self.apply_theme(dark_mode)
        self.save_settings(dark_mode)

    def apply_theme(self, dark_mode):
        if dark_mode:
            dark_style = """
                QWidget { background-color: #2b2b2b; color: #ffffff; }
                QPushButton { background-color: #555; color: #fff; border-radius: 5px; padding: 5px; }
                QPushButton:hover { background-color: #777; }
                QLineEdit, QTextEdit, QListWidget { background-color: #444; color: #fff; border: 1px solid #666; }
                QTabWidget::pane { border: 1px solid #666; }
            """
        else:
            dark_style = ""  # Reset to default (light mode)

        self.main_app.setStyleSheet(dark_style)

    def save_settings(self, dark_mode):
        config = {"dark_mode": dark_mode}
        with open(self.CONFIG_FILE, "w") as file:
            json.dump(config, file)

    def load_settings(self):
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, "r") as file:
                try:
                    config = json.load(file)
                    dark_mode = config.get("dark_mode", False)
                    self.dark_mode_checkbox.setChecked(dark_mode)
                    self.apply_theme(dark_mode)
                except json.JSONDecodeError:
                    pass  # Ignore errors and use default light mode

    def apply_saved_theme(self):
        """Call this from MainApp to apply the saved theme at startup."""
        self.load_settings()


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.password_generator_tab = PasswordGenerator()
        self.password_viewer_tab = PasswordViewer()
        self.text_editor_tab = TextEditor()
        self.settings_tab = SettingsTab(self)

        self.tabs.addTab(self.password_generator_tab, "Password Generator")
        self.tabs.addTab(self.password_viewer_tab, "Saved Passwords")
        self.tabs.addTab(self.text_editor_tab, "Text Editor")
        self.tabs.addTab(self.settings_tab, "Settings")
        
        self.settings_tab.apply_saved_theme()
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        self.setWindowTitle("SecurePass")
        self.resize(500, 400)
        

    def show_saved_passwords(self):
        self.password_viewer_tab.load_saved_passwords()
        self.tabs.setCurrentWidget(self.password_viewer_tab)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
