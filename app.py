import tkinter as tk
from tkinter import ttk, messagebox
from db_config import get_connection
import os
from PIL import Image, ImageDraw, ImageFont, ImageTk

# ==========================================
# FUNGSI MEMBUAT BACKGROUND OTOMATIS
# ==========================================
def create_background():
    bg_path = "bg.png"
    if not os.path.exists(bg_path):
        width, height = 1200, 700
        img = Image.new('RGB', (width, height), color='#0f172a')
        draw = ImageDraw.Draw(img)
        
        # Membuat gradient efek elektronik
        for y in range(height):
            r = int(15 + (y * 0.02))
            g = int(23 + (y * 0.04))
            b = int(42 + (y * 0.06))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
            
        # Membuat efek grid layar HP
        for x in range(0, width, 40):
            draw.line([(x, 0), (x, height)], fill=(255, 255, 255, 10), width=1)
        for y in range(0, height, 40):
            draw.line([(0, y), (width, y)], fill=(255, 255, 255, 10), width=1)
            
        # Membuat lingkaran dekoratif (simbol node/tech)
        for _ in range(15):
            x, y = 100, 100
            draw.ellipse([x-50, y-50, x+50, y+50], outline="#3b82f6", width=2)
            
        img.save(bg_path)
    return bg_path

# ==========================================
# SETTING TAMPILAN GLOBAL (THEME)
# ==========================================
ROOT_BG = "#0f172a"
FRAME_BG = "#1e293b"
TEXT_COLOR = "#f8fafc"
ACCENT_COLOR = "#3b82f6"
BTN_BG = "#2563eb"
BTN_HOVER = "#1d4ed8"
TREE_BG = "#334155"

# ==========================================
# INISIALISASI WINDOW UTAMA
# ==========================================
root = tk.Tk()
root.title("SISC - Sistem Informasi Service Center Elektronik & Smartphone")
root.geometry("1100x650")
root.configure(bg=ROOT_BG)
root.resizable(False, False)

# Pasang Background
bg_path = create_background()
bg_image = Image.open(bg_path)
bg_image = bg_image.resize((1100, 650), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Judul Aplikasi
judul_frame = tk.Frame(root, bg="#0f172a", bd=0)
judul_frame.place(relx=0.5, y=20, anchor="n")

judul = tk.Label(judul_frame, text="SISC - SERVICE CENTER", 
                 font=("Helvetica", 24, "bold"), bg="#0f172a", fg=ACCENT_COLOR)
judul.pack()
sub_judul = tk.Label(judul_frame, text="Sistem Informasi Elektronik & Smartphone", 
                     font=("Helvetica", 12), bg="#0f172a", fg=TEXT_COLOR)
sub_judul.pack()

# Container untuk konten dinamis
container = tk.Frame(root, bg=ROOT_BG)
container.place(relx=0.5, y=110, anchor="n", width=1050, height=520)

def clear_container():
    for widget in container.winfo_children():
        widget.destroy()

# ==========================================
# STYLE TABEL (TREEVIEW)
# ==========================================
style = ttk.Style()
style.theme_use("clam")
style.configure("Custom.Treeview", 
                background=TREE_BG, 
                foreground=TEXT_COLOR, 
                fieldbackground=TREE_BG, 
                rowheight=25, 
                font=("Helvetica", 10))
style.configure("Custom.Treeview.Heading", 
                background=ACCENT_COLOR, 
                foreground="white", 
                font=("Helvetica", 11, "bold"))
style.map("Custom.Treeview", background=[("selected", "#1e40af")])

# ==========================================
# HELPER: TOMBOL STYLISH
# ==========================================
def create_button(parent, text, command, color=BTN_BG):
    btn = tk.Button(parent, text=text, command=command, 
                    bg=color, fg="white", font=("Helvetica", 10, "bold"),
                    relief="flat", cursor="hand2", padx=15, pady=5,
                    activebackground=BTN_HOVER, activeforeground="white")
    return btn

# ==========================================
# FORM 1: DATA PELANGGAN
# ==========================================
def form_pelanggan():
    clear_container()
    frame = tk.Frame(container, bg=FRAME_BG, padx=20, pady=15)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="DATA PELANGGAN", font=("Helvetica", 14, "bold"), 
             bg=FRAME_BG, fg=ACCENT_COLOR).grid(row=0, column=0, columnspan=4, pady=(0,10), sticky="w")

    # Entry
    lbl = ["ID Pelanggan", "Nama Pelanggan", "No HP", "Alamat"]
    entries = []
    for i, l in enumerate(lbl):
        tk.Label(frame, text=l, bg=FRAME_BG, fg=TEXT_COLOR, font=("Helvetica", 10)).grid(row=i+1, column=0, sticky="w", pady=5)
        e = tk.Entry(frame, width=40, font=("Helvetica", 10))
        e.grid(row=i+1, column=1, columnspan=3, pady=5, padx=10)
        entries.append(e)

    # Tabel
    kolom = ("id_pelanggan", "nama_pelanggan", "no_hp", "alamat")
    tree = ttk.Treeview(frame, columns=kolom, show="headings", style="Custom.Treeview")
    for c in kolom:
        tree.heading(c, text=c.title())
        tree.column(c, width=220)
    tree.grid(row=7, column=0, columnspan=4, pady=15, sticky="nsew")

    def tampil():
        for item in tree.get_children(): tree.delete(item)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbpelanggan")
        for row in cursor.fetchall(): tree.insert("", "end", values=row)
        conn.close()

    def simpan():
        if not entries[0].get(): return messagebox.showwarning("Peringatan", "ID harus diisi!")
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO tbpelanggan VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, tuple(e.get() for e in entries))
        conn.commit(); conn.close()
        messagebox.showinfo("Sukses", "Data Berhasil Disimpan!")
        for e in entries: e.delete(0, "end")
        tampil()

    def hapus():
        selected = tree.focus()
        if not selected: return
        val = tree.item(selected)["values"][0]
        if messagebox.askyesno("Hapus", "Yakin hapus data ini?"):
            conn = get_connection(); cursor = conn.cursor()
            cursor.execute("DELETE FROM tbpelanggan WHERE id_pelanggan=%s", (val,))
            conn.commit(); conn.close(); tampil()

    # Tombol
    frame_btn = tk.Frame(frame, bg=FRAME_BG)
    frame_btn.grid(row=6, column=0, columnspan=4, pady=5)
    create_button(frame_btn, "Simpan", simpan).pack(side="left", padx=5)
    create_button(frame_btn, "Tampil Data", tampil, color="#16a34a").pack(side="left", padx=5)
    create_button(frame_btn, "Hapus Data", hapus, color="#dc2626").pack(side="left", padx=5)

    tampil() # Auto load data saat buka form

# ==========================================
# FORM 2: DATA TEKNISI
# ==========================================
def form_teknisi():
    clear_container()
    frame = tk.Frame(container, bg=FRAME_BG, padx=20, pady=15)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="DATA TEKNISI", font=("Helvetica", 14, "bold"), bg=FRAME_BG, fg=ACCENT_COLOR).grid(row=0, column=0, columnspan=4, pady=(0,10), sticky="w")

    lbl = ["ID Teknisi", "Nama Teknisi", "Spesialisasi", "No HP"]
    entries = []
    for i, l in enumerate(lbl):
        tk.Label(frame, text=l, bg=FRAME_BG, fg=TEXT_COLOR, font=("Helvetica", 10)).grid(row=i+1, column=0, sticky="w", pady=5)
        e = tk.Entry(frame, width=40, font=("Helvetica", 10))
        e.grid(row=i+1, column=1, columnspan=3, pady=5, padx=10)
        entries.append(e)

    kolom = ("id_teknisi", "nama_teknisi", "spesialisasi", "no_hp")
    tree = ttk.Treeview(frame, columns=kolom, show="headings", style="Custom.Treeview")
    for c in kolom:
        tree.heading(c, text=c.title())
        tree.column(c, width=220)
    tree.grid(row=6, column=0, columnspan=4, pady=15, sticky="nsew")

    def tampil():
        for item in tree.get_children(): tree.delete(item)
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbteknisi")
        for row in cursor.fetchall(): tree.insert("", "end", values=row)
        conn.close()

    def simpan():
        if not entries[0].get(): return messagebox.showwarning("Peringatan", "ID harus diisi!")
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("INSERT INTO tbteknisi VALUES (%s,%s,%s,%s)", tuple(e.get() for e in entries))
        conn.commit(); conn.close()
        messagebox.showinfo("Sukses", "Data Berhasil Disimpan!")
        for e in entries: e.delete(0, "end")
        tampil()

    frame_btn = tk.Frame(frame, bg=FRAME_BG)
    frame_btn.grid(row=5, column=0, columnspan=4, pady=5)
    create_button(frame_btn, "Simpan", simpan).pack(side="left", padx=5)
    create_button(frame_btn, "Tampil Data", tampil, color="#16a34a").pack(side="left", padx=5)
    tampil()

# ==========================================
# FORM 3: DATA PERANGKAT
# ==========================================
def form_perangkat():
    clear_container()
    frame = tk.Frame(container, bg=FRAME_BG, padx=20, pady=15)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="DATA PERANGKAT", font=("Helvetica", 14, "bold"), bg=FRAME_BG, fg=ACCENT_COLOR).grid(row=0, column=0, columnspan=4, pady=(0,10), sticky="w")

    lbl = ["ID Perangkat", "Jenis (HP/Laptop/TV)", "Merk", "Model/Tipe"]
    entries = []
    for i, l in enumerate(lbl):
        tk.Label(frame, text=l, bg=FRAME_BG, fg=TEXT_COLOR, font=("Helvetica", 10)).grid(row=i+1, column=0, sticky="w", pady=5)
        e = tk.Entry(frame, width=40, font=("Helvetica", 10))
        e.grid(row=i+1, column=1, columnspan=3, pady=5, padx=10)
        entries.append(e)
    
    tk.Label(frame, text="Garansi (Y/N)", bg=FRAME_BG, fg=TEXT_COLOR, font=("Helvetica", 10)).grid(row=5, column=0, sticky="w", pady=5)
    combo_garansi = ttk.Combobox(frame, values=["Y", "N"], width=37, state="readonly")
    combo_garansi.grid(row=5, column=1, columnspan=3, pady=5, padx=10)

    kolom = ("id_perangkat", "jenis_perangkat", "merk", "model", "garansi")
    tree = ttk.Treeview(frame, columns=kolom, show="headings", style="Custom.Treeview")
    for c in kolom:
        tree.heading(c, text=c.title())
        tree.column(c, width=180)
    tree.grid(row=7, column=0, columnspan=4, pady=15, sticky="nsew")

    def tampil():
        for item in tree.get_children(): tree.delete(item)
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbperangkat")
        for row in cursor.fetchall(): tree.insert("", "end", values=row)
        conn.close()

    def simpan():
        if not entries[0].get() or not combo_garansi.get(): return messagebox.showwarning("Peringatan", "Lengkapi data!")
        data = tuple(e.get() for e in entries) + (combo_garansi.get(),)
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("INSERT INTO tbperangkat VALUES (%s,%s,%s,%s,%s)", data)
        conn.commit(); conn.close()
        messagebox.showinfo("Sukses", "Data Berhasil Disimpan!")
        for e in entries: e.delete(0, "end")
        combo_garansi.set("")
        tampil()

    frame_btn = tk.Frame(frame, bg=FRAME_BG)
    frame_btn.grid(row=6, column=0, columnspan=4, pady=5)
    create_button(frame_btn, "Simpan", simpan).pack(side="left", padx=5)
    create_button(frame_btn, "Tampil Data", tampil, color="#16a34a").pack(side="left", padx=5)
    tampil()

# ==========================================
# FORM 4: TRANSAKSI SERVIS
# ==========================================
def form_servis():
    clear_container()
    frame = tk.Frame(container, bg=FRAME_BG, padx=20, pady=15)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="TRANSAKSI SERVIS", font=("Helvetica", 14, "bold"), bg=FRAME_BG, fg=ACCENT_COLOR).grid(row=0, column=0, columnspan=4, pady=(0,10), sticky="w")

    # Load data combo dari database
    conn = get_connection(); cursor = conn.cursor()
    cursor.execute("SELECT id_pelanggan FROM tbpelanggan"); id_plg = [r[0] for r in cursor.fetchall()]
    cursor.execute("SELECT id_perangkat FROM tbperangkat"); id_prd = [r[0] for r in cursor.fetchall()]
    cursor.execute("SELECT id_teknisi FROM tbteknisi"); id_tkn = [r[0] for r in cursor.fetchall()]
    conn.close()

    lbl_text = ["ID Pelanggan", "ID Perangkat", "ID Teknisi", "Tanggal (YYYY-MM-DD)"]
    widgets = []
    for i, l in enumerate(lbl_text):
        tk.Label(frame, text=l, bg=FRAME_BG, fg=TEXT_COLOR, font=("Helvetica", 10)).grid(row=i+1, column=0, sticky="w", pady=5)
        if i < 3:
            cb = ttk.Combobox(frame, values=eval(f"id_{['plg','prd','tkn'][i]}"), width=37, state="readonly")
            cb.grid(row=i+1, column=1, columnspan=3, pady=5, padx=10)
            widgets.append(cb)
        else:
            e = tk.Entry(frame, width=40, font=("Helvetica", 10))
            e.grid(row=i+1, column=1, columnspan=3, pady=5, padx=10)
            widgets.append(e)

    tk.Label(frame, text="Keluhan", bg=FRAME_BG, fg=TEXT_COLOR, font=("Helvetica", 10)).grid(row=5, column=0, sticky="w", pady=5)
    txt_keluhan = tk.Text(frame, width=45, height=2, font=("Helvetica", 10))
    txt_keluhan.grid(row=5, column=1, columnspan=3, pady=5, padx=10)

    tk.Label(frame, text="Status", bg=FRAME_BG, fg=TEXT_COLOR, font=("Helvetica", 10)).grid(row=6, column=0, sticky="w", pady=5)
    combo_status = ttk.Combobox(frame, values=["Diterima","Diperiksa","Diperbaiki","Selesai","Diambil"], width=37, state="readonly")
    combo_status.grid(row=6, column=1, columnspan=3, pady=5, padx=10)
    combo_status.set("Diterima")

    tk.Label(frame, text="Biaya (Rp)", bg=FRAME_BG, fg=TEXT_COLOR, font=("Helvetica", 10)).grid(row=7, column=0, sticky="w", pady=5)
    entry_biaya = tk.Entry(frame, width=40, font=("Helvetica", 10))
    entry_biaya.grid(row=7, column=1, columnspan=3, pady=5, padx=10)

    kolom = ("ID Servis", "Pelanggan", "Perangkat", "Teknisi", "Tgl Masuk", "Keluhan", "Status", "Biaya")
    tree = ttk.Treeview(frame, columns=kolom, show="headings", style="Custom.Treeview")
    for c in kolom: 
        tree.heading(c, text=c)
        tree.column(c, width=120)
    tree.column("Keluhan", width=200)
    tree.grid(row=9, column=0, columnspan=4, pady=15, sticky="nsew")

    def tampil():
        for item in tree.get_children(): tree.delete(item)
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("""SELECT id_servis, id_pelanggan, id_perangkat, id_teknisi, 
                          tanggal_masuk, keluhan, status_servis, biaya FROM tbservis""")
        for row in cursor.fetchall(): tree.insert("", "end", values=row)
        conn.close()

    def simpan():
        if not widgets[0].get(): return messagebox.showwarning("Peringatan", "Pilih Pelanggan!")
        data = (widgets[0].get(), widgets[1].get(), widgets[2].get(), widgets[3].get(), 
                txt_keluhan.get("1.0", "end"), combo_status.get(), entry_biaya.get() or 0)
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("""INSERT INTO tbservis (id_pelanggan, id_perangkat, id_teknisi, 
                        tanggal_masuk, keluhan, status_servis, biaya) VALUES (%s,%s,%s,%s,%s,%s,%s)""", data)
        conn.commit(); conn.close()
        messagebox.showinfo("Sukses", "Data Servis Disimpan!")
        tampil()

    frame_btn = tk.Frame(frame, bg=FRAME_BG)
    frame_btn.grid(row=8, column=0, columnspan=4, pady=5)
    create_button(frame_btn, "Simpan Servis", simpan).pack(side="left", padx=5)
    create_button(frame_btn, "Tampil Data", tampil, color="#16a34a").pack(side="left", padx=5)
    tampil()

# ==========================================
# MENU NAVIGASI (MENGGANTIKAN MENU BAR AGAR LEBIH MODERN)
# ==========================================
menu_frame = tk.Frame(root, bg="#0f172a")
menu_frame.place(relx=0.5, y=75, anchor="n")

menus = [
    ("Data Pelanggan", form_pelanggan),
    ("Data Teknisi", form_teknisi),
    ("Data Perangkat", form_perangkat),
    ("Transaksi Servis", form_servis),
    ("Keluar", root.quit)
]

for text, cmd in menus:
    color = "#dc2626" if text == "Keluar" else BTN_BG
    create_button(menu_frame, text, cmd, color).pack(side="left", padx=5)

# Tampilkan form pertama saat mulai
form_pelanggan()

root.mainloop()