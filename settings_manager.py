import json
import os
from constants import SETTINGS_FILE, DEFAULT_COLOR, DEFAULT_HOTKEY

class SettingsManager:
    def __init__(self):
        self.default_settings = {
            "shape": "stick_figure",
            "color": DEFAULT_COLOR,
            "scale": 1.0,
            "line_width": 3,
            "hotkey": DEFAULT_HOTKEY
        }
        self.settings = self.default_settings.copy()
        self.load()

    def save(self, key=None, value=None):
        if key and value:
            self.settings[key] = value
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def load(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r') as f:
                    loaded_settings = json.load(f)
                    if self.validate_settings(loaded_settings):
                        self.settings.update(loaded_settings)
                    else:
                        self.reset()
            except (json.JSONDecodeError, KeyError):
                self.reset()

    def validate_settings(self, settings):
        return all(k in self.default_settings and isinstance(settings.get(k), type(self.default_settings[k])) for k in settings)

    def reset(self):
        self.settings = self.default_settings.copy()
        self.save()