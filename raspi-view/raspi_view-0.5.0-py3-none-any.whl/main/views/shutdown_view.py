from main.view import View
from main.controller import Controller
import subprocess

class ShutdownView(View):
    def __init__(self, controller: Controller):
        super().__init__(controller)

    def update_display(self, canvas, bounding_box):
        canvas.text((40, 20), "Shutdown?", fill="white")
        canvas.text((0, 50), "Cancel", fill="white")
        canvas.text((110, 50), "OK", fill="white")

    def get_name(self):
        return "Test View"

    def button_pushed(self):
            cmd = "shutdown now"
            result = subprocess.check_output(cmd, shell=True).decode('ascii')[:-1]
