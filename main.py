"""main.py
Entry point for the Tkinter AI GUI application.
"""
import tkinter as tk
from gui_components import AppGUI
from models import ModelManager

def main():
    root = tk.Tk()
    root.title("Tkinter AI GUI")
    root.geometry("1000x700")
    manager = ModelManager()
    app = AppGUI(root, manager)
    app.pack(fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()