#!/usr/bin/env python3
"""
Test sederhana LibreOffice Writer menggunakan Dogtail
Untuk QA BlankOn Linux / GNOME
"""

from dogtail.tree import root
from dogtail.utils import run
from dogtail.predicate import *
from dogtail.config import config
import dogtail.rawinput as rawinput
import time
import os
import sys

# Konfigurasi dogtail
config.searchCutoffCount = 40          # lebih sabar mencari elemen
config.actionDelay = 0.8
config.defaultDelay = 0.5
config.childrenLimit = 500

# Path file yang akan disimpan
SAVE_PATH = os.path.expanduser("~/Documents/test_dogtail_blankon.odt")

def log(msg):
    print(f"[QA] {msg}")

def wait(seconds=1.5):
    time.sleep(seconds)

def main():
    log("=== Mulai test LibreOffice Writer ===")

    # 1. Hapus file lama kalau ada
    if os.path.exists(SAVE_PATH):
        os.remove(SAVE_PATH)
        log(f"File lama dihapus: {SAVE_PATH}")

    # 2. Jalankan LibreOffice Writer
    log("Menjalankan LibreOffice Writer...")
    run("libreoffice --writer", appName="soffice")
    wait(4)  # beri waktu loading

    # 3. Cari aplikasi
    try:
        app = root.application("soffice")
        log("Aplikasi 'soffice' ditemukan")
    except Exception:
        try:
            app = root.application("libreoffice")
            log("Aplikasi 'libreoffice' ditemukan")
        except Exception as e:
            log(f"GAGAL menemukan aplikasi LibreOffice: {e}")
            sys.exit(1)

    # 4. Cari jendela Writer
    try:
        # Coba beberapa kemungkinan nama window
        win = None
        for name in ["Untitled 1", "Untitled", "Dokumen tanpa judul 1", "LibreOffice Writer"]:
            try:
                win = app.window(name)
                log(f"Jendela ditemukan: {name}")
                break
            except:
                continue

        if win is None:
            # Fallback: ambil window pertama
            win = app.children[0]
            log(f"Menggunakan window pertama: {win.name}")
    except Exception as e:
        log(f"GAGAL menemukan jendela: {e}")
        sys.exit(1)

    wait(1)

    # 5. Fokus ke area dokumen dan ketik teks
    log("Mengetik teks uji...")
    try:
        # Coba fokus ke document frame
        doc = win.child(roleName="document")
        doc.grabFocus()
    except:
        # Fallback: klik tengah jendela
        win.click()
    
    wait(0.8)

    # Ketik teks
    teks_uji = "Ini adalah tes otomatis Dogtail untuk BlankOn Linux.\nQA LibreOffice Writer berhasil."
    rawinput.typeText(teks_uji)
    wait(1)
    log("Teks berhasil diketik")

    # 6. Simpan dokumen (Ctrl + S)
    log("Menyimpan dokumen...")
    rawinput.pressKey("ctrl")
    rawinput.pressKey("s")
    rawinput.releaseKey("s")
    rawinput.releaseKey("ctrl")
    wait(2)

    # 7. Isi dialog Save
    try:
        # Cari dialog Save
        save_dlg = root.dialog("Save") or root.dialog("Simpan") or app.dialog("Save")
        
        # Cari entry nama file
        try:
            entry = save_dlg.child(roleName="text")
            entry.click()
            wait(0.3)
            # Hapus isi lama
            rawinput.pressKey("ctrl")
            rawinput.pressKey("a")
            rawinput.releaseKey("a")
            rawinput.releaseKey("ctrl")
            wait(0.2)
            rawinput.typeText(SAVE_PATH)
        except:
            # Alternatif: langsung ketik path
            rawinput.typeText(SAVE_PATH)

        wait(0.5)

        # Tekan tombol Save / Simpan
        try:
            btn = save_dlg.button("Save") or save_dlg.button("Simpan")
            btn.click()
        except:
            rawinput.pressKey("Return")  # fallback

        wait(2)
        log(f"Dokumen disimpan ke: {SAVE_PATH}")
    except Exception as e:
        log(f"Peringatan saat menyimpan (mungkin sudah tersimpan): {e}")

    # 8. Tutup LibreOffice (Ctrl + Q)
    log("Menutup LibreOffice...")
    rawinput.pressKey("ctrl")
    rawinput.pressKey("q")
    rawinput.releaseKey("q")
    rawinput.releaseKey("ctrl")
    wait(1.5)

    # 9. Verifikasi hasil
    if os.path.exists(SAVE_PATH):
        size = os.path.getsize(SAVE_PATH)
        log(f"SUKSES! File berhasil dibuat ({size} bytes)")
        log(f"Lokasi: {SAVE_PATH}")
        print("\n=== HASIL TEST: PASS ===")
        return 0
    else:
        log("GAGAL: File tidak ditemukan setelah save")
        print("\n=== HASIL TEST: FAIL ===")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nDibatalkan oleh user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError tidak terduga: {e}")
        sys.exit(1)
