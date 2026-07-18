class App:
    def get_extension_manager(self):
        return ExtensionManager()

class ExtensionManager:
    def set_extension_enabled_immediate(self, name, enabled):
        print(f"Extension {name} set to {enabled}")
        return True

def get_app():
    return App()
