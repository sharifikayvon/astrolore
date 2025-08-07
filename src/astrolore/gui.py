from astrolore.dataset import astrolore_dataset
import tkinter as tk
from tkinter import ttk

class main_gui():

    def __init__(self):
        self.dataset = astrolore_dataset()
        self._setup_window()
        self.setup_main_gui()

    def _setup_window(self):
        # Fonts
        self.window = tk.Tk()
        self.window.title("AstroLore Explorer")
        #window.geometry("500x500")  # Constrain size (width x height)
        self.window.resizable(True, True)  # Prevent resizing
        self.header_font = ("Helvetica", 28, "bold", "italic")

        self.frame = ttk.Frame(self.window, padding="15 15 15 15")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.title = tk.Label(self.frame, text="AstroLore", font=self.header_font)
        self.title.pack(pady=(0, 3))

    def setup_main_gui(self):
        subtitle = tk.Label(
            self.frame,
            wraplength=420,
            text='Welcome to AstroLoreBot v1.0!\nGiven an astrophysical object of your choice,\nI output the nearest object on the sky referenced in sci-fi.',
            justify="center",
            #font=OUTPUT_FONT,
            #anchor="w",
            #relief="sunken",
            padx=15,
            pady=15
        )
        subtitle.pack(pady=(5, 5), fill=tk.X)

        label = tk.Label(self.frame, text="Search by:")
        label.pack(pady=(0, 3))

        label = tk.Label(self.frame,text="Enter an Astrophysical Object:")
        label.pack(pady=(0, 6))

        self.entry_widget = ttk.Entry(self.frame, width=30)
        self.entry_widget.pack()

        self.entry_widget.bind("<Return>", self._handle_return)  
        button = ttk.Button(self.window, text="Process", command=self._handle_click)
        button.pack()

        self.output = tk.Label(
            self.frame,
            wraplength=420,
            justify="left",
            #font=OUTPUT_FONT,
            anchor="w",
            #relief="sunken",
            padx=15,
            pady=20
        )
        self.output.pack(pady=(5, 5), fill=tk.X)


    def start_gui(self):
        """Starts the GUI"""
        self.window.mainloop()


    def _handle_click(self):
        input = self.entry_widget.get()
        closest_object = self.dataset.find_closest_object(input)
        lore = self.dataset.output_lore(closest_object)
        #output = tk.Label(text=processor.process(input))
        self.output.config(text=lore)
        self.window.update_idletasks()  # Refresh layout
        self.window.geometry("")        # Resize to fit content


    def _handle_return(self, e):
        self._handle_click()
        self.window.update_idletasks()  # Refresh layout
        self.window.geometry("")        # Resize to fit content