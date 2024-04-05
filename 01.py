import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import datetime
import getpass

class BackupRestoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Baldur's Gate 3 Honour Mode Save Saver")
        self.root.geometry("600x350")

        self.username = getpass.getuser()
        self.source_dir_base = f"C:/Users/{self.username}/AppData/Local/Larian Studios/Baldur's Gate 3/PlayerProfiles/Public/Savegames/Story"
        self.backup_dir = None
        self.selected_uuid_dir = None

        self.uuid_combobox = ttk.Combobox(self.root, state="readonly", width=50)
        self.uuid_combobox.pack(pady=10)
        self.uuid_combobox.bind("<<ComboboxSelected>>", self.select_uuid_directory)

        self.backup_button = tk.Button(self.root, text="Select Backup Directory", command=self.select_backup_directory)
        self.backup_button.pack(pady=10)

        self.backup_label = tk.Label(self.root, text="")
        self.backup_label.pack(pady=5)

        self.restore_button = tk.Button(self.root, text="Restore Save", command=self.restore_save)
        self.restore_button.pack(pady=10)

        self.restore_combobox = ttk.Combobox(self.root, state="readonly", width=50)
        self.restore_combobox.pack(pady=5)
        self.restore_combobox.bind("<<ComboboxSelected>>", self.update_restore_combobox)

        self.update_uuid_combobox()

    def update_uuid_combobox(self):
        uuid_dirs = [d for d in os.listdir(self.source_dir_base) if os.path.isdir(os.path.join(self.source_dir_base, d))]
        self.uuid_combobox['values'] = uuid_dirs
        if uuid_dirs:
            self.uuid_combobox.current(0)
            self.select_uuid_directory()

    def select_uuid_directory(self, event=None):
        self.selected_uuid_dir = self.uuid_combobox.get()
        self.update_restore_combobox()

    def select_backup_directory(self):
        self.backup_dir = filedialog.askdirectory(title="Select Backup Directory")
        if self.backup_dir:
            self.backup_label.config(text=f"Backup Directory: {self.backup_dir}")
            self.backup_button.config(text="Backup Save", command=self.backup_save)
            self.update_restore_combobox()

    def backup_save(self):
        if self.selected_uuid_dir and self.backup_dir:
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            dest_dir = os.path.join(self.backup_dir, timestamp)
            shutil.copytree(os.path.join(self.source_dir_base, self.selected_uuid_dir), dest_dir)
            messagebox.showinfo("Success", "Backup completed successfully.")
            self.update_restore_combobox()
        else:
            messagebox.showerror("Error", "UUID directory not selected or backup directory not selected.")

    def update_restore_combobox(self):
        if self.backup_dir:
            saves = [d for d in os.listdir(self.backup_dir) if os.path.isdir(os.path.join(self.backup_dir, d))]
            self.restore_combobox['values'] = saves
            if saves:
                self.restore_combobox.current(0)

    def restore_save(self):
        selected_save = self.restore_combobox.get()
        if selected_save and self.selected_uuid_dir:
            source_dir = os.path.join(self.backup_dir, selected_save)
            dest_dir = os.path.join(self.source_dir_base, self.selected_uuid_dir)
            for file in os.listdir(source_dir):
                if file.endswith(".WebP") or file.endswith(".lsv"):
                    shutil.copy2(os.path.join(source_dir, file), dest_dir)
            messagebox.showinfo("Success", "Restore completed successfully.")
        else:
            messagebox.showerror("Error", "No save selected for restore or UUID directory not selected.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BackupRestoreApp(root)
    root.mainloop()
