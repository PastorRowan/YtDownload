
from kivymd.app import MDApp

def navigateToScreen(screenName: str) -> None:
    print("navigateToScreen called with: ", screenName)
    app = MDApp.get_running_app()
    app.screenManager.current = screenName
