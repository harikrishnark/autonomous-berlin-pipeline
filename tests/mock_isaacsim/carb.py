class Settings:
    def set(self, name, value):
        print(f"Carb setting {name} set to {value}")
        return True

class SettingsManager:
    def get_settings(self):
        return Settings()

settings = SettingsManager()
