import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import re
qr_window = None
qr_label = None
def generate_qr():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    if not re.fullmatch(r"[A-Za-z ]+", name):
        messagebox.showerror("Invalid Name", "Name should contain only letters")
        return
    if not re.fullmatch(r"\d{10}", phone):
        messagebox.showerror("Invalid Phone", "Phone number must be 10 digits")
        return
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showerror("Invalid Email", "Enter a valid email address")
        return
    data = f"""
Name: {name}
Phone: {phone}
Email: {email}
"""

    qr = qrcode.make(data)
    qr.save("my_qr_code.png")

    show_qr_window("my_qr_code.png")
def show_qr_window(image_path):
    global qr_window, qr_label

    if qr_window is None or not qr_window.winfo_exists():
        qr_window = tk.Toplevel(root)
        qr_window.title("Generated QR Code")
        qr_window.geometry("300x340")
        qr_window.configure(bg="white")
        qr_window.resizable(False, False)

        qr_label = tk.Label(qr_window, bg="white")
        qr_label.pack(pady=20)

        tk.Label(
            qr_window,
            text="Scan this QR Code",
            font=("Segoe UI", 11),
            bg="white"
        ).pack(pady=5)

    img = Image.open(image_path).resize((220, 220))
    img_tk = ImageTk.PhotoImage(img)

    qr_label.config(image=img_tk)
    qr_label.image = img_tk   # IMPORTANT
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("420x480")
root.configure(bg="#E8ECF1")
root.resizable(False, False)
canvas = tk.Canvas(root, bg="#E8ECF1", highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
scroll_frame = tk.Frame(canvas, bg="#E8ECF1")
canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

def update_scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scroll_frame.bind("<Configure>", update_scroll)
card = tk.Frame(scroll_frame, bg="white")
card.pack(pady=20, padx=20, fill="both")
tk.Label(
    card,
    text="QR Code Generator",
    font=("Segoe UI", 16, "bold"),
    bg="white",
    fg="#333"
).pack(pady=15)
def create_field(label_text):
    tk.Label(
        card,
        text=label_text,
        bg="white",
        fg="#555",
        font=("Segoe UI", 10)
    ).pack(anchor="w", padx=30)

    entry = tk.Entry(
        card,
        font=("Segoe UI", 11),
        bg="#F2F4F7",
        relief="flat"
    )
    entry.pack(fill="x", padx=30, pady=6, ipady=6)
    return entry

name_entry = create_field("Name")
phone_entry = create_field("Phone Number")
email_entry = create_field("Email")
tk.Button(
    card,
    text="Generate QR",
    command=generate_qr,
    font=("Segoe UI", 11, "bold"),
    bg="#4CAF50",
    fg="white",
    relief="flat",
    cursor="hand2",
    padx=20,
    pady=8
).pack(pady=25)

# ----------------- Run App -----------------
root.mainloop()

