import tkinter as tk
from tkinter import ttk
import winreg
import pandas as pd
import matplotlib.pyplot as plt

def get_installed_apps():
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    apps = []

    for reg_path in reg_paths:
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
        except:
            continue

        for i in range(0, winreg.QueryInfoKey(reg_key)[0]):
            try:
                sub_key_name = winreg.EnumKey(reg_key, i)
                sub_key = winreg.OpenKey(reg_key, sub_key_name)

                # Get values safely
                name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                version = ""
                size_kb = 0

                try:
                    version = winreg.QueryValueEx(sub_key, "DisplayVersion")[0]
                except:
                    pass
                try:
                    size_kb = winreg.QueryValueEx(sub_key, "EstimatedSize")[0]
                except:
                    pass

                size_mb = round(size_kb / 1024, 2)

                apps.append({
                    "Name": name,
                    "Version": version,
                    "Size(MB)": size_mb
                })
            except:
                continue

    return pd.DataFrame(apps).sort_values(by="Size(MB)", ascending=False)

def show_apps():
    df = get_installed_apps()
    tree.delete(*tree.get_children())  # Clear previous
    for i, row in df.iterrows():
        tree.insert("", tk.END, values=(row["Name"], row["Version"], row["Size(MB)"]))

def plot_top_10():
    df = get_installed_apps().head(10)
    plt.figure(figsize=(10, 6))
    plt.barh(df["Name"], df["Size(MB)"], color='skyblue')
    plt.xlabel("Size (MB)")
    plt.title("Top 10 Largest Installed Apps")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

# GUI Setup
root = tk.Tk()
root.title("SpaceScanner")
root.geometry("800x500")
root.iconbitmap("SpaceScanner.ico")  # Set custom icon

# Table
tree = ttk.Treeview(root, columns=("Name", "Version", "Size(MB)"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Version", text="Version")
tree.heading("Size(MB)", text="Size (MB)")
tree.pack(fill=tk.BOTH, expand=True)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

load_btn = tk.Button(btn_frame, text="Load Apps", command=show_apps)
load_btn.pack(side=tk.LEFT, padx=10)

plot_btn = tk.Button(btn_frame, text="Plot Top 10", command=plot_top_10)
plot_btn.pack(side=tk.LEFT)

root.mainloop()

