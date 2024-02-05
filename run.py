# from eksekusi import eksekusi, output_history
from eksekusi import eksekusi

import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog

def compile_code():
    global outputDisplay
    code = code_text.get("1.0", tk.END)
    lines = code.split("\n")
    
    try:
        for line in lines:
            line = line.strip()
            if line:
                outputDisplay = eksekusi(line)
                # print(f"Debug:: {line}")
                output_text.insert(tk.END, outputDisplay+"\n")
        
    except Exception as e:
        output_text.insert(tk.END, str(e))

def clear(action):
    if action == "input":
        code_text.delete("1.0", tk.END)
    elif action == "output":
        output_text.delete("1.0", tk.END)
        # print(f"Debug test clouput 1:: {output_history}")

def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, "r") as file:
            code_content = file.read()
            code_text.delete("1.0", tk.END)
            code_text.insert(tk.END, code_content)


window = tk.Tk()
window.geometry("1000x800")
window.title("EETHON - Python Compiler 1.0 By Eeja")
window.resizable(False, False)

custom_font = ("Arial", 12, "bold")
button_bg_width = 12
button_bg_height = 1

# Create a frame for buttons
button_frame = tk.Frame(window)
button_frame.pack(pady=1, anchor=tk.W)

# Create buttons with the same size
open_file_button = tk.Button(
    button_frame,
    text="Buka File",
    command=open_file,
    font=custom_font,
    width=button_bg_width,
    height=button_bg_height,
)
tombol_clear1 = tk.Button(
    button_frame,
    text="Clear Input",
    command=lambda: clear("input"),
    font=custom_font,
    width=button_bg_width,
    height=button_bg_height,
)
tombol_clear2 = tk.Button(
    button_frame,
    text="Clear Output",
    command=lambda: clear("output"),
    font=custom_font,
    width=button_bg_width,
    height=button_bg_height,
)
compile_button = tk.Button(
    button_frame,
    text="Eksekusi",
    command=compile_code,
    font=custom_font,
    width=button_bg_width,
    height=button_bg_height,
)

# Use pack to place buttons on the left
open_file_button.pack(side=tk.LEFT, padx=8, pady=5)
tombol_clear1.pack(side=tk.LEFT, padx=5, pady=5)
tombol_clear2.pack(side=tk.LEFT, padx=5, pady=5)
compile_button.pack(side=tk.LEFT, padx=5, pady=5)

# Text area for code
code_text = scrolledtext.ScrolledText(window, width=120, height=22)
code_text.pack(padx=5, pady=5)

# Label for "Hasil:"
output_label = tk.Label(window, text="Hasil:", font=custom_font)
output_label.pack(anchor=tk.W, padx=5)

# Text area for output
output_text = scrolledtext.ScrolledText(window, width=120, height=20)
output_text.pack(padx=5, pady=5)

window.mainloop()
