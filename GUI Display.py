import tkinter as tk
from tkinter import ttk, filedialog

# Main window
root = tk.Tk()
root.title("Tkinter AI GUI")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

# ---------- Top Section: Model Selection ----------
model_frame = tk.LabelFrame(root, text="Model Selection", padx=10, pady=10)
model_frame.pack(fill="x", padx=10, pady=5)

model_var = tk.StringVar()
model_dropdown = ttk.Combobox(model_frame, textvariable=model_var)
model_dropdown['values'] = ["Text-to-Image", "Image-to-Text", "Audio-to-Text"]
model_dropdown.current(0)
model_dropdown.pack(side="left", padx=5)

load_button = tk.Button(model_frame, text="Load Model")
load_button.pack(side="left", padx=5)

# ---------- Input Section ----------
input_frame = tk.LabelFrame(root, text="User Input", padx=10, pady=10)
input_frame.pack(fill="x", padx=10, pady=5)

input_type = tk.StringVar(value="Text")
text_radio = tk.Radiobutton(input_frame, text="Text", variable=input_type, value="Text")
image_radio = tk.Radiobutton(input_frame, text="Image", variable=input_type, value="Image")
text_radio.pack(side="left", padx=5)
image_radio.pack(side="left", padx=5)

browse_button = tk.Button(input_frame, text="Browse", command=lambda: filedialog.askopenfilename())
browse_button.pack(side="left", padx=5)

run1_button = tk.Button(input_frame, text="Run Model 1")
run2_button = tk.Button(input_frame, text="Run Model 2")
clear_button = tk.Button(input_frame, text="Clear")
run1_button.pack(side="left", padx=5)
run2_button.pack(side="left", padx=5)
clear_button.pack(side="left", padx=5)

# ---------- Output Display ----------
output_frame = tk.LabelFrame(root, text="Output Display", padx=10, pady=10)
output_frame.pack(fill="both", expand=True, padx=10, pady=5)

output_label = tk.Label(output_frame, text="Results will appear here...", bg="white", anchor="nw", justify="left")
output_label.pack(fill="both", expand=True)

# ---------- Model Info ----------
info_frame = tk.LabelFrame(root, text="Selected Model Info", padx=10, pady=10)
info_frame.pack(fill="x", padx=10, pady=5)

tk.Label(info_frame, text="Model Name:").grid(row=0, column=0, sticky="w")
tk.Label(info_frame, text="Category:").grid(row=1, column=0, sticky="w")
tk.Label(info_frame, text="Short Description:").grid(row=2, column=0, sticky="w")

# ---------- OOP Explanation ----------
oop_frame = tk.LabelFrame(root, text="OOP Concepts Explanation", padx=10, pady=10)
oop_frame.pack(fill="x", padx=10, pady=5)

tk.Label(oop_frame, text="Where Multiple Inheritance is used").pack(anchor="w")
tk.Label(oop_frame, text="Why Encapsulation was applied").pack(anchor="w")
tk.Label(oop_frame, text="How Polymorphism and Abstraction are applied").pack(anchor="w")
tk.Label(oop_frame, text="Where Multiple Decorators are applied").pack(anchor="w")

# ---------- Notes ----------
notes_frame = tk.LabelFrame(root, text="Notes", padx=10, pady=10)
notes_frame.pack(fill="x", padx=10, pady=5)

notes_text = tk.Text(notes_frame, height=4)
notes_text.pack(fill="x")

# Run the app
root.mainloop()
