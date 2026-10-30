#!/usr/bin/env python3
import time
import os
from dogtail.apps import startApplication
from dogtail.tree import root

# 1. Jalankan LibreOffice Writer
print("Memulai LibreOffice Writer...")
startApplication('libreoffice --writer')
time.sleep(3) # Tunggu hingga aplikasi terbuka sepenuhnya

# 2. Cari aplikasi LibreOffice di Accessibility Tree
# LibreOffice biasanya terdaftar sebagai 'soffice' atau 'LibreOffice X.X'
writer_app = root.application('soffice')

# 3. Simulasikan mengetik teks di area kerja utama (Document/Text Area)
print("Mengetik teks dokumen...")
# Mencari area teks berdasarkan rolenya (biasanya 'document text' atau memiliki nama default)
text_area = writer_app.child(roleName='document text')
text_area.typeText("Halo, ini adalah pengujian otomatis menggunakan Dogtail dan Python!")

# 4. Mengklik Menu Bar (Contoh: Buka Dialog Find & Replace)
print("Membuka menu Edit -> Find...")
menu_edit = writer_app.child(text='Edit', roleName='menu')
menu_edit.click()

# Klik submenu Find
menu_find = writer_app.child(text='Find...', roleName='menu item')
menu_find.click()
time.sleep(1)

# 5. Menutup jendela Find yang muncul (jika terbuka)
try:
    find_dialog = writer_app.child(roleName='dialog')
    close_button = find_dialog.child(text='Close', roleName='push button')
    close_button.click()
    print("Jendela Find berhasil ditutup.")
except Exception:
    print("Jendela Find tidak ditemukan atau gagal ditutup.")

# 6. Menutup LibreOffice Writer (File -> Exit LibreOffice)
print("Menutup aplikasi...")
menu_file = writer_app.child(text='File', roleName='menu')
menu_file.click()

menu_exit = writer_app.child(text='Exit LibreOffice', roleName='menu item')
menu_exit.click()
time.sleep(1)

# 7. Menangani dialog "Save Changes" (Pilih 'Don't Save')
try:
    dialog_save = writer_app.child(roleName='dialog')
    # Cari tombol 'Don't Save' atau 'Close without saving'
    dont_save_btn = dialog_save.child(text="Don't Save", roleName='push button')
    dont_save_btn.click()
    print("Pengujian Selesai: Aplikasi ditutup tanpa menyimpan.")
except Exception:
    print("Aplikasi langsung tertutup tanpa dialog konfirmasi.")

