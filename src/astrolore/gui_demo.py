import tkinter as tk
from tkinter import ttk
from scifistarfinder import *



astrolore = AstroLore()

# Create main window
window = tk.Tk()
window.title("AstroLore Explorer")
#window.geometry("500x500")  # Constrain size (width x height)
window.resizable(True, True)  # Prevent resizing


# Fonts
HEADER_FONT = ("Helvetica", 28, "bold", "italic")




# Frame for padding
frame = ttk.Frame(window, padding="15 15 15 15")
frame.pack(fill=tk.BOTH, expand=True)


# Title
title = tk.Label(frame, text="AstroLore", font=HEADER_FONT)
title.pack(pady=(0, 3))

subtitle = tk.Label(
    frame,
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

label = tk.Label(frame, text="Search by:")
label.pack(pady=(0, 3))


input_frame = tk.Frame(frame)



label = tk.Label(frame,text="Enter an Astrophysical Object:")
label.pack(pady=(0, 6))



e = ttk.Entry(frame, width=30)
e.pack()


#name = entry.get()


def handle_click():
    input_text = e.get()
    try:
        closest_star = astrolore.closest_star_finder(input_text)
        output.config(text=closest_star)
    except Exception as err:
        output.config(text=f"It's dark out here...\nMaybe verify the spelling?")


    window.update_idletasks()  # Refresh layout
    window.geometry("")        # Resize to fit content

def handle_return(e):
    try:
        handle_click()
    except Exception as err:
        output.config(text=f"It's dark out here...\nMaybe verify the spelling?")

    window.update_idletasks()  # Refresh layout
    window.geometry("")        # Resize to fit content


button = ttk.Button(window, text="Process", command=handle_click)
e.bind("<Return>", handle_return)  



button.pack()


output = tk.Label(
    frame,
    wraplength=420,
    justify="center",      # Center text lines
    anchor="center",       # Center the label in the frame
    padx=15,
    pady=20
)

output.pack(pady=(5, 5), fill=tk.X)



window.mainloop()



'''a = AstroLore()
closest_star = a.closest_star_finder('pleione')
print(closest_star)
#a.visualize()'''