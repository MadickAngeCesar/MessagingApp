# view/main_view.py
import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget
from PyQt6.QtGui import QPixmap, QIcon  # added QIcon import
from PyQt6.QtCore import Qt
from view.tabs import MessagingTab, StatusTab, GroupsTab, ProfileTab, ApartmentManagementTab, DashboardTab

class MainView(QMainWindow):
    def __init__(self, user_id, user_name, user_role, db_manager, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.user_name = user_name
        self.user_role = user_role  # 'landlord' or 'tenant'
        self.db_manager = db_manager
        self.setWindowTitle("Apartment Management & Messaging App")
        self.setWindowIcon(QIcon("university_logo.ico"))  # set the app icon
        self.setGeometry(100, 100, 1000, 700)
        self.initUI()
    
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_layout = QHBoxLayout()
        logo_label = QLabel()
        logo_path = "university_logo.jpeg"
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path).scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pix)
        else:
            logo_label.setText("University Logo")
        header_layout.addWidget(logo_label)
        header_layout.addStretch()
        dev_label = QLabel("Developed by Madick Ange César")
        header_layout.addWidget(dev_label)
        main_layout.addLayout(header_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(MessagingTab(self.db_manager, self.user_id), "Messages")
        self.tabs.addTab(StatusTab(self.db_manager, self.user_id), "Status")
        self.tabs.addTab(ProfileTab(self.db_manager, self.user_id), "Profile")
        if self.user_role == "landlord":
            self.tabs.addTab(GroupsTab(self.db_manager, self.user_id), "Groups")
            self.tabs.addTab(DashboardTab(self.db_manager), "Dashboard")
            self.tabs.addTab(ApartmentManagementTab(self.db_manager), "Apartments")
        main_layout.addWidget(self.tabs)
        
        # Footer
        footer_text = "Apartment Management App | Messaging, Status, Profile"
        if self.user_role == "landlord":
            footer_text += ", Groups, Dashboard, Apartments"
        footer = QLabel(footer_text)
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(footer)
