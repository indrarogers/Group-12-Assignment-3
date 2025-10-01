# Contains the Tkinter GUI classes. Shows usage of OOP: encapsulation, inheritance, and composition.
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
from utils import timing, simple_logger


class ScrollableFrame(ttk.Frame):
    """A reusable scrollable frame for Tkinter GUIs."""
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        # Make canvas expand with content
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        self._window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)


class AppGUI(ttk.Frame):
    def __init__(self, parent, model_manager):
        super().__init__(parent, padding=10)
        self.parent = parent
        self.manager = model_manager
        self._selected_model_key = tk.StringVar(value="Text-to-Image")
        self._input_type = tk.StringVar(value="Text")
        self._loaded_image = None  # keep reference to Tk image
        self._selected_path = None
        self._text_prompt = ""

        # Wrap everything in a scrollable container
        self.scrollable = ScrollableFrame(self)
        self.scrollable.pack(fill="both", expand=True)
        self.main_area = self.scrollable.scrollable_frame

        self._setup_widgets()
        simple_logger("GUI initialized.")

    def _setup_widgets(self):
        # ---------- Model Selection ----------
        model_frame = ttk.LabelFrame(self.main_area, text="Model Selection")
        model_frame.pack(fill="x", pady=5)
        self.model_combo = ttk.Combobox(
            model_frame,
            values=self.manager.available_models(),
            textvariable=self._selected_model_key,
            state="readonly"
        )
        self.model_combo.pack(side="left", padx=5, pady=5)
        self.model_combo.bind("<<ComboboxSelected>>", lambda e: self._update_info_display())
        load_btn = ttk.Button(model_frame, text="Load Model", command=self._load_model)
        load_btn.pack(side="left", padx=5)

        # ---------- Input ----------
        input_frame = ttk.LabelFrame(self.main_area, text="User Input")
        input_frame.pack(fill="x", pady=5)
        ttk.Radiobutton(input_frame, text="Text", variable=self._input_type, value="Text").pack(side="left", padx=5)
        ttk.Radiobutton(input_frame, text="Image", variable=self._input_type, value="Image").pack(side="left", padx=5)
        browse_btn = ttk.Button(input_frame, text="Browse", command=self._browse_file)
        browse_btn.pack(side="left", padx=5)
        self.run_btn = ttk.Button(input_frame, text="Run Model", command=self._run_model)
        self.run_btn.pack(side="left", padx=5)
        clear_btn = ttk.Button(input_frame, text="Clear Output", command=self._clear_output)
        clear_btn.pack(side="left", padx=5)

        # ---------- Output Display ----------
        out_frame = ttk.LabelFrame(self.main_area, text="Output Display")
        out_frame.pack(fill="both", expand=True, pady=5)
        self.output_text = tk.Text(out_frame, wrap="word", height=10)
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)

        # ---------- Image Preview ----------
        preview_frame = ttk.LabelFrame(self.main_area, text="Image Preview")
        preview_frame.pack(fill="x", pady=5)
        self.preview_label = ttk.Label(preview_frame, text="No image selected")
        self.preview_label.pack()

        # ---------- Model Info & OOP Explanation ----------
        info_frame = ttk.LabelFrame(self.main_area, text="Model Info & OOP Explanation")
        info_frame.pack(fill="x", pady=5)
        self.model_info_label = tk.Label(info_frame, text="", justify="left", anchor="w")
        self.model_info_label.pack(fill="x", padx=5, pady=5)

        self.oop_info_text = tk.Text(info_frame, height=8, wrap="word")
        self.oop_info_text.pack(fill="x", padx=5, pady=5)
        self._populate_oop_explanation()
        self._update_info_display()

    def _populate_oop_explanation(self):
        expl = (
            "OOP Concepts used in this project:\n"
            "- Multiple Inheritance: Model adapter classes (e.g., TextToImageModel, BlipCaptionModel) inherit from ModelInterface and LoggerMixin.\n"
            "- Multiple Decorators: utils.timing and utils.cached_result are applied to model load/run methods to measure time and cache results.\n"
            "- Encapsulation: model objects are stored in private attributes (e.g., self._model, self._loaded).\n"
            "- Polymorphism: ModelManager returns different model objects which share the same interface (load/run/info).\n"
            "- Method Overriding: Concrete models implement load/run/info overriding the abstract ModelInterface methods.\n"
        )
        self.oop_info_text.delete("1.0", "end")
        self.oop_info_text.insert("1.0", expl)

    def _update_info_display(self):
        model = self.manager.get_model(self._selected_model_key.get())
        if not model:
            self.model_info_label.config(text="No model selected")
            return
        info = model.info()
        text = f"Name: {info.get('name')}\nType: {info.get('type')}\nDescription: {info.get('description')}"
        self.model_info_label.config(text=text)

    def _load_model(self):
        model = self.manager.get_model(self._selected_model_key.get())
        if not model:
            messagebox.showerror("Error", "No model selected.")
            return
        try:
            model.load()
            messagebox.showinfo("Model Loaded", f"Model '{self._selected_model_key.get()}' loaded (or prepared).")
        except Exception as e:
            messagebox.showerror("Load Error", str(e))

    def _browse_file(self):
        if self._input_type.get() == "Image":
            path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")]
            )
            if path:
                self._show_image(path)
                self._selected_path = path
                self.output_text.insert("end", f"Selected file: {path}\n")
        else:
            self._selected_path = None
            prompt = simpledialog.askstring("Input Text", "Enter text prompt for the model:")
            if prompt:
                self._text_prompt = prompt
                self.output_text.insert("end", f"Text prompt set: {prompt}\n")

    def _show_image(self, path):
        try:
            img = Image.open(path)
            img.thumbnail((300, 300))
            self._loaded_image = ImageTk.PhotoImage(img)
            self.preview_label.config(image=self._loaded_image, text="")
        except Exception as e:
            self.preview_label.config(text=f"Failed to load image: {e}")

    @timing
    def _run_model(self):
        self.output_text.insert("end", "Running model...\n")
        model = self.manager.get_model(self._selected_model_key.get())
        if not model:
            self.output_text.insert("end", "No model available.\n")
            return
        try:
            if self._selected_model_key.get() == "Text-to-Image":
                prompt = getattr(self, "_text_prompt", "A scenic landscape with mountains and a river")
                res = model.run(prompt)
                if res.get("path"):
                    self.output_text.insert("end", f"Image generated and saved to: {res['path']}\n")
                    self._show_image(res['path'])
                else:
                    self.output_text.insert("end", f"Result: {res}\n")
            else:
                image_path = getattr(self, "_selected_path", None)
                if not image_path:
                    messagebox.showwarning("Input missing", "Please browse and select an image first.")
                    return
                res = model.run(image_path)
                self.output_text.insert("end", f"Caption: {res.get('caption')}\n")
        except Exception as e:
            self.output_text.insert("end", f"Model run failed: {e}\n")

    def _clear_output(self):
        self.output_text.delete("1.0", "end")

