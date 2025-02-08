# groups_tab.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QMessageBox
from PyQt6.QtCore import Qt

class GroupsTab(QWidget):
    def __init__(self, db_manager, current_user_id, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.current_user_id = current_user_id
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        self.groups_list = QListWidget()
        layout.addWidget(self.groups_list)
        self.group_input = QLineEdit()
        self.group_input.setPlaceholderText("Enter new group name (landlord only)...")
        layout.addWidget(self.group_input)
        self.create_button = QPushButton("Create Group")
        self.create_button.clicked.connect(self.create_group)
        layout.addWidget(self.create_button)
        self.view_members_button = QPushButton("View Group Members")
        self.view_members_button.clicked.connect(self.view_group_members)
        layout.addWidget(self.view_members_button)
        self.load_groups()
    
    def create_group(self):
        # Only landlords can create groups.
        user = self.db_manager.get_user(self.current_user_id)
        if user and user[4] != "landlord":
            QMessageBox.warning(self, "Not Allowed", "Only landlords can create groups.")
            return
        group_name = self.group_input.text().strip()
        if group_name:
            group_id = self.db_manager.add_group(group_name, self.current_user_id)
            self.db_manager.add_user_to_group(group_id, self.current_user_id)
            self.group_input.clear()
            self.load_groups()
    
    def load_groups(self):
        self.groups_list.clear()
        groups = self.db_manager.get_groups()
        for group_id, name in groups:
            self.groups_list.addItem(f"{group_id}: {name}")
    
    def view_group_members(self):
        current_item = self.groups_list.currentItem()
        if current_item:
            group_info = current_item.text().split(":")
            group_id = int(group_info[0])
            members = self.db_manager.get_group_members(group_id)
            member_names = ", ".join([name for (_, name) in members])
            QMessageBox.information(self, "Group Members", f"Members: {member_names}")
        else:
            QMessageBox.warning(self, "No Group Selected", "Please select a group.")
