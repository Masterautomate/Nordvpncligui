import sys
import subprocess
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox, QTextEdit, QHBoxLayout, QCheckBox, QLineEdit)

class NordVPNGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.populate_countries()
        self.populate_groups()
        self.update_status()
        self.display_account_info()
        self.load_settings()
    
    def initUI(self):
        self.setWindowTitle("NordVPN GUI 4 NordVPN CLI")
        self.setGeometry(100, 100, 600, 500)
        
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
        
        self.settings_label = QLabel("NordVPN Settings", self)
        self.killswitch_checkbox = QCheckBox("Enable Kill Switch", self)
        self.autoconnect_checkbox = QCheckBox("Enable Auto-Connect", self)
        self.firewall_checkbox = QCheckBox("Enable Firewall", self)
        self.notify_checkbox = QCheckBox("Enable Notifications", self)
        self.tray_checkbox = QCheckBox("Show Tray Icon", self)
        self.meshnet_checkbox = QCheckBox("Enable Meshnet", self)
        self.virtual_location_checkbox = QCheckBox("Enable Virtual Location", self)
        self.post_quantum_checkbox = QCheckBox("Enable Post-Quantum VPN", self)
        
        self.dns_input = QLineEdit(self)
        self.dns_input.setPlaceholderText("Enter custom DNS server")
        self.set_dns_button = QPushButton("Set DNS", self)
        self.set_dns_button.clicked.connect(self.set_dns)
        
        self.apply_settings_button = QPushButton("Apply Settings", self)
        self.apply_settings_button.clicked.connect(self.apply_settings)
        
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
        
        layout.addWidget(self.settings_label)
        layout.addWidget(self.killswitch_checkbox)
        layout.addWidget(self.autoconnect_checkbox)
        layout.addWidget(self.firewall_checkbox)
        layout.addWidget(self.notify_checkbox)
        layout.addWidget(self.tray_checkbox)
        layout.addWidget(self.meshnet_checkbox)
        layout.addWidget(self.virtual_location_checkbox)
        layout.addWidget(self.post_quantum_checkbox)
        
        dns_layout = QHBoxLayout()
        dns_layout.addWidget(self.dns_input)
        dns_layout.addWidget(self.set_dns_button)
        layout.addLayout(dns_layout)
        
        layout.addWidget(self.apply_settings_button)
        
        self.setLayout(layout)
    
    def run_command(self, command):
        try:
            result = subprocess.run(command.split(), capture_output=True, text=True)
            return result.stdout.strip()
        except Exception as e:
            return str(e)
    
    def set_dns(self):
        dns_value = self.dns_input.text().strip()
        if dns_value:
            self.run_command(f"nordvpn set dns {dns_value}")
    
    def apply_settings(self):
        settings = {
            "killswitch": self.killswitch_checkbox.isChecked(),
            "autoconnect": self.autoconnect_checkbox.isChecked(),
            "firewall": self.firewall_checkbox.isChecked(),
            "notify": self.notify_checkbox.isChecked(),
            "tray": self.tray_checkbox.isChecked(),
            "meshnet": self.meshnet_checkbox.isChecked(),
            "virtual-location": self.virtual_location_checkbox.isChecked(),
            "post-quantum": self.post_quantum_checkbox.isChecked()
        }
        for key, value in settings.items():
            self.run_command(f"nordvpn set {key} {'on' if value else 'off'}")

    def load_settings(self):
        settings_output = self.run_command("nordvpn settings")
        settings_map = {
            "Kill Switch": self.killswitch_checkbox,
            "Auto-connect": self.autoconnect_checkbox,
            "Firewall": self.firewall_checkbox,
            "Notify": self.notify_checkbox,
            "Tray": self.tray_checkbox,
            "Meshnet": self.meshnet_checkbox,
            "Virtual Location": self.virtual_location_checkbox,
            "Post-quantum VPN": self.post_quantum_checkbox
        }
        
        for line in settings_output.split('\n'):
            key, _, value = line.partition(": ")
            if key in settings_map:
                settings_map[key].setChecked(value.strip().lower() == "enabled")
    
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
    
    def display_account_info(self):
        output = self.run_command("nordvpn account")
        self.account_label.setText(f"Account: {output.splitlines()[1] if output else 'Unavailable'}")
    
    def populate_countries(self):
        output = self.run_command("nordvpn countries")
        countries = output.split() if output else []
        self.country_combo.clear()
        self.country_combo.addItems(countries)
    
    def populate_cities(self):
        selected_country = self.country_combo.currentText()
        if selected_country:
            output = self.run_command(f"nordvpn cities {selected_country}")
            cities = output.split() if output else []
            self.city_combo.clear()
            self.city_combo.addItems(cities)
    
    def populate_groups(self):
        output = self.run_command("nordvpn groups")
        groups = output.split() if output else []
        self.group_combo.clear()
        self.group_combo.addItems(groups)
    
    def update_status(self):
        status_output = self.run_command("nordvpn status")
        self.status_text.setText(status_output)
        if "Connected" in status_output:
            self.status_label.setText(f"Status: {status_output.splitlines()[1] if status_output else 'Disconnected'}")
        else:
            self.status_label.setText("Status: Disconnected")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NordVPNGUI()
    window.show()
    sys.exit(app.exec())
