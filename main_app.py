import sys
import keyboard
from settings_manager import SettingsManager
from crosshair_manager import CrosshairManager
from main_app_ui import MainAppUI
import customtkinter as ctk

class MainApp:
    def __init__(self):
        self.settings_manager = SettingsManager()
        self.crosshair_manager = CrosshairManager(self.settings_manager)
        self.ui = MainAppUI(self)  # Pass self (MainApp instance) to the UI
        self.setup_hotkeys()

    def run(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.ui.mainloop()

    def toggle_crosshair(self):
        self.crosshair_manager.toggle_crosshair()
        self.ui.update_toggle_button_text()

    def reset_settings(self):
        self.settings_manager.reset()
        self.ui.update_ui_from_settings()
        self.crosshair_manager.update_crosshair()

    def close_application(self):
        self.settings_manager.save()
        if self.crosshair_manager.crosshair_window:
            self.crosshair_manager.crosshair_window.destroy()
        self.ui.destroy()

    def setup_hotkeys(self):
        try:
            keyboard.remove_hotkey(self.settings_manager.settings["hotkey"])
        except KeyError:
            pass  # Ignore if the hotkey doesn't exist
        keyboard.add_hotkey(self.settings_manager.settings["hotkey"], self.toggle_crosshair)

if __name__ == "__main__":
    app = MainApp()
    app.run()
