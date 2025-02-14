import sys
import subprocess
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox, QTextEdit, QHBoxLayout, QCheckBox)

class NordVPNGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.populate_countries()
        self.populate_groups()
        self.update_status()
        self.display_account_info()
    
    def initUI(self):
        self.setWindowTitle("NordVPN GUI NordVPN CLI")
        self.setGeometry(100, 100, 500, 400)
        
        self.account_label = QLabel("Account: Loading...", self)
        self.status_label = QLabel("Status: Checking...", self)
        
        self.country_combo = QComboBox(self)
        self.city_combo = QComboBox(self)
        self.group_combo = QComboBox(self)
        self.group_checkbox = QCheckBox("Use Server Group", self)
        
        self.connect_button = QPushButton("Connect", self)
        self.disconnect_button = QPushButton("Disconnect", self)
        self.refresh_button = QPushButton("Refresh Status", self)
        self.status_text = QTextEdit(self)
        self.status_text.setReadOnly(True)
        
        self.connect_button.clicked.connect(self.connect_vpn)
        self.disconnect_button.clicked.connect(self.disconnect_vpn)
        self.refresh_button.clicked.connect(self.update_status)
        self.country_combo.currentIndexChanged.connect(self.populate_cities)
        
        layout = QVBoxLayout()
        layout.addWidget(self.account_label)
        layout.addWidget(self.status_label)
        
        country_layout = QHBoxLayout()
        country_layout.addWidget(QLabel("Country:"))
        country_layout.addWidget(self.country_combo)
        layout.addLayout(country_layout)
        
        city_layout = QHBoxLayout()
        city_layout.addWidget(QLabel("City:"))
        city_layout.addWidget(self.city_combo)
        layout.addLayout(city_layout)
        
        group_layout = QHBoxLayout()
        group_layout.addWidget(QLabel("Server Group:"))
        group_layout.addWidget(self.group_combo)
        group_layout.addWidget(self.group_checkbox)
        layout.addLayout(group_layout)
        
        layout.addWidget(self.connect_button)
        layout.addWidget(self.disconnect_button)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.status_text)
        
        self.setLayout(layout)
    
    def run_command(self, command):
        try:
            result = subprocess.run(command.split(), capture_output=True, text=True)
            return result.stdout.strip()
        except Exception as e:
            return str(e)
    
    def display_account_info(self):
        output = self.run_command("nordvpn account")
        self.account_label.setText(f"Account: {output.splitlines()[1]}")
    
    def format_list(self, raw_output):
        """Ensures list items are in a single row rather than spread across multiple lines."""
        return [item.strip() for line in raw_output.split('\n') for item in line.split() if item.strip()]
    
    def populate_countries(self):
        output = self.run_command("nordvpn countries")
        countries = self.format_list(output)
        self.country_combo.addItems(countries)
    
    def populate_cities(self):
        selected_country = self.country_combo.currentText()
        if selected_country:
            output = self.run_command(f"nordvpn cities {selected_country}")
            cities = self.format_list(output)
            self.city_combo.clear()
            self.city_combo.addItems(cities)
    
    def populate_groups(self):
        output = self.run_command("nordvpn groups")
        groups = self.format_list(output)
        self.group_combo.addItems(groups)
    
    def connect_vpn(self):
        if self.group_checkbox.isChecked():
            selected_location = self.group_combo.currentText()
        else:
            selected_location = self.city_combo.currentText() or self.country_combo.currentText()
        
        if selected_location:
            self.run_command(f"nordvpn connect {selected_location}")
            self.update_status()
    
    def disconnect_vpn(self):
        self.run_command("nordvpn disconnect")
        self.update_status()
    
    def update_status(self):
        status_output = self.run_command("nordvpn status")
        self.status_text.setText(status_output)
        if "Connected" in status_output:
            self.status_label.setText(f"Status: {status_output.splitlines()[1]}")
        else:
            self.status_label.setText("Status: Disconnected")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NordVPNGUI()
    window.show()
    sys.exit(app.exec())
