# dashboard_tab.py
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt6.QtWidgets import QWidget, QVBoxLayout

class DashboardTab(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        # Create a Matplotlib figure and embed it in a canvas
        self.figure, self.ax = plt.subplots(figsize=(4, 3))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        # Update the dashboard when shown (or you can call update_dashboard() periodically)
        self.update_dashboard()
    
    def update_dashboard(self):
        # Get room data from the model
        rooms = self.db_manager.get_rooms()  # returns list of tuples (room_number, tenant_id)
        total = len(rooms)
        occupied = sum(1 for _, tenant in rooms if tenant)
        occupancy_pct = (occupied / total * 100) if total > 0 else 0

        # For demonstration, simulate a 20-day history trending to current occupancy
        days = np.arange(1, 21)
        # Dummy history: linearly trends from 70% to the current occupancy with random noise
        history = np.linspace(70, occupancy_pct, num=20) + np.random.randint(-3, 4, size=20)
        # Compute a linear regression trend using SciPy
        slope, intercept, r_value, _, _ = stats.linregress(days, history)
        trend = slope * days + intercept

        self.ax.clear()
        self.ax.plot(days, history, 'o-', label="Occupancy (%)")
        self.ax.plot(days, trend, 'r--', label=f"Trend (r={r_value:.2f})")
        self.ax.set_title("Apartment Occupancy (Current: {:.1f}%)".format(occupancy_pct))
        self.ax.set_xlabel("Day")
        self.ax.set_ylabel("Occupancy (%)")
        self.ax.legend()
        self.canvas.draw()
