import keyboard
from crosshair_window import CrosshairWindow

class CrosshairManager:
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
        self.crosshair_window = None
        self.last_settings = self.settings_manager.settings.copy()

    def toggle_crosshair(self):
        if self.crosshair_window is None:
            self.crosshair_window = CrosshairWindow(self.settings_manager)
        else:
            self.crosshair_window.destroy()
            self.crosshair_window = None

    def update_crosshair(self):
        current_settings = self.settings_manager.settings
        if self.crosshair_window and current_settings != self.last_settings:
            self.crosshair_window.update_crosshair()
            self.last_settings = current_settings.copy()

    def is_active(self):
        return self.crosshair_window is not None