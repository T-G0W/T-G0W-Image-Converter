# -- Changelog Version 1.0 by T-G0W


import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
from threading import Thread

class TGOWImageConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("T-G0W Image Converter")
        self.root.geometry("950x550")
        self.root.minsize(900, 500)
        
        self.primary_color = "#1976D2"
        self.secondary_color = "#64B5F6"
        self.accent_color = "#FF5722"
        self.bg_color = "#E3F2FD"
        self.card_color = "#FFFFFF"
        self.text_color = "#212121"
        self.listbox_bg = "#FFFFFF"
        self.listbox_fg = "#000000"
        
        self.input_files = []
        self.output_format = tk.StringVar(value="png")
        self.output_folder = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Horizontal.TProgressbar",
            background=self.primary_color,
            troughcolor="#E0E0E0",
            bordercolor="#E0E0E0",
            lightcolor=self.primary_color,
            darkcolor=self.primary_color
        )
        self.style.configure("TButton",
            background=self.primary_color,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            padding=(10, 5),
            relief="flat"
        )
        self.style.map("TButton",
            background=[("active", self.secondary_color), ("disabled", "#BDBDBD")],
            foreground=[("disabled", "#757575")]
        )
        self.style.configure("TLabel",
            background=self.bg_color,
            foreground=self.text_color,
            font=("Segoe UI", 10)
        )
        self.style.configure("Card.TFrame",
            background=self.card_color,
            relief="raised",
            borderwidth=1
        )

    def create_widgets(self):
        self.root.configure(bg=self.bg_color)
        
        header_frame = ttk.Frame(self.root, style="Card.TFrame", padding=10)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(
            header_frame,
            text="T-G0W IMAGE CONVERTER",
            font=("Segoe UI", 16, "bold"),
            foreground=self.primary_color
        ).pack(side=tk.LEFT)
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        input_card = ttk.Frame(left_frame, style="Card.TFrame", padding=15)
        input_card.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        ttk.Label(
            input_card,
            text="Dateien auswählen",
            font=("Segoe UI", 11, "bold"),
            foreground=self.primary_color
        ).pack(anchor=tk.W, pady=(0, 10))
        
        self.file_listbox = tk.Listbox(
            input_card,
            height=10,
            selectmode=tk.EXTENDED,
            bg=self.listbox_bg,
            fg=self.listbox_fg,
            selectbackground=self.primary_color,
            selectforeground="white",
            borderwidth=1,
            relief="solid",
            font=("Segoe UI", 9)
        )
        self.file_listbox.pack(fill=tk.BOTH, expand=True)
        
        btn_frame = ttk.Frame(input_card)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.add_btn = ttk.Button(
            btn_frame,
            text="📁 Dateien hinzufügen",
            command=self.add_files,
            style="TButton"
        )
        self.add_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.add_folder_btn = ttk.Button(
            btn_frame,
            text="📂 Ordner hinzufügen",
            command=self.add_folder,
            style="TButton"
        )
        self.add_folder_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.remove_btn = ttk.Button(
            btn_frame,
            text="🗑️ Auswahl entfernen",
            command=self.remove_files,
            style="TButton"
        )
        self.remove_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        right_frame = ttk.Frame(main_frame, width=250)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        settings_card = ttk.Frame(right_frame, style="Card.TFrame", padding=15)
        settings_card.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            settings_card,
            text="Konvertierungseinstellungen",
            font=("Segoe UI", 11, "bold"),
            foreground=self.primary_color
        ).pack(anchor=tk.W, pady=(0, 15))
        
        format_frame = ttk.Frame(settings_card)
        format_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(format_frame, text="Zielformat:").pack(side=tk.LEFT)
        
        formats = ["png", "jpg", "jpeg", "webp", "gif", "bmp", "tiff", "tif", "heic", "heif", "avif"]
        self.format_combo = ttk.Combobox(
            format_frame,
            textvariable=self.output_format,
            values=formats,
            state="readonly",
            width=12
        )
        self.format_combo.pack(side=tk.RIGHT)
        
        self.quality_frame = ttk.Frame(settings_card)
        self.quality_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(self.quality_frame, text="Qualität:").pack(side=tk.LEFT)
        
        self.quality_slider = ttk.Scale(
            self.quality_frame,
            from_=1,
            to=100,
            value=90,
            orient=tk.HORIZONTAL
        )
        self.quality_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        self.quality_value = ttk.Label(self.quality_frame, text="90%")
        self.quality_value.pack(side=tk.RIGHT, padx=(0, 5))
        
        folder_frame = ttk.Frame(settings_card)
        folder_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(folder_frame, text="Zielordner:").pack(side=tk.LEFT)
        
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.output_folder)
        self.folder_entry.pack(side=tk.LEFT, padx=(10, 5), fill=tk.X, expand=True)
        
        self.browse_btn = ttk.Button(
            folder_frame,
            text="📂",
            command=self.browse_folder,
            style="TButton",
            width=3
        )
        self.browse_btn.pack(side=tk.LEFT)
        
        self.progress = ttk.Progressbar(
            right_frame,
            style="Horizontal.TProgressbar",
            orient=tk.HORIZONTAL,
            mode='determinate'
        )
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        self.convert_btn = ttk.Button(
            right_frame,
            text="🚀 Konvertieren starten",
            command=self.start_conversion,
            style="TButton"
        )
        self.convert_btn.pack(fill=tk.X, ipady=8)
        
        footer_frame = ttk.Frame(self.root, style="Card.TFrame", padding=8)
        footer_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.status = ttk.Label(
            footer_frame,
            text="Bereit zur Konvertierung",
            font=("Segoe UI", 9)
        )
        self.status.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(
            footer_frame,
            text="© 2025 T-G0W Converter",
            font=("Segoe UI", 9),
            foreground="#757575"
        ).pack(side=tk.RIGHT, padx=5)
        
        self.format_combo.bind("<<ComboboxSelected>>", self.update_quality_visibility)
        self.quality_slider.configure(command=self.update_quality_value)
        
        self.update_quality_visibility()
        
    def update_quality_visibility(self, event=None):
        format = self.output_format.get().lower()
        if format in ['jpg', 'jpeg', 'webp', 'heic', 'heif']:
            self.quality_frame.pack(fill=tk.X, pady=(0, 15))
        else:
            self.quality_frame.pack_forget()
        
    def update_quality_value(self, value):
        self.quality_value.config(text=f"{int(float(value))}%")
        
    def add_files(self):
        filetypes = [
            ("Bilder", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.tif *.webp *.heic *.heif *.avif *.svg *.dng *.cr2 *.cr3 *.nef"),
            ("Alle Dateien", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Bilder auswählen",
            filetypes=filetypes
        )
        
        if files:
            self.input_files.extend(files)
            self.update_file_list()
            self.status.config(text=f"{len(self.input_files)} Dateien ausgewählt")
    
    def add_folder(self):
        folder = filedialog.askdirectory(title="Ordner mit Bildern auswählen")
        if folder:
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', 
                              '.webp', '.heic', '.heif', '.avif', '.svg', '.dng', '.cr2', '.cr3', '.nef']
            folder_files = []
            for root, _, files in os.walk(folder):
                for file in files:
                    if os.path.splitext(file)[1].lower() in image_extensions:
                        folder_files.append(os.path.join(root, file))
            
            if folder_files:
                self.input_files.extend(folder_files)
                self.update_file_list()
                self.status.config(text=f"{len(self.input_files)} Dateien aus {os.path.basename(folder)} hinzugefügt")
            else:
                messagebox.showwarning("Warnung", "Der ausgewählte Ordner enthält keine unterstützten Bilddateien!")
    
    def remove_files(self):
        selected = self.file_listbox.curselection()
        if selected:
            for i in reversed(selected):
                del self.input_files[i]
            self.update_file_list()
            self.status.config(text=f"{len(self.input_files)} Dateien ausgewählt")
    
    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for file in self.input_files:
            self.file_listbox.insert(tk.END, os.path.basename(file))
    
    def browse_folder(self):
        folder = filedialog.askdirectory(
            title="Ausgabeordner auswählen",
            initialdir=self.output_folder.get()
        )
        if folder:
            self.output_folder.set(folder)
    
    def start_conversion(self):
        if not self.input_files:
            messagebox.showwarning("Warnung", "Bitte fügen Sie zuerst Bilder hinzu!")
            return
            
        if not os.path.isdir(self.output_folder.get()):
            messagebox.showerror("Fehler", "Der Ausgabeordner existiert nicht!")
            return
            
        self.convert_btn.config(state=tk.DISABLED, text="Konvertierung läuft...")
        Thread(target=self.convert_images, daemon=True).start()
    
    def convert_images(self):
        total_files = len(self.input_files)
        self.progress['maximum'] = total_files
        self.progress['value'] = 0
        
        for i, input_path in enumerate(self.input_files, 1):
            try:
                filename = os.path.basename(input_path)
                self.status.config(text=f"Konvertiere {filename}...")
                
                name, _ = os.path.splitext(filename)
                output_path = os.path.join(
                    self.output_folder.get(),
                    f"{name}.{self.output_format.get()}"
                )
                
                with Image.open(input_path) as img:
                    format = self.output_format.get().lower()
                    quality = int(self.quality_slider.get())
                    
                    if format in ['jpg', 'jpeg']:
                        img.save(output_path, format='JPEG', quality=quality)
                    elif format == 'png':
                        img.save(output_path, format='PNG', compress_level=9)
                    elif format == 'webp':
                        img.save(output_path, format='WEBP', quality=quality)
                    elif format in ['heic', 'heif']:
                        img.save(output_path, format='HEIF', quality=quality)
                    else:
                        img.save(output_path, format=format.upper())
                
                self.progress['value'] = i
                self.root.update_idletasks()
                
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Konvertieren von {input_path}:\n{str(e)}")
                continue
        
        self.status.config(text=f"Fertig! {self.progress['value']}/{total_files} Bildern konvertiert.")
        self.convert_btn.config(state=tk.NORMAL, text="✅ Konvertierung abgeschlossen")
        self.root.after(2000, lambda: self.convert_btn.config(text="🚀 Konvertieren starten"))
        messagebox.showinfo("Fertig", f"Konvertierung abgeschlossen!\n{self.progress['value']} von {total_files} Bildern wurden konvertiert.")

if __name__ == "__main__":
    root = tk.Tk()
    if os.name == "nt":
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    app = TGOWImageConverter(root)
    root.mainloop()
