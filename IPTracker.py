import sys
import requests
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTextEdit, QComboBox, QSystemTrayIcon,
    QMenu, QLabel, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QFormLayout, QCheckBox, QSpinBox, QProgressBar
)
from PyQt6.QtGui import QIcon, QFont, QAction, QPalette, QColor
from PyQt6.QtCore import Qt, QTranslator, QLocale, QSettings, QTimer
import os
from datetime import datetime
import sqlite3
import logging
from pathlib import Path
import re
import csv
import qdarkstyle
import threading
import queue

# Setup logging
logging.basicConfig(
    filename='ip_tracker.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumWidth(400)
        layout = QFormLayout()

        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Windows 11 Default", "Light", "Dark", "Red", "Blue"])
        layout.addRow("Theme:", self.theme_combo)

        # Language selection
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "فارسی", "中文"])
        layout.addRow("Language:", self.language_combo)

        # Auto-refresh settings
        self.auto_refresh = QCheckBox("Enable Auto-refresh")
        self.refresh_interval = QSpinBox()
        self.refresh_interval.setRange(1, 60)
        self.refresh_interval.setValue(5)
        self.refresh_interval.setSuffix(" minutes")
        layout.addRow("Auto-refresh:", self.auto_refresh)
        layout.addRow("Refresh Interval:", self.refresh_interval)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        layout.addRow(button_layout)
        self.setLayout(layout)

class IPTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("Hamid Yarali", "IPTracker")
        self.translator = QTranslator()
        self.current_language = self.settings.value("language", "English")
        self.current_theme = self.settings.value("theme", "Windows 11 Default")
        self.history = []
        self.lookup_queue = queue.Queue()
        self.init_db()
        self.init_ui()
        self.load_language(self.current_language)
        self.apply_theme(self.current_theme)
        self.setup_auto_refresh()

    def init_db(self):
        """Initialize SQLite database for storing IP lookup history"""
        home_dir = Path.home()
        db_path = home_dir / ".ip_tracker" / "history.db"
        db_path.parent.mkdir(exist_ok=True)
        
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT,
                country TEXT,
                city TEXT,
                latitude REAL,
                longitude REAL,
                timestamp TEXT
            )
        ''')
        self.conn.commit()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("IP Tracker")
        self.setMinimumSize(900, 700)
        self.setWindowIcon(QIcon("IPTracker.jpg"))  # Set window icon

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # IP Lookup Tab
        lookup_widget = QWidget()
        lookup_layout = QVBoxLayout(lookup_widget)
        
        # Input section
        input_layout = QHBoxLayout()
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter IP address (e.g., 8.8.8.8)")
        self.lookup_button = QPushButton("Lookup")
        self.lookup_button.clicked.connect(self.start_lookup_thread)
        self.ip_input.returnPressed.connect(self.start_lookup_thread)
        input_layout.addWidget(QLabel("IP Address:"))
        input_layout.addWidget(self.ip_input)
        input_layout.addWidget(self.lookup_button)
        lookup_layout.addLayout(input_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        lookup_layout.addWidget(self.progress_bar)

        # Result display
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        lookup_layout.addWidget(self.result_display)

        # History Tab
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels([
            "IP Address", "Country", "City", "Latitude", "Longitude", "Timestamp"
        ])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        for i in range(5):
            self.history_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)
        history_layout.addWidget(self.history_table)

        # History controls
        history_controls = QHBoxLayout()
        clear_history = QPushButton("Clear History")
        clear_history.clicked.connect(self.clear_history)
        export_history = QPushButton("Export to CSV")
        export_history.clicked.connect(self.export_history)
        history_controls.addWidget(clear_history)
        history_controls.addWidget(export_history)
        history_layout.addLayout(history_controls)

        # Add tabs
        self.tabs.addTab(lookup_widget, "IP Lookup")
        self.tabs.addTab(history_widget, "History")

        # System tray
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("IPTracker.jpg"))  # Set tray icon
        tray_menu = QMenu()
        show_action = QAction("Show", self)
        quit_action = QAction("Quit", self)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        file_menu.addAction(settings_action)
        file_menu.addAction(quit_action)

        # Status bar
        self.statusBar().showMessage("Ready")

        # Load history
        self.load_history()

    def load_language(self, language):
        """Load translation files"""
        if language == "فارسی":
            self.translator.load(":/translations/fa.qm")
            QApplication.instance().installTranslator(self.translator)
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        elif language == "中文":
            self.translator.load(":/translations/zh.qm")
            QApplication.instance().installTranslator(self.translator)
            self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        else:
            QApplication.instance().removeTranslator(self.translator)
            self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.update_ui_texts()

    def update_ui_texts(self):
        """Update UI texts based on current language"""
        language = self.current_language
        translations = {
            "English": {
                "window_title": "IP Tracker",
                "lookup_button": "Lookup",
                "clear_history": "Clear History",
                "export_history": "Export to CSV",
                "settings": "Settings",
                "quit": "Quit",
                "show": "Show",
                "tab_lookup": "IP Lookup",
                "tab_history": "History",
                "placeholder": "Enter IP address (e.g., 8.8.8.8)",
                "invalid_ip": "Invalid IP address format",
                "lookup_success": "Lookup successful",
                "lookup_failed": "Lookup failed",
                "network_error": "Network error",
                "history_cleared": "History cleared",
                "export_success": "History exported to {}",
                "export_failed": "Export failed: {}"
            },
            "فارسی": {
                "window_title": "ردیاب آی‌پی",
                "lookup_button": "جستجو",
                "clear_history": "پاک کردن تاریخچه",
                "export_history": "صادر کردن به CSV",
                "settings": "تنظیمات",
                "quit": "خروج",
                "show": "نمایش",
                "tab_lookup": "جستجوی آی‌پی",
                "tab_history": "تاریخچه",
                "placeholder": "آدرس آی‌پی را وارد کنید (مثال: 8.8.8.8)",
                "invalid_ip": "فرمت آدرس آی‌پی نامعتبر است",
                "lookup_success": "جستجو با موفقیت انجام شد",
                "lookup_failed": "جستجو ناموفق بود",
                "network_error": "خطای شبکه",
                "history_cleared": "تاریخچه پاک شد",
                "export_success": "تاریخچه به {} صادر شد",
                "export_failed": "خطا در صادرات: {}"
            },
            "中文": {
                "window_title": "IP追踪器",
                "lookup_button": "查询",
                "clear_history": "清除历史记录",
                "export_history": "导出到CSV",
                "settings": "设置",
                "quit": "退出",
                "show": "显示",
                "tab_lookup": "IP查询",
                "tab_history": "历史记录",
                "placeholder": "输入IP地址（例如：8.8.8.8）",
                "invalid_ip": "IP地址格式无效",
                "lookup_success": "查询成功",
                "lookup_failed": "查询失败",
                "network_error": "网络错误",
                "history_cleared": "历史记录已清除",
                "export_success": "历史记录导出到 {}",
                "export_failed": "导出失败：{}"
            }
        }

        self.setWindowTitle(translations[language]["window_title"])
        self.lookup_button.setText(translations[language]["lookup_button"])
        self.ip_input.setPlaceholderText(translations[language]["placeholder"])
        self.tabs.setTabText(0, translations[language]["tab_lookup"])
        self.tabs.setTabText(1, translations[language]["tab_history"])
        
        # Update menu actions
        for action in self.menuBar().actions()[0].menu().actions():
            if action.text() in ["Settings", "تنظیمات", "设置"]:
                action.setText(translations[language]["settings"])
            elif action.text() in ["Quit", "خروج", "退出"]:
                action.setText(translations[language]["quit"])

        # Update tray menu
        for action in self.tray_icon.contextMenu().actions():
            if action.text() in ["Show", "نمایش", "显示"]:
                action.setText(translations[language]["show"])
            elif action.text() in ["Quit", "خروج", "退出"]:
                action.setText(translations[language]["quit"])

    def apply_theme(self, theme):
        """Apply selected theme"""
        app = QApplication.instance()
        
        if theme == "Dark":
            app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt6'))
        elif theme == "Light":
            app.setStyleSheet("")
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
            app.setPalette(palette)
        elif theme == "Red":
            app.setStyleSheet("""
                QWidget { background-color: #ffe6e6; color: #800000; }
                QLineEdit, QTextEdit { background-color: #ffffff; border: 1px solid #800000; }
                QPushButton { background-color: #ff3333; color: white; }
                QPushButton:hover { background-color: #cc0000; }
                QTabWidget::pane { border: 1px solid #800000; }
                QTabBar::tab { background: #ff9999; color: #800000; }
                QTabBar::tab:selected { background: #ff3333; color: white; }
            """)
        elif theme == "Blue":
            app.setStyleSheet("""
                QWidget { background-color: #e6f3ff; color: #003366; }
                QLineEdit, QTextEdit { background-color: #ffffff; border: 1px solid #003366; }
                QPushButton { background-color: #0066cc; color: white; }
                QPushButton:hover { background-color: #003366; }
                QTabWidget::pane { border: 1px solid #003366; }
                QTabBar::tab { background: #99ccff; color: #003366; }
                QTabBar::tab:selected { background: #0066cc; color: white; }
            """)
        else:  # Windows 11 Default
            app.setStyleSheet("")
            app.setStyle("Fusion")
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, QColor(243, 243, 243))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.Button, QColor(225, 225, 225))
            app.setPalette(palette)

    def setup_auto_refresh(self):
        """Setup auto-refresh timer"""
        self.refresh_timer = QTimer()
        if self.settings.value("auto_refresh", False, type=bool):
            interval = self.settings.value("refresh_interval", 5, type=int) * 60 * 1000
            self.refresh_timer.timeout.connect(self.start_lookup_thread)
            self.refresh_timer.start(interval)

    def start_lookup_thread(self):
        """Start IP lookup in a separate thread"""
        ip_address = self.ip_input.text().strip()
        if not ip_address:
            return

        self.lookup_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.statusBar().showMessage("Looking up IP...")

        thread = threading.Thread(target=self.perform_lookup, args=(ip_address,))
        thread.daemon = True
        thread.start()

        # Check thread result periodically
        self.check_thread_timer = QTimer()
        self.check_thread_timer.timeout.connect(self.check_lookup_result)
        self.check_thread_timer.start(100)

    def perform_lookup(self, ip_address):
        """Perform IP lookup and put result in queue"""
        if not self.validate_ip(ip_address):
            self.lookup_queue.put(("error", "Invalid IP address format", ip_address))
            return

        try:
            url = f'http://ip-api.com/json/{ip_address}'
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            if data['status'] == 'success':
                result = (
                    f"IP: {ip_address}\n"
                    f"Country: {data['country']}\n"
                    f"City: {data['city']}\n"
                    f"Latitude: {data['lat']}\n"
                    f"Longitude: {data['lon']}\n"
                    f"ISP: {data.get('isp', 'N/A')}\n"
                    f"Organization: {data.get('org', 'N/A')}\n"
                    f"Timezone: {data.get('timezone', 'N/A')}"
                )
                self.lookup_queue.put(("success", result, ip_address, data.get('lat'), data.get('lon'), data.get('country'), data.get('city')))
            else:
                self.lookup_queue.put(("error", "Unable to retrieve location information", ip_address))
        except requests.RequestException as e:
            self.lookup_queue.put(("error", f"Error: {str(e)}", ip_address))

    def check_lookup_result(self):
        """Check lookup thread result"""
        try:
            result = self.lookup_queue.get_nowait()
            status, message, ip_address = result[:3]
            extra = result[3:] if len(result) > 3 else [None] * 4

            self.lookup_button.setEnabled(True)
            self.progress_bar.setVisible(False)
            self.check_thread_timer.stop()

            translations = {
                "English": {
                    "invalid_ip": "Invalid IP address format",
                    "lookup_success": "Lookup successful",
                    "lookup_failed": "Lookup failed",
                    "network_error": "Network error"
                },
                "فارسی": {
                    "invalid_ip": "فرمت آدرس آی‌پی نامعتبر است",
                    "lookup_success": "جستجو با موفقیت انجام شد",
                    "lookup_failed": "جستجو ناموفق بود",
                    "network_error": "خطای شبکه"
                },
                "中文": {
                    "invalid_ip": "IP地址格式无效",
                    "lookup_success": "查询成功",
                    "lookup_failed": "查询失败",
                    "network_error": "网络错误"
                }
            }

            self.result_display.setText(message)
            if status == "success":
                self.statusBar().showMessage(translations[self.current_language]["lookup_success"])
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                latitude, longitude, country, city = extra
                if latitude is not None and longitude is not None:
                    self.cursor.execute('''
                        INSERT INTO history (ip_address, country, city, latitude, longitude, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (ip_address, country, city, latitude, longitude, timestamp))
                    self.conn.commit()
                    
                    self.history.append({
                        'ip': ip_address,
                        'country': country,
                        'city': city,
                        'latitude': latitude,
                        'longitude': longitude,
                        'timestamp': timestamp
                    })
                    self.update_history_table()
                logging.info(f"Successful lookup for IP: {ip_address}")
            elif message == "Invalid IP address format":
                self.statusBar().showMessage(translations[self.current_language]["invalid_ip"])
                logging.error(f"Invalid IP address entered: {ip_address}")
            elif message == "Unable to retrieve location information":
                self.statusBar().showMessage(translations[self.current_language]["lookup_failed"])
                logging.error(f"Failed lookup for IP: {ip_address}")
            else:
                self.statusBar().showMessage(translations[self.current_language]["network_error"])
                logging.error(f"Network error during lookup for IP: {ip_address} - {message}")
                
        except queue.Empty:
            pass

    def validate_ip(self, ip_address):
        """Validate IP address format"""
        ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return bool(re.match(ip_pattern, ip_address))

    def load_history(self):
        """Load history from database"""
        self.history_table.setRowCount(0)
        self.cursor.execute("SELECT ip_address, country, city, latitude, longitude, timestamp FROM history ORDER BY timestamp DESC")
        for row_data in self.cursor.fetchall():
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)
            for col, data in enumerate(row_data):
                self.history_table.setItem(row, col, QTableWidgetItem(str(data)))

    def clear_history(self):
        """Clear lookup history"""
        translations = {
            "English": {"history_cleared": "History cleared"},
            "فارسی": {"history_cleared": "تاریخچه پاک شد"},
            "中文": {"history_cleared": "历史记录已清除"}
        }
        self.cursor.execute("DELETE FROM history")
        self.conn.commit()
        self.history_table.setRowCount(0)
        self.statusBar().showMessage(translations[self.current_language]["history_cleared"])
        logging.info("History cleared")

    def export_history(self):
        """Export history to CSV"""
        translations = {
            "English": {"export_success": "History exported to {}", "export_failed": "Export failed: {}"},
            "فارسی": {"export_success": "تاریخچه به {} صادر شد", "export_failed": "خطا در صادرات: {}"},
            "中文": {"export_success": "历史记录导出到 {}", "export_failed": "导出失败：{}"}
        }
        try:
            home_dir = Path.home()
            export_path = home_dir / "ip_history.csv"
            with open(export_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["IP Address", "Country", "City", "Latitude", "Longitude", "Timestamp"])
                self.cursor.execute("SELECT ip_address, country, city, latitude, longitude, timestamp FROM history")
                writer.writerows(self.cursor.fetchall())
            self.statusBar().showMessage(translations[self.current_language]["export_success"].format(export_path))
            logging.info(f"History exported to {export_path}")
        except Exception as e:
            self.statusBar().showMessage(translations[self.current_language]["export_failed"].format(str(e)))
            logging.error(f"Export failed: {str(e)}")

    def update_history_table(self):
        """Update history table display"""
        self.load_history()

    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self)
        dialog.theme_combo.setCurrentText(self.current_theme)
        dialog.language_combo.setCurrentText(self.current_language)
        dialog.auto_refresh.setChecked(self.settings.value("auto_refresh", False, type=bool))
        dialog.refresh_interval.setValue(self.settings.value("refresh_interval", 5, type=int))
        
        if dialog.exec():
            new_theme = dialog.theme_combo.currentText()
            new_language = dialog.language_combo.currentText()
            auto_refresh = dialog.auto_refresh.isChecked()
            refresh_interval = dialog.refresh_interval.value()

            self.settings.setValue("theme", new_theme)
            self.settings.setValue("language", new_language)
            self.settings.setValue("auto_refresh", auto_refresh)
            self.settings.setValue("refresh_interval", refresh_interval)

            if new_theme != self.current_theme:
                self.current_theme = new_theme
                self.apply_theme(new_theme)
            
            if new_language != self.current_language:
                self.current_language = new_language
                self.load_language(new_language)

            if auto_refresh:
                self.refresh_timer.start(refresh_interval * 60 * 1000)
            else:
                self.refresh_timer.stop()

    def closeEvent(self, event):
        """Handle window close event"""
        event.ignore()
        self.hide()
        translations = {
            "English": "Application minimized to system tray",
            "فارسی": "برنامه به سینی سیستم مینیمایز شد",
            "中文": "应用程序已最小化到系统托盘"
        }
        self.tray_icon.showMessage(
            "IP Tracker",
            translations[self.current_language],
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    app.setWindowIcon(QIcon("IPTracker.jpg"))  # Set application icon (favicon)
    
    tracker = IPTracker()
    tracker.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()