import tkinter as tk
from tkinter import ttk
from dataset import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

# Load your dataset (replace with your actual dataset loader)
astrolore = astrolore_dataset()

# Constants for styling
HEADER_FONT = ("Helvetica", 28, "bold", "italic")
LABEL_FONT = ("Helvetica", 16, "italic")
OUTPUT_FONT = ("Helvetica", 12)
TEXT_FONT = ("Helvetica", 12)
RADIO_FONT = ("Menlo", 13, "bold", "italic")
BG_COLOR = "#000000"  # matches dark background with overlay

# Initialize main window
window = tk.Tk()
window.title("AstroLore")
window.geometry("800x600")
window.resizable(False, False)

# Load and resize background image (change path to your actual image)
bg_image = Image.open("background.png")
bg_image = bg_image.resize((800, 600), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
window.bg_photo = bg_photo  # prevent GC

# Create canvas with background image
canvas = tk.Canvas(window, width=800, height=600, highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)
canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo)

# Semi-transparent black overlay rectangle for UI clarity
canvas.create_rectangle(150, 100, 650, 500, fill="black", stipple="gray50", outline="")

# Container frame centered on canvas with dark background
frame = tk.Frame(canvas, bg=BG_COLOR)
canvas.create_window((400, 300), window=frame, anchor="center")

# Title and description labels
title = tk.Label(frame, text="✨ AstroLore ✨", font=HEADER_FONT, fg="white", bg=BG_COLOR)
title.pack(pady=(0, 5))

subtitle = tk.Label(
    frame,
    text="Welcome to AstroLoreBot v1.0!\nGiven an astrophysical object of your choice,\n"
         "I output the nearest object on the sky referenced in sci-fi.",
    font=LABEL_FONT,
    fg="white",
    bg=BG_COLOR,
    justify="center",
    wraplength=400,
    padx=20,
    pady=20,
)
subtitle.pack(pady=(0, 10))

# Search mode selection
search_label = tk.Label(frame, text="Search by:", font=LABEL_FONT, fg="white", bg=BG_COLOR)
search_label.pack(pady=10)

mode_input_var = tk.StringVar(value="name")

radio_frame = tk.Frame(frame, bg=BG_COLOR)
radio_frame.pack()

name_radio = tk.Radiobutton(
    radio_frame, text="Name", variable=mode_input_var, value="name",
    font=RADIO_FONT, fg="white", bg=BG_COLOR, selectcolor=BG_COLOR, activebackground=BG_COLOR,
    command=lambda: update_input_mode()
)
name_radio.pack(side=tk.LEFT, padx=(5,5))

coord_radio = tk.Radiobutton(
    radio_frame, text="Coordinates (RA/DEC)", variable=mode_input_var, value="coords",
    font=RADIO_FONT, fg="white", bg=BG_COLOR, selectcolor=BG_COLOR, activebackground=BG_COLOR,
    command=lambda: update_input_mode()
)
coord_radio.pack(side=tk.LEFT, padx=10)

# Input frame for name or coordinate entries
input_frame = tk.Frame(frame, bg=BG_COLOR)
input_frame.pack(pady=10)

# Name entry (default)
name_entry = tk.Entry(input_frame, font=TEXT_FONT, justify="center", width=35)
name_entry.pack()

# RA inputs: h, m, s
ra_frame = tk.Frame(input_frame, bg=BG_COLOR)
ra_h = ttk.Entry(ra_frame, width=5)
ra_m = ttk.Entry(ra_frame, width=5)
ra_s = ttk.Entry(ra_frame, width=5)
tk.Label(ra_frame, text="RA:", font=RADIO_FONT, fg="white", bg=BG_COLOR).pack(side="left", padx=5)
ra_h.pack(side="left")
tk.Label(ra_frame, text="h", font=RADIO_FONT, fg="white", bg=BG_COLOR).pack(side="left")
ra_m.pack(side="left")
tk.Label(ra_frame, text="m", font=RADIO_FONT, fg="white", bg=BG_COLOR).pack(side="left")
ra_s.pack(side="left")
tk.Label(ra_frame, text="s", font=RADIO_FONT, fg="white", bg=BG_COLOR).pack(side="left")

# DEC inputs: deg, arcmin, arcsec
dec_frame = tk.Frame(input_frame, bg=BG_COLOR)
dec_d = ttk.Entry(dec_frame, width=5)
dec_m = ttk.Entry(dec_frame, width=5)
dec_s = ttk.Entry(dec_frame, width=5)
tk.Label(dec_frame, text="DEC:", font=RADIO_FONT, fg="white", bg=BG_COLOR).pack(side="left", padx=5)
dec_d.pack(side="left")
tk.Label(dec_frame, text="°", font=RADIO_FONT, fg="white", bg=BG_COLOR).pack(side="left")
dec_m.pack(side="left")
tk.Label(dec_frame, text="′", font=RADIO_FONT, fg="white", bg=BG_COLOR).pack(side="left")
dec_s.pack(side="left")
tk.Label(dec_frame, text="″", font=RADIO_FONT, fg="white", bg=BG_COLOR).pack(side="left")

# Initially hide coordinate inputs
ra_frame.pack_forget()
dec_frame.pack_forget()

# Output label for results
output = tk.Label(frame, font=OUTPUT_FONT, fg="white", bg=BG_COLOR, wraplength=400, justify="center")
output.pack(pady=(10, 5), fill=tk.X)

# Buttons Frame
buttons_frame = tk.Frame(frame, bg=BG_COLOR)
buttons_frame.pack(pady=10)

# Search button
button_state = tk.StringVar(value="process")

def reset_all():
    name_entry.delete(0, tk.END)
    ra_h.delete(0, tk.END)
    ra_m.delete(0, tk.END)
    ra_s.delete(0, tk.END)
    dec_d.delete(0, tk.END)
    dec_m.delete(0, tk.END)
    dec_s.delete(0, tk.END)
    output.config(text="")
    mode_input_var.set("name")
    update_input_mode()
    reset_button.pack_forget()
    plot_button.pack_forget()
    visualize_button.pack_forget()

def update_input_mode():
    output.config(text="")
    button.config(text="Search")
    button_state.set("process")
    plot_button.pack_forget()
    visualize_button.pack_forget()

    for widget in input_frame.winfo_children():
        widget.pack_forget()

    if mode_input_var.get() == "name":
        name_entry.pack()
    else:
        ra_frame.pack(pady=5)
        dec_frame.pack(pady=5)

# Plot button to show sample plot

def show_plot(get_fig_func):
    # Create a new pop-up window
    plot_window = tk.Toplevel(window)
    plot_window.title("Full Sky Map")
    plot_window.geometry("800x600")

    # Get figure from function
    fig, ax = get_fig_func

    # Embed plot in the pop-up window
    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    #ttk.Button(plot_window, text="Close", command=plot_window.destroy).pack(pady=5)



plot_button = ttk.Button(buttons_frame, text="Full Sky Plot", command=show_plot)

# Visualize button for sky observation
visualize_button = ttk.Button(buttons_frame, text="View in Aladin", command=astrolore.aladin_webview)

def handle_click():
    if button_state.get() == "process":
        try:
            if mode_input_var.get() == "name":
                name = name_entry.get().strip()
                if not name:
                    output.config(text="Please enter a name.")
                    return
                closest_object = astrolore.find_closest_object(name=name, coords=None)
            else:
                try:
                    h = int(ra_h.get())
                    m = int(ra_m.get())
                    s = float(ra_s.get())
                    d = int(dec_d.get())
                    am = int(dec_m.get())
                    asec = float(dec_s.get())
                    ra_str = f"{h}h{m}m{s}s"
                    dec_str = f"{d}d{am}m{asec}s"
                    coords = (ra_str, dec_str)
                    closest_object = astrolore.find_closest_object(name=None, coords=coords)
                except Exception:
                    output.config(text="Invalid coordinates, please try again (Hint: ICRS)")
                    return

            lore = astrolore.output_lore(closest_object)
            output.config(text=lore)
            plot_button.config(command=lambda: show_plot(astrolore.get_catalog_map()))
            plot_button.pack(side=tk.LEFT, padx=5)
            visualize_button.pack(side=tk.LEFT, padx=5)

            button.config(text="Search Again")
            button_state.set("reset")
            reset_button.pack(side=tk.LEFT, padx=5)

        except Exception:
            output.config(text="It's dark out here...\nMaybe verify the spelling?")
            plot_button.pack_forget()
            visualize_button.pack_forget()

    else:
        reset_all()
        button.config(text="Search")
        button_state.set("process")

button = ttk.Button(buttons_frame, text="Search", command=handle_click)
button.pack(side=tk.LEFT, padx=5)

reset_button = ttk.Button(buttons_frame, text="Reset", command=reset_all)
reset_button.pack_forget()

# Bind Enter key to search
window.bind('<Return>', lambda event: handle_click())

# Start with correct input mode
update_input_mode()


def on_closing():
    window.destroy()
    window.quit()  # Ensures the mainloop stops and the process exits

window.protocol("WM_DELETE_WINDOW", on_closing)



# Run main loop
window.mainloop()


