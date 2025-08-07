import tkinter as tk
from tkinter import ttk
from dataset import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

astrolore = astrolore_dataset()

# URL for AladinLite viewer (example static, you might want to generate this dynamically)



# Create main window
window = tk.Tk()
window.title("AstroLore Finder")
#window.geometry("800x600")  # Set initial size
window.resizable(True, True)

# Fonts
HEADER_FONT = ("Helvetica", 28, "bold", "italic")
radio_button_font = ("Menlo", 13, "bold", "italic")

# Frame for padding
frame = ttk.Frame(window, padding="15 15 15 15")
frame.pack(fill=tk.BOTH, expand=True)

# Title
title = tk.Label(frame, text="✨ AstroLore ✨", font=HEADER_FONT)
title.pack(pady=(0, 3))

subtitle = tk.Label(
    frame,
    wraplength=420,
    text='Welcome to AstroLoreBot v1.0!\nGiven an astrophysical object of your choice,\nI output the nearest object on the sky referenced in sci-fi.',
    justify="center",
    padx=15,
    pady=15
)
subtitle.pack(pady=(5, 5), fill=tk.X)

label = tk.Label(frame, text="Search by:")
label.pack(pady=(0, 3))

mode_input_var = tk.StringVar(value='name')

def update_input_mode():
    
    # Reset output and UI state
    output.config(text="")
    button.config(text="Search")
    button_state.set("process")
    plot_button.pack_forget()
    visualize_button.pack_forget()


    for widget in input_frame.winfo_children():
        widget.pack_forget()
    if mode_input_var.get() == "name":
        name_entry.pack(pady=5)
    else:
        ra_frame.pack(pady=5)
        dec_frame.pack(pady=5)

# Radio buttons to choose mode
frame_buttons = tk.Frame(frame)
ttk.Radiobutton(frame_buttons, text="Name", variable=mode_input_var, value="name", command=update_input_mode).pack(side="left", padx=10)
ttk.Radiobutton(frame_buttons, text="Coordinates (RA/DEC)", variable=mode_input_var, value="coords", command=update_input_mode).pack(side="left", padx=10)
frame_buttons.pack(pady=5)

input_frame = tk.Frame(frame)
input_frame.pack()

# RA inputs: h, m, s
ra_frame = tk.Frame(input_frame)
ra_h = ttk.Entry(ra_frame, width=5)
ra_m = ttk.Entry(ra_frame, width=5)
ra_s = ttk.Entry(ra_frame, width=5)
tk.Label(ra_frame, text="RA:",font=radio_button_font).pack(side="left", padx=5)
ra_h.pack(side="left")
tk.Label(ra_frame, text="h",font=radio_button_font).pack(side="left")
ra_m.pack(side="left")
tk.Label(ra_frame, text="m",font=radio_button_font).pack(side="left")
ra_s.pack(side="left")
tk.Label(ra_frame, text="s",font=radio_button_font).pack(side="left")

# DEC inputs: deg, arcmin, arcsec
dec_frame = tk.Frame(input_frame)
dec_d = ttk.Entry(dec_frame, width=5)
dec_m = ttk.Entry(dec_frame, width=5)
dec_s = ttk.Entry(dec_frame, width=5)
tk.Label(dec_frame, text="DEC:",font=radio_button_font).pack(side="left", padx=0)
dec_d.pack(side="left")
tk.Label(dec_frame, text="°",font=radio_button_font).pack(side="left")
dec_m.pack(side="left")
tk.Label(dec_frame, text="′",font=radio_button_font).pack(side="left")
dec_s.pack(side="left")
tk.Label(dec_frame, text="″",font=radio_button_font).pack(side="left")

name_entry = ttk.Entry(input_frame, width=30)
name_entry.pack()

def reset_all():
    # Reset fields
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


button_state = tk.StringVar(value="process")


visualize_button = ttk.Button(frame, text="View in Aladin", command=astrolore.aladin_webview)
visualize_button.config(state='normal')



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




plot_button = ttk.Button(frame, text="Full Sky Map", command=show_plot)


def handle_click():
    if button_state.get() == "process":
        try:
            if mode_input_var.get() == "name":
                
                button.config(text="Search")
                #button_state.set("process")
                name = name_entry.get()
                closest_object = astrolore.find_closest_object(name=name, coords=None)
                lore = astrolore.output_lore(closest_object)
                output.config(text=lore)
                # Define what to plot when Show Plot is clicked
         
                plot_button.config(command=lambda: show_plot(astrolore.get_catalog_map()))
                plot_button.pack(pady=(5,10))
                visualize_button.pack(pady=(5, 10))

            else:
                try:
                    button.config(text="Search")
                    #button_state.set("process")
                    h = int(ra_h.get())
                    m = int(ra_m.get())
                    s = float(ra_s.get())
                    d = int(dec_d.get())
                    am = int(dec_m.get())
                    asec = float(dec_s.get())
                    from astropy.coordinates import SkyCoord
                    import astropy.units as u
                    ra_str = f"{h}h{m}m{s}s"
                    dec_str = f"{d}d{am}m{asec}s"
                    coords = (ra_str, dec_str)
                    closest_object = astrolore.find_closest_object(name=None, coords=coords)
                    lore = astrolore.output_lore(closest_object)
                    output.config(text=lore)
                    plot_button.config(command=lambda: show_plot(astrolore.get_catalog_map()))
                    plot_button.pack(pady=(5,10))
                    visualize_button.pack(pady=(5, 10))
                except Exception as e:
                    output.config(text="Invalid coordinates, try again (Hint: ICRS)")
            button.config(text="Search Again")
            #button_state.set("reset")
            reset_button.pack(pady=(5, 10))

        except Exception as err:
            output.config(text="It's dark out here...\nMaybe verify the spelling?")
            plot_button.pack_forget()
            visualize_button.pack_forget()

    else:
        reset_all()
        button.config(text="Search Again")
        button_state.set("process")
    window.update_idletasks()
    window.geometry("")
    #window.geometry("800x700")  # Set initial size


button = ttk.Button(frame, text="Search", command=handle_click)
button.pack(pady=10)

window.bind('<Return>', lambda event: handle_click())



output = tk.Label(frame, wraplength=420, justify="center", anchor="center", padx=15, pady=20)
output.pack(pady=(5, 5), fill=tk.X)

reset_button = ttk.Button(frame, text="Reset", command=lambda: reset_all())
reset_button.pack(pady=(5, 10))
reset_button.pack_forget()  # Hidden by default




update_input_mode()


def on_closing():
    window.destroy()
    window.quit()  # Ensures the mainloop stops and the process exits

window.protocol("WM_DELETE_WINDOW", on_closing)



window.mainloop()
