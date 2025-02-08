# apartment_tab.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PyQt6.QtCore import Qt

class ApartmentManagementTab(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        # Header
        header = QLineEdit("Apartment Management")
        header.setReadOnly(True)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Initialize rooms section
        init_layout = QHBoxLayout()
        self.num_rooms_edit = QLineEdit()
        self.num_rooms_edit.setPlaceholderText("Enter total number of rooms")
        init_layout.addWidget(self.num_rooms_edit)
        self.init_rooms_button = QPushButton("Initialize Rooms")
        self.init_rooms_button.clicked.connect(self.initialize_rooms)
        init_layout.addWidget(self.init_rooms_button)
        layout.addLayout(init_layout)
        
        # Table to show room assignments
        self.rooms_table = QTableWidget()
        self.rooms_table.setColumnCount(2)
        self.rooms_table.setHorizontalHeaderLabels(["Room Number", "Tenant Name"])
        self.rooms_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.rooms_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.rooms_table)
        
        # Controls to assign tenant to a room (by tenant name)
        assign_layout = QHBoxLayout()
        self.room_number_edit = QLineEdit()
        self.room_number_edit.setPlaceholderText("Room Number")
        assign_layout.addWidget(self.room_number_edit)
        self.tenant_name_edit = QLineEdit()
        self.tenant_name_edit.setPlaceholderText("Tenant Name")
        assign_layout.addWidget(self.tenant_name_edit)
        self.assign_button = QPushButton("Assign Tenant")
        self.assign_button.clicked.connect(self.assign_tenant)
        assign_layout.addWidget(self.assign_button)
        layout.addLayout(assign_layout)
        
        self.load_rooms()
    
    def initialize_rooms(self):
        try:
            num = int(self.num_rooms_edit.text().strip())
            self.db_manager.initialize_rooms(num)
            self.load_rooms()
            QMessageBox.information(self, "Rooms Initialized", f"Initialized {num} rooms.")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid number.")
    
    def load_rooms(self):
        rooms = self.db_manager.get_rooms()  # returns list of (room_number, tenant_id)
        self.rooms_table.setRowCount(len(rooms))
        for row, (room_number, tenant_id) in enumerate(rooms):
            self.rooms_table.setItem(row, 0, QTableWidgetItem(room_number))
            if tenant_id:
                tenant = self.db_manager.get_user(tenant_id)
                tenant_name = tenant[2] if tenant else "Unknown"
                self.rooms_table.setItem(row, 1, QTableWidgetItem(tenant_name))
            else:
                self.rooms_table.setItem(row, 1, QTableWidgetItem("Vacant"))
    
    def assign_tenant(self):
        room_number = self.room_number_edit.text().strip()
        tenant_name = self.tenant_name_edit.text().strip()
        if room_number and tenant_name:
            if self.db_manager.assign_tenant_to_room_by_name(room_number, tenant_name):
                self.load_rooms()
                QMessageBox.information(self, "Assigned", f"Assigned {tenant_name} to room {room_number}.")
            else:
                QMessageBox.warning(self, "Error", "Tenant not found or could not be assigned.")
        else:
            QMessageBox.warning(self, "Input Error", "Please provide both room number and tenant name.")
