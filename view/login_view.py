# view/login_view.py
import os
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt

class LoginView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login / Register")
        self.setWindowIcon(QIcon("university_logo.ico"))  # set the app icon
        self.setFixedSize(350, 300)
        layout = QVBoxLayout()

        # Logo and Developer name
        self.logo_label = QLabel()
        logo_path = "university_logo.jpeg"
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            self.logo_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.logo_label.setText("University Logo")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo_label)
        
        self.dev_label = QLabel("Developed by Madick Ange César")
        self.dev_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.dev_label)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number")
        layout.addWidget(self.phone_input)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        layout.addWidget(self.name_input)
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Landlord", "Tenant"])
        layout.addWidget(QLabel("Select Role:"))
        layout.addWidget(self.role_combo)
        
        # New password field for landlords
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password (Landlord only)")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        self.password_input.setVisible(self.role_combo.currentText() == "Landlord")
        self.role_combo.currentTextChanged.connect(lambda role: self.password_input.setVisible(role == "Landlord"))
        
        self.landlord_phone_input = QLineEdit()
        self.landlord_phone_input.setPlaceholderText("Enter Landlord Phone")
        layout.addWidget(self.landlord_phone_input)
        self.landlord_phone_input.setVisible(self.role_combo.currentText() == "Tenant")
        self.role_combo.currentTextChanged.connect(lambda role: self.landlord_phone_input.setVisible(role == "Tenant"))
        
        self.login_button = QPushButton("Login / Register")
        layout.addWidget(self.login_button)
        self.setLayout(layout)
        
    def login(self):
        phone = self.phone_input.text().strip()
        name = self.name_input.text().strip()
        role = self.role_combo.currentText().lower()
        password = self.password_input.text().strip() if role == "landlord" else None
        landlord_phone = self.landlord_phone_input.text().strip() if role == "tenant" else None
        
        if not phone or not name:
            QMessageBox.warning(self, "Error", "Please enter both phone and name.")
            return

        if role == "tenant" and not landlord_phone:
            QMessageBox.warning(self, "Error", "Please enter your landlord's phone number.")
            return

        if role == "landlord" and not password:
            QMessageBox.warning(self, "Error", "Password is required for landlords.")
            return

        landlord_id = None
        if landlord_phone:
            from controller import AppController  # avoid circular dependency
            app_controller = AppController()
            db_manager = app_controller.db_manager
            landlord = db_manager.get_user_by_phone(landlord_phone)
            if not landlord:
                QMessageBox.warning(self, "Error", "Landlord with this phone number not found.")
                return
            landlord_id = landlord[0]

        from controller import AppController  # avoid circular dependency
        app_controller = AppController()
        db_manager = app_controller.db_manager
        try:
            user_id = db_manager.add_user(phone, name, role, landlord_id, password)
        except ValueError as ve:
            QMessageBox.warning(self, "Login Error", str(ve))
            return
        self.user_id = user_id
        self.accept()
