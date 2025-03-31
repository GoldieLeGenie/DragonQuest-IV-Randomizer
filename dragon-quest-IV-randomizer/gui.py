from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QCheckBox, QLabel, QGroupBox, QTabWidget, QMessageBox)
from PySide6.QtCore import QPropertyAnimation, QRect
import sys
import os
import randomize_loot, randomize_mini_medals, randomize_monster, randomize_shop
import utils

class CompletionWindow(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Randomization Complete")
        self.setText("Randomization complete!")
        self.setIcon(QMessageBox.Information)
        self.setStandardButtons(QMessageBox.Ok)

class CustomGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dragon quest IV Beta-Randomizer")
        self.setGeometry(100, 100, 550, 400)
        self.setFixedSize(550, 400)
        self.options = {}
        
        self.setStyleSheet("""
            QWidget { background-color: #2c2f38; color: white; font-family: Arial; font-size: 11pt; }
            QGroupBox { background-color: #3b414d; border: 2px solid #5e8f44; border-radius: 5px; padding: 8px; }
            QPushButton { padding: 6px; background-color: #5e8f44; color: white; border-radius: 4px; }
            QPushButton:hover { background-color: #6a9f55; }
            QCheckBox, QLabel { padding: 2px; color: white; }
            QTabWidget::pane { background-color: #2c2f38; border: 1px solid #444; border-radius: 5px; }
            QTabBar::tab { background-color: #3b414d; padding: 6px; border-radius: 4px; }
            QTabBar::tab:selected { background-color: #5e8f44; }
        """)

        self.layout = QVBoxLayout()

        file_group = QGroupBox("File Selection")
        file_layout = QVBoxLayout()
        
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("font-weight: bold;")
        file_layout.addWidget(self.file_label)
        
        self.file_button = QPushButton("Choose a file")
        self.file_button.setStyleSheet("background-color: #3b5998; color: white; border-radius: 4px;")
        self.file_button.clicked.connect(self.choose_file)
        file_layout.addWidget(self.file_button)

        file_group.setLayout(file_layout)
        self.layout.addWidget(file_group)
        
        self.tabs = QTabWidget()
        self.tabs.setVisible(False)
        self.layout.addWidget(self.tabs)
        
        self.create_tab("Area", ["Randomize Monster", "Randomize Monster Drop", "Randomize Loot"])
        self.create_tab("Shop", ["Randomize Shop Price", "Randomize Shop Items"])
        self.create_tab("Other", ["Randomize Mini Medal Prize"])

        self.run_button = QPushButton("Randomize")
        self.run_button.setStyleSheet("background-color: #008000; color: white; border-radius: 4px;")
        self.run_button.clicked.connect(self.run_action)
        self.run_button.setVisible(False)
        self.layout.addWidget(self.run_button)
        
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-weight: bold; color: #5e8f44;")
        self.layout.addWidget(self.status_label)
        
        self.setLayout(self.layout)
        
        self.anim = QPropertyAnimation(self.run_button, b"geometry")
        self.run_button.enterEvent = self.animate_button_hover
        self.run_button.leaveEvent = self.animate_button_leave

    def animate_button_hover(self, event):
        self.anim.stop()
        self.anim.setDuration(200)
        self.anim.setStartValue(self.run_button.geometry())
        self.anim.setEndValue(QRect(self.run_button.x()-2, self.run_button.y()-2, self.run_button.width()+4, self.run_button.height()+4))
        self.anim.start()

    def animate_button_leave(self, event):
        self.anim.stop()
        self.anim.setDuration(200)
        self.anim.setStartValue(self.run_button.geometry())
        self.anim.setEndValue(QRect(self.run_button.x()+2, self.run_button.y()+2, self.run_button.width()-4, self.run_button.height()-4))
        self.anim.start()

    def create_tab(self, name, options):
        tab = QWidget()
        tab_layout = QVBoxLayout()
        group_box = QGroupBox(name)
        group_layout = QVBoxLayout()

        for opt_text in options:
            checkbox = QCheckBox(opt_text)
            self.options[opt_text.replace(" ", "_").lower()] = checkbox
            group_layout.addWidget(checkbox)

        group_box.setLayout(group_layout)
        tab_layout.addWidget(group_box)
        tab.setLayout(tab_layout)
        self.tabs.addTab(tab, name)

    def choose_file(self):
        nds_file, _ = QFileDialog.getOpenFileName(self, "Choose a file")
        if nds_file:
            self.file_label.setText(os.path.basename(nds_file))
            self.selected_file = nds_file
            self.tabs.setVisible(True)
            self.run_button.setVisible(True)

    def run_action(self):
        if not hasattr(self, 'selected_file') or not self.selected_file:
            self.status_label.setText("No file selected!")
            return

        if self.options["randomize_monster"].isChecked():
            randomize_monster.randomize_monsters("./param/param_encount_data.dat", "./data/param_encount_data.json", self.selected_file, 0xA1AE0)
        
        if self.options["randomize_mini_medal_prize"].isChecked():
            randomize_mini_medals.randomize_medal_prize("./param/param_map_medal.dat", self.selected_file, 0x5474800)
        
        if self.options["randomize_monster_drop"].isChecked():
            randomize_monster.randomize_monster_drop("./param/param_monster_monster.dat", "./data/param_monster_monster.json", self.selected_file, 0xA42E4)
            randomize_monster.randomize_monster_drop("./param/param_monster_monster.dat", "./data/param_monster_monster.json", self.selected_file, 0x5478200)
        
        if self.options["randomize_loot"].isChecked():
            directory = "./param/"
            file_list_and_pattern = utils.extract_pattern_from_files(directory)
            for filepath, pattern in file_list_and_pattern:
                start_offset = utils.find_offset(self.selected_file, pattern)
                randomize_loot.randomize_all_loot(filepath, self.selected_file, start_offset)
        
        if self.options["randomize_shop_price"].isChecked() or self.options["randomize_shop_items"].isChecked():
            json_path = "./data/shop_items.json"
            filepaths = {
                "./param/param_map_shop_first.dat": [0x9A964, 0x5474C00],
                "./param/param_map_shop_second.dat": [0x9FD9C, 0x5475C00]
            }

            price = self.options["randomize_shop_price"].isChecked()
            items = self.options["randomize_shop_items"].isChecked()

            for filepath, offsets in filepaths.items():
                randomize_shop.randomize_shop_price_and_items(filepath, json_path, self.selected_file, offsets, price=price, items=items)
        
        self.completion_window = CompletionWindow()
        self.completion_window.exec()

def start():
    app = QApplication(sys.argv)
    window = CustomGUI()
    window.show()
    sys.exit(app.exec())