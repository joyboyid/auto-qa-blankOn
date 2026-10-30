# Template Ansible dari map-feature.md — QA BlankOn

Pohon tes = `docs/map-feature.md`. Satu cabang = satu role. Satu daun = file tasks + ID.

```
Installation Desktop Hardware System Localization Applications Infrastructure
```

## 1. Pasang

Di BlankOn (live atau terpasang):

```bash
tar -xzf blankon-qa-map.tar.gz
cd blankon-qa-map
sudo apt install -y ansible-core
```

Opsional (biar leaf hardware/lokal lebih lengkap):

```bash
sudo apt install -y iw network-manager bluez alsa-utils pulseaudio-utils \
  libinput-tools pciutils fontconfig
```

## 2. Cek config

```bash
ansible-playbook playbooks/qa.yaml --syntax-check
ansible-inventory --graph
```

## 3. Jalankan

Semua cabang:

```bash
sudo ansible-playbook -i inventory/inventory.ini -l localhost playbooks/qa.yaml \
  -e jahitan=J20260930 \
  -e target_zone=Asia/Makassar
```

Satu cabang:

```bash
sudo ansible-playbook -i inventory/inventory.ini -l localhost playbooks/qa.yaml \
  --tags hardware \
  -e jahitan=J20260930
```

Satu daun:

```bash
sudo ansible-playbook -i inventory/inventory.ini -l localhost playbooks/qa.yaml \
  --tags wifi \
  -e jahitan=J20260930
```

Tag cabang: `installation` `desktop` `hardware` `system` `localization` `applications` `infrastructure`  
Tag daun contoh: `wifi` `timezone` `repo` `uefi`

## 4. Baca hasil

Layar: `PASS [HW-WIFI-1] ...` lalu verdict LULUS/GAGAL.  
JSON: `/tmp/qa-results-<hostname>.json`

Laporan:

```bash
ansible-playbook playbooks/generate-report.yaml \
  -e jahitan=J20260930 \
  -e results_file=/tmp/qa-results-localhost.json
```

## 5. Arti config

| File | Fungsi |
|---|---|
| `ansible.cfg` | inventory + roles_path |
| `inventory/inventory.ini` | host: local / hardware / infra |
| `inventory/group_vars/blankon.yml` | `jahitan`, `target_zone`, `qa_results`, flag SKIP |
| `playbooks/qa.yaml` | urutan role = urutan peta |
| `roles/<cabang>/tasks/` | daun |

Variabel penting (`group_vars` atau `-e`):

- `jahitan` — label ISO
- `target_zone` — `Asia/Makassar` atau `Asia/Jakarta`
- `skip_manual_install_leaves=true` — jangan anggap FAIL untuk partisi manual
- `skip_infra_leaves=true` — ISO/IRGSH tidak diuji di laptop

## 6. Yang diotomasi vs manual

Otomasi: deteksi (device, paket, locale, repo, systemd).  
Manual tetap: installer partisi, lock/logout, pairing BT, suara, suspend sungguhan, pipeline rilis.

FAIL Wi-Fi di VM itu wajar. Tes hardware di laptop fisik (`-l hardware`).

## 7. Tambah daun

1. Tulis `roles/<cabang>/tasks/daun-baru.yml`
2. `include_tasks` + `tags` di `main.yml` cabang itu
3. Append ke `qa_results`, **bukan** `results`
4. Field wajib: `id`, `area`, `kasus`, `ok`, `evidence`

Tiket: https://github.com/BlankOn/revival/issues
