#!/usr/bin/env python3
"""
Skenario QA: Buat 3 paragraf anekdot di LibreOffice Writer
lalu export ke PDF menggunakan Dogtail
"""

from dogtail.tree import root
from dogtail.utils import run
from dogtail.config import config
import dogtail.rawinput as rawinput
import time
import os
import sys

# ==================== KONFIGURASI ====================
config.searchCutoffCount = 50
config.actionDelay = 0.7
config.defaultDelay = 0.4

# Lokasi file hasil
OUTPUT_DIR = os.path.expanduser("~/Documents")
ODT_PATH = os.path.join(OUTPUT_DIR, "anekdot_blankon.odt")
PDF_PATH = os.path.join(OUTPUT_DIR, "anekdot_blankon.pdf")

# Isi anekdot (3 paragraf)
ANEKDOT = """Suatu hari di warung kopi dekat kampus, ada mahasiswa informatika yang sedang mengeluh.

"Pak, saya sudah belajar coding seharian, tapi programnya tetap error terus," kata mahasiswa itu sambil menyeruput kopi.

Tukang warung yang kebetulan pernah ikut kursus komputer menjawab santai, "Anak muda, error itu bukan musuh. Dia hanya sedang mengajari kamu dengan cara yang agak kasar."
"""

def log(msg):
    print(f"[QA] {msg}")

def wait(sec=1.2):
    time.sleep(sec)

def press_ctrl(key):
    """Tekan kombinasi Ctrl + key"""
    rawinput.pressKey("ctrl")
    rawinput.pressKey(key)
    rawinput.releaseKey(key)
    rawinput.releaseKey("ctrl")
    wait(0.6)

def main():
    log("=== Skenario: 3 Paragraf Anekdot → Export PDF ===")

    # Bersihkan file lama
    for f in [ODT_PATH, PDF_PATH]:
        if os.path.exists(f):
            os.remove(f)
            log(f"File lama dihapus: {f}")

    # 1. Buka LibreOffice Writer
    log("Membuka LibreOffice Writer...")
    run("libreoffice --writer", appName="soffice")
    wait(4.5)

    # 2. Cari aplikasi
    try:
        app = root.application("soffice")
    except Exception:
        app = root.application("libreoffice")
    log("Aplikasi ditemukan")

    # 3. Ambil jendela utama
    try:
        win = app.window("Untitled 1")
    except Exception:
        try:
            win = app.window("Dokumen tanpa judul 1")
        except Exception:
            win = app.children[0]
    log(f"Jendela aktif: {win.name}")

    wait(1)
    win.click()          # pastikan fokus
    wait(0.5)

    # 4. Ketik 3 paragraf anekdot
    log("Mengetik 3 paragraf anekdot...")
    rawinput.typeText(ANEKDOT)
    wait(1.5)
    log("Teks berhasil diketik")

    # 5. Simpan dulu sebagai ODT (opsional tapi disarankan)
    log("Menyimpan sebagai ODT...")
    press_ctrl("s")
    wait(1.8)

    # Isi nama file di dialog Save
    rawinput.typeText(ODT_PATH)
    wait(0.6)
    rawinput.pressKey("Return")
    wait(2)
    log(f"ODT disimpan: {ODT_PATH}")

    # 6. Export ke PDF
    # Cara paling stabil: File → Export As → Export as PDF
    log("Membuka dialog Export as PDF...")

    # Buka menu File
    press_ctrl("f")          # kadang tidak konsisten, jadi kita pakai Alt
    wait(0.4)

    # Alternatif lebih andal: gunakan shortcut atau navigasi menu
    # Tekan Alt + F (menu File)
    rawinput.pressKey("alt")
    rawinput.pressKey("f")
    rawinput.releaseKey("f")
    rawinput.releaseKey("alt")
    wait(0.8)

    # Panah bawah sampai "Export As" / "Ekspor Sebagai"
    # Karena beda bahasa, kita pakai cara yang lebih aman:
    # Langsung pakai dialog Export as PDF lewat perintah
    # Cara paling stabil di banyak versi LO:
    rawinput.pressKey("Escape")   # tutup menu dulu
    wait(0.4)

    # Gunakan cara keyboard yang umum bekerja:
    # File → Export As → Export as PDF (lewat urutan tombol)
    rawinput.pressKey("alt")
    rawinput.pressKey("f")
    rawinput.releaseKey("f")
    rawinput.releaseKey("alt")
    wait(0.7)

    # Ketik huruf untuk mempercepat (tergantung bahasa)
    # Untuk versi Indonesia biasanya "E" untuk Ekspor
    rawinput.typeText("e")        # Ekspor / Export
    wait(0.5)
    rawinput.typeText("e")        # Export as PDF
    wait(1.5)

    # Jika dialog Export as PDF muncul
    log("Mengisi path PDF...")
    rawinput.typeText(PDF_PATH)
    wait(0.7)
    rawinput.pressKey("Return")   # Export
    wait(3)

    # 7. Tutup LibreOffice
    log("Menutup LibreOffice...")
    press_ctrl("q")
    wait(1.5)

    # Kadang muncul dialog "Save changes?" → pilih Don't Save / Jangan Simpan
    try:
        rawinput.pressKey("alt")
        rawinput.pressKey("n")      # Don't Save / Tidak
        rawinput.releaseKey("n")
        rawinput.releaseKey("alt")
    except:
        pass

    wait(1)

    # 8. Verifikasi hasil
    log("Memverifikasi hasil...")
    odt_ok = os.path.exists(ODT_PATH)
    pdf_ok = os.path.exists(PDF_PATH)

    print("\n" + "="*50)
    if odt_ok:
        print(f"ODT  : PASS  ({os.path.getsize(ODT_PATH)} bytes)")
    else:
        print("ODT  : FAIL  (file tidak ditemukan)")

    if pdf_ok:
        print(f"PDF  : PASS  ({os.path.getsize(PDF_PATH)} bytes)")
        print(f"Lokasi PDF: {PDF_PATH}")
    else:
        print("PDF  : FAIL  (file tidak ditemukan)")

    print("="*50)

    if odt_ok and pdf_ok:
        log("SEMUA TEST BERHASIL (PASS)")
        return 0
    else:
        log("ADA YANG GAGAL (FAIL)")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nDibatalkan oleh user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
