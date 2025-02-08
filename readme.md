# Apartment Management & Messaging App

## Overview
This project is a desktop application built with PyQt6 and SQLite. It provides features for apartment management, messaging, status updates, group communications, and more. The app is designed for two user types: landlords and tenants.

## Features
- **Messaging:** One-on-one messaging between users.
- **Status Updates:** Landlords can post statuses; tenants can view updates.
- **Apartment Management:** Initialize rooms, assign tenants, and view room status.
- **Groups:** Landlords can create groups and manage group members.
- **Dashboard:** Visual overview of apartment occupancy trends.

## Installation
1. Ensure you have Python 3 installed.
2. Install required packages:
   ```
   pip install PyQt6 matplotlib numpy scipy
   ```
3. Run the application:
   ```
   python main.py
   ```

## Building an Executable
↑To create a standalone executable for the app, 
- install PyInstaller:
```bash
pip install pyinstaller
```
- Generate a spec file:
```bash
pyi-makespec --onefile --windowed --icon=university_logo.ico main.py
```
Then run:
```bash
pyinstaller main.spec
```
The executable will be created in the `dist` folder.

## Project Structure
- **model.py:** Contains the DatabaseManager for SQLite operations.
- **view/**: Contains all the PyQt6 view files:
  - *login_view.py*: Handles user login and registration.
  - *main_view.py*: Main window integrating all tabs.
  - Other tab files for messaging, groups, dashboard, apartment management, etc.
- **controller.py:** Manages the app flow and coordination between views and the model.
- **main.py:** Entry point of the application.

## Usage
Launch the app using `python main.py` and follow the on-screen instructions to login or register. Depending on your role (landlord or tenant), access features such as messaging, status, and apartment management.

## License
This project is provided "as is" without any warranty. Feel free to modify and distribute it as needed.
