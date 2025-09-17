# Setting up Tkinter and the GUI window
from tkinter import *
from tkinter import ttk
screen = Tk()
screen.title("Tkinter AI GUI")
screen.geometry("400x400")
options = ["Text-to-Image", "Text-to-Speech"]

# Default Command
def doNothing():
    print("ok ok I won't...")

# Setting up the Menu
menu = Menu(screen)
screen.config(menu=menu)
subMenu = Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="New Project", command=doNothing)
subMenu.add_command(label="New...", command=doNothing)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=doNothing)

modelMenu = Menu(menu)
menu.add_cascade(label="Models", menu=modelMenu)
modelMenu.add_command(label="Redo", command=doNothing)

helpMenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpMenu)
helpMenu.add_command(label="Redo", command=doNothing)

#Toolbar
toolbar = Frame(screen, bg="white")

modelSelect = Label(toolbar, text="Model Selection: ", bg="white")
modelSelect.pack(side=LEFT, padx=2, pady=2)

combobox = ttk.Combobox(toolbar, values=options)
combobox.pack(side=LEFT, padx=2, pady=2)
combobox.set("Text-to-Image")
combobox = ttk.Combobox(screen, values=options, state="readonly")
selected_value = combobox.get()
def on_combobox_select(event):
    print("Selected: ", combobox.get())
combobox.bind("<<ComboboxSelected>>", on_combobox_select)

loadButton = Button(toolbar, text="Load Model", command=doNothing)
loadButton.pack(side=LEFT, padx=2, pady=2)
toolbar.pack(side=TOP, fill=X)

screen.mainloop()
