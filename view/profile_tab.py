# profile_tab.py
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ProfileTab(QWidget):
    def __init__(self, db_manager, current_user_id, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.current_user_id = current_user_id
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        
        self.name_label = QLabel("Name:")
        layout.addWidget(self.name_label)
        self.name_edit = QLineEdit()
        layout.addWidget(self.name_edit)
        
        self.phone_label = QLabel("Phone:")
        layout.addWidget(self.phone_label)
        self.phone_edit = QLineEdit()
        self.phone_edit.setReadOnly(True)
        layout.addWidget(self.phone_edit)
        
        self.role_label = QLabel("Role:")
        layout.addWidget(self.role_label)
        self.role_display = QLabel("")
        layout.addWidget(self.role_display)
        
        self.pic_label = QLabel("Profile Picture:")
        layout.addWidget(self.pic_label)
        self.pic_display = QLabel()
        self.pic_display.setFixedSize(100, 100)
        self.pic_display.setStyleSheet("border: 1px solid gray;")
        layout.addWidget(self.pic_display)
        
        self.change_pic_button = QPushButton("Change Picture")
        self.change_pic_button.clicked.connect(self.change_profile_picture)
        layout.addWidget(self.change_pic_button)
        
        self.update_button = QPushButton("Update Profile")
        self.update_button.clicked.connect(self.update_profile)
        layout.addWidget(self.update_button)
        
        self.load_profile()
    
    def load_profile(self):
        user = self.db_manager.get_user(self.current_user_id)
        if user:
            # user tuple: (id, phone, name, profile_pic, role, landlord_id)
            _, phone, name, profile_pic, role, _ = user
            self.name_edit.setText(name)
            self.phone_edit.setText(phone)
            self.role_display.setText(role.capitalize())
            if profile_pic and os.path.exists(profile_pic):
                pix = QPixmap(profile_pic).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                self.pic_display.setPixmap(pix)
            else:
                self.pic_display.setText("No Picture")
    
    def change_profile_picture(self):
        from PyQt6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Profile Picture")
        if file_path:
            pix = QPixmap(file_path).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.pic_display.setPixmap(pix)
            self.new_profile_pic = file_path
    
    def update_profile(self):
        name = self.name_edit.text().strip()
        profile_pic = getattr(self, "new_profile_pic", None)
        self.db_manager.update_user_profile(self.current_user_id, name=name, profile_pic=profile_pic)
        QMessageBox.information(self, "Profile Updated", "Your profile has been updated.")
        self.load_profile()
