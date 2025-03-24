from controllers import PlayerController
from controllers import EventController
import tkinter as tk
class BaseView():
    def __init__(self, root,eventcontroller:EventController,playercontroller:PlayerController):
        self.eventcontroller = eventcontroller
        self.playercontroller = playercontroller
        self.root = root
        self.frame = tk.Frame(self.root)
        self.is_show=False

    def show(self):
        print('show frame')
        self.is_show=True
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        print('hide frame')
        self.is_show=False
        self.frame.pack_forget()