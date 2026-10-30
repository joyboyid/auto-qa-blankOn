Tempel ini ke chat AI:

---

Baca peta tes saya di docs/map-feature.md (BlankOn QA).
Saya QA volunteer BlankOn Linux (Sinambung / Revival). Tiket: https://github.com/BlankOn/revival/issues

Saya punya template Ansible blankon-qa-map:
- satu cabang peta = satu role
- satu daun = satu file tasks + ID (IN- UEFI, HW-WIFI, SY-REPO, LO-TZ, AP-BR, IF-ISO, ...)
- hasil: qa_results (JANGAN pakai nama results)
- kasus: id, area, kasus, ok, evidence
- playbooks/qa.yaml + tags sesuai cabang/daun

Automasi hanya deteksi. Jangan ubah SUT. changed_when: false.
Installer partisi, lock screen, pairing, upgrade penuh, shutdown, pipeline: SKIP atau manual.
Jangan klaim PASS tanpa bukti.
Timezone: baca field "Time zone:" saja.

Kalau saya minta kerja: YAML siap tempel + perintah run (tag + -e jahitan=...).
Bahasa Indonesia, ringkas.

---

Pendek:

QA BlankOn. Automasi template dari map-feature.md. Ansible blankon-qa-map, variabel qa_results. Deteksi saja. YAML siap tempel + cara run.
