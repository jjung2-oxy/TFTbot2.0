import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow
from pynput.keyboard import Listener, KeyCode
import Files.screen_coords as screen_coords
import threaded_main as tm
import Files.interface as interface
import pyautogui

class OverlayApp:
    def __init__(self, screen_scaling=1, opacity=1):
        self.app = QApplication(sys.argv)
        self.screen_scaling = screen_scaling
        self.opacity = opacity
        self.custom_window = CustomWindow(self.app, self.screen_scaling, self.opacity)

    def run(self):
        self.custom_window.showFullScreen()
        self.custom_window.setWindowFlags(self.custom_window.windowFlags() | Qt.WindowStaysOnTopHint)
        self.custom_window.activateWindow()
        self.custom_window.raise_()
      
        print("Running OverlayApp...")
        sys.exit(self.app.exec_())

    def close_window(self):
        self.custom_window.close_window()
        self.app.quit()

class CustomWindow(QMainWindow):
    keyPressed = pyqtSignal(KeyCode)
    update_signal = pyqtSignal(list)

    def __init__(self, app, screen_scaling, opacity, parent=None):
        super().__init__(parent)
        self.update_signal.connect(self.update_overlay)
        self.listener = Listener(on_release=self.on_release)
        self.app = app
        self.screen_scaling = screen_scaling
        self.opacity = opacity
        self.target_champs = []
        self.curr_shop = []
        self.string_dict = {}  # Initialize with an empty dictionary
        self.champPool = {
            '1_cost': 29,
            '2_cost': 22,
            '3_cost': 18,
            '4_cost': 12
            # Add more if needed
        }
        self.static_dict = {
            1: [("ChampionA1", 5), ("ChampionB1", 3), ("ChampionC1", 2)],
            2: [("ChampionA2", 4), ("ChampionB2", 3)],
            3: [("ChampionA3", 6), ("ChampionB3", 4), ("ChampionC3", 1)],
            4: [("ChampionA4", 2), ("ChampionB4", 1)]
        }
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.listener.start()

    def update_overlay(self, stats_dict):
        self.string_dict = self.static_dict  # Update the data for the textbox
        self.update()  # Trigger a repaint

    def on_release(self, key):
        if hasattr(key, 'char') and key.char == 'd':
            self.shouldDraw = True
            self.update()

    def close_window(self):
        self.listener.stop()
        self.close()

    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setOpacity(self.opacity)
        self.highlight(painter)
        self.drawNewTextBox(painter, self.string_dict)  # Use the updated data
  # Reset the flag after drawing

    def highlight(self, painter):
        painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))
        for idx, champ in enumerate(self.curr_shop):
            if champ in self.target_champs:
                self.drawHighlightRectangle(painter, idx)

    def drawHighlightRectangle(self, painter, idx):
        spacing = round(screen_coords.CHAMP_SPACING * self.screen_scaling)
        x = round(screen_coords.CHAMP_LEFT * self.screen_scaling)
        y = round(screen_coords.CHAMP_TOP * self.screen_scaling)
        height = round((screen_coords.CHAMP_BOT - screen_coords.CHAMP_TOP) * self.screen_scaling)
        width = round((screen_coords.CHAMP_RIGHT - screen_coords.CHAMP_LEFT) * self.screen_scaling)
        painter.drawRect(x + (spacing * idx), y, width, height)

    def drawNewTextBox(self, painter, stats_dict):
        textbox_x, textbox_y = 10, 10
        textbox_width = 200  # Initial width, adjust as needed
        text_y_offset = 20
        y = textbox_y + text_y_offset

        # Calculate the required height of the textbox
        textbox_height = text_y_offset  # Start with the offset as initial height
        for cost, champs in stats_dict.items():
            textbox_height += text_y_offset  # Add space for the cost header
            textbox_height += len(champs) * text_y_offset  # Add space for each champion

        # Draw the textbox
        painter.setOpacity(1.0)  # Ensure full opacity for the textbox
        painter.setBrush(Qt.black)
        painter.setPen(QPen(Qt.white))
        painter.drawRect(textbox_x, textbox_y, textbox_width, textbox_height)

        # Set the font for the text
        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)

        # Draw the text inside the textbox
        y = textbox_y + text_y_offset
        for cost, champs in stats_dict.items():
            painter.drawText(textbox_x + 10, y, f"Top champions for cost {cost}:")
            y += text_y_offset
            for name, count in champs:
                remaining_champs = self.champPool[f'{cost}_cost'] - count
                painter.drawText(textbox_x + 10, y, f"  {name} - {count} tallied, {remaining_champs} remaining")
                y += text_y_offset



if __name__ == "__main__":
    overlay_app = OverlayApp(screen_scaling=1, opacity=0.8)
    overlay_app.run()
