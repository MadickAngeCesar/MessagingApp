# Apartment Management & Messaging App

## Overview
This project is a desktop application built with PyQt6 and SQLite that integrates apartment management with user messaging. The app supports two types of users: landlords and tenants, and provides messaging, status updates, group management, and occupancy dashboard features.

## Features
- **Messaging:** One-on-one messaging between users.
- **Status Updates:** Landlords can post statuses; tenants view updates.
- **Apartment Management:** Initialize rooms, assign tenants, and view room status.
- **Groups:** Landlords can create and manage groups.
- **Dashboard:** Visualize apartment occupancy trends with interactive charts.
- **Resource Management:** Supports image assets using a resource helper, ensuring icons and logos are loaded correctly in both development and production.

## Installation
1. **Python Requirements:** Ensure you have Python 3 installed.
2. **Dependencies:** Install required packages by running:
   ```bash
   pip install PyQt6 matplotlib numpy scipy
   ```
3. **Running in Development Mode:**  
   Launch the application by executing:
   ```bash
   python main.py
   ```
   Images and icons are loaded from project files using a helper function.

## Resource Management
This project uses a helper (`utilities.py`) to load resources when running the executable. In development, files are read directly; in production (bundled via PyInstaller), the helper uses `sys._MEIPASS` to resolve the correct path.

## Building an Executable
To create a standalone executable:
1. **Install PyInstaller:**  
   ```bash
   pip install pyinstaller
   ```
2. **Generate and Edit Spec File:**  
   The provided `main.spec` file includes resource files (e.g., `university_logo.png`, `university_logo.ico`). Verify that the datas paths match your project's structure.
   - Generate a spec file:
   ```bash
   pyi-makespec --onefile --windowed --icon=university_logo.ico main.py
   ```
3. **Build the Executable:**
   ```bash
   pyinstaller main.spec
   ```
   The executable will be located in the `dist` folder.
   
   **Note:** If images/icons do not appear correctly in the built executable, ensure that all asset paths in your code use the `resource_path()` helper provided in `utilities.py`.

## Troubleshooting & FAQ
- **Missing Images in Production:**  
  If the university logo or icons are missing after building, confirm that:
  - The asset filenames and paths in `main.spec` match those in your project.
  - All resource paths in your code are obtained via `resource_path()`.
- **Database Issues:**  
  If you encounter issues with the database schema, check that any migrations (like adding the `password` column) have been applied correctly.

## Project Structure
- **model.py:** Manages SQLite database interactions.
- **view/**: Contains all PyQt6 UI modules including:
  - *login_view.py*: User authentication.
  - *main_view.py*: Main interface integrating multiple tabs.
  - Additional views: Messaging, Dashboard, Apartment Management, etc.
- **controller.py:** Coordinates app flow between model and view.
- **utilities.py:** Contains helpers (e.g., `resource_path()`) for resource management.
- **main.py:** Application entry point.
- **main.spec:** PyInstaller spec file for building the executable.

## Usage
Run the app with:
```bash
python main.py
```
Follow on-screen instructions to log in or register. Depending on your role, access features such as messaging, posting status updates (landlord only), or managing apartments.

## License
This project is provided "as is" without any warranty. Feel free to modify and distribute as needed.
