import requests
from bs4 import BeautifulSoup
import json

url = "https://umsida.ac.id/jadi-kebanggaan-sidoarjo-sekda-sanjung-umsida/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print("Gagal mengambil halaman:", e)
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# ======================
# BAGIAN JUDULNYA
# ======================
judul_tag = soup.find("h1")
judul = judul_tag.get_text(strip=True) if judul_tag else "Tidak ditemukan"

# ======================
# AMBIL TANGGAL (khusus struktur UMSIDA)
# ======================
tanggal = "Tidak ditemukan"

# coba beberapa kemungkinan lokasi tanggal
selectors_tanggal = [
    ("time", {}),
    ("span", {"class": "entry-date"}),
    ("p", {"class": "post-date"}),
    ("div", {"class": "td-post-date"}),
]

for tag, attr in selectors_tanggal:
    el = soup.find(tag, attr)
    if el and el.get_text(strip=True):
        tanggal = el.get_text(strip=True)
        break

# ======================
# AMBIL ISI ARTIKEL (fokus ke konten utama)
# ======================
isi_list = []

# cari container artikel (umumnya dipakai wordpress)
content = soup.find("div", class_="td-post-content")

if not content:
    content = soup.find("article")

if content:
    paragraphs = content.find_all("p")
else:
    paragraphs = soup.find_all("p")  # fallback terakhir

for p in paragraphs:
    text = p.get_text(strip=True)
    if text:
        isi_list.append(text)

isi = " ".join(isi_list)

# ======================
# STRUCTURE JSON
# ======================
data = {
    "url": url,
    "judul": judul,
    "tanggal": tanggal,
    "isi": isi
}

# ======================
# SIMPAN JSON
# ======================
try:
    with open("hasil_umsida.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("✅ Berhasil! File: hasil_umsida.json")
except Exception as e:
    print("Gagal menyimpan file:", e)
