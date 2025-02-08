# controller.py
import sys
from model import DatabaseManager
from view.login_view import LoginView
from view.main_view import MainView
from PyQt6.QtWidgets import QApplication, QDialog

class AppController:
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def run(self):
        app = QApplication(sys.argv)
        
        login = LoginView()
        login.login_button.clicked.connect(lambda: self.process_login(login))
        if login.exec() == QDialog.DialogCode.Accepted:
            user_id = login.user_id
            user_name = login.name_input.text().strip()
            user_role = login.role_combo.currentText().lower()
            main_view = MainView(user_id, user_name, user_role, self.db_manager)
            main_view.show()
            app.exec()
    
    def process_login(self, login_view):
        # Process login data; this function is called when login_button is pressed.
        login_view.login()
        
if __name__ == "__main__":
    controller = AppController()
    controller.run()
