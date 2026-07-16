# MediaShare (Web App + TCP Upload + UDP Streaming)

Dokumentasi ini menjelaskan kebutuhan **requirements**, **pembuatan database**, dan langkah sampai **program berjalan** dengan skema:
- **Server dijalankan di VM** (Flask + TCP Server + UDP Server)
- **Client web dijalankan dari VSCode/lokal** (akses browser via URL Cloudflare Free Tunnel)
- **Deploy ekspos server menggunakan Cloudflare Free Tunnel**

---

## 1. Arsitektur Sistem

Aplikasi ini terdiri dari 3 komponen:

1) **Flask Web Server (HTTP)**
- Lokasi: `app.py`
- Menangani:
  - Register/Login (Flask-Login)
  - Verifikasi email (Flask-Mail)
  - Dashboard daftar video user
  - Route streaming ke browser: `/stream/video_feed/<filename>`
  - Upload video melalui endpoint: `/upload` (upload file dari browser)

2) **TCP Server (Upload biner video ke storage VM)**
- Lokasi: `server/tcp_server/tcp_server.py` dan `server/tcp_server/handlers.py`
- Protokol:
  - Command `UPLOAD`
  - Transfer biner file dengan handshake `READY`
  - Disimpan ke folder `server/uploads/`

3) **UDP Server (Streaming raw video chunk untuk ditampilkan di browser)**
- Lokasi: `server/udp_server/udp_server.py`
- Mengirim chunk video biner ke client streaming (UDP packet)
- Client web mengonsumsi stream melalui generator di `client/web/services/udp_service.py`.

Komunikasi penting:
- Flask <-> DB: SQLAlchemy
- Flask <-> TCP Server: upload file (chunk)
- Flask <-> UDP Server: streaming (Flask membungkus UDP generator menjadi Response `video/mp4`)

---

## 2. Requirements Runtime

### 2.1. Software yang dibutuhkan
- **Python 3.10+** (disarankan)
- **MySQL / MariaDB** (untuk database `mediashare`)
- **SMTP Mail Server** (untuk fitur verifikasi email)
- **Port akses dari internet** ke VM untuk Flask (default 5000)

### 2.2. Python dependencies
Install dependency dari `requirements.txt`:

```bash
pip install -r requirements.txt
```

> Daftar library di `requirements.txt` mencakup: Flask, Flask-Login, Flask-Mail, Flask-SQLAlchemy, PyMySQL, openCV, dll.

---

## 3. Setup Database (MySQL/MariaDB)

### 3.1. Buat database
Buat database bernama:
- `mediashare`

Contoh (dengan user root):
```sql
CREATE DATABASE mediashare;
```

### 3.2. Import skema
Import isi file:
- `mediashare.sql`

Contoh:
```bash
mysql -u <DB_USER> -p mediashare < mediashare.sql
```

Skema yang dibuat:
- Tabel `users`
- Tabel `videos` (FK ke `users.id`)

---

## 4. Setup Environment Variables (Wajib)

Konfigurasi aplikasi membaca file `.env` (dipanggil dari `client/web/config.py`).
Buat file `.env` di **root proyek** (satu level dengan `app.py`).

### 4.1. Variabel yang dibutuhkan (sesuai pemakaian di code)
Isi minimal berikut:

```env
# Secret untuk Flask session
SECRET_KEY=change_me

# Database
DB_HOST=127.0.0.1
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=mediashare

# Mail (SMTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email
MAIL_PASSWORD=your_email_password_or_app_password

# Base URL aplikasi (dipakai untuk link verifikasi)
BASE_URL=https://<cloudflare-tunnel-url>

# IP/Port server internal untuk TCP/UDP
TCP_SERVER_IP=127.0.0.1
TCP_SERVER_PORT=5001
UDP_SERVER_IP=127.0.0.1
UDP_SERVER_PORT=5002
```

> Pada `shared/constants.py` ada `SERVER_IP = "192.168.146.114"`. Nilai ini dipakai oleh TCP/UDP client saat mengirim request. Pada deploy VM real, pastikan `SERVER_IP` mengarah ke IP VM/host server.


## 5. Setup Server di VM

### 5.1. Buka port yang diperlukan
Pastikan VM menerima:
- **5000/tcp**: Flask HTTP
- **5001/tcp**: TCP upload server
- **5002/udp**: UDP streaming server

> Sesuaikan aturan firewall sesuai OS VM.

### 5.2. Jalankan 3 service Python
Di VM, aktifkan venv (disarankan):

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Lalu jalankan:

#### (A) Flask Web Server
```bash
python app.py
```

`app.py` menjalankan Flask dengan:
- `host="0.0.0.0"`
- `port=5000`

#### (B) TCP Upload Server
```bash
python server\tcp_server\tcp_server.py
```

#### (C) UDP Streaming Server
```bash
python server\udp_server\udp_server.py
```

### 5.3. Storage upload video
Server menyimpan file ke folder:
- `server/uploads/`

---

## 6. Setup Client di VSCode (lalu diakses via Cloudflare Free Tunnel)

Client di proyek ini pada dasarnya adalah **akses web Flask** (bukan aplikasi yang harus “run build frontend”).

Yang perlu dilakukan dari VSCode/lokal:
- Siapkan environment Python hanya jika kamu perlu menjalankan komponen client Python (TCP/UDP client).
- Untuk penggunaan normal, cukup buka URL Web dari Cloudflare Tunnel.

Namun pada kode, streaming & upload video dilakukan lewat backend Flask pada server, dan TCP/UDP server ada di VM.

### 6.1. Jalankan/akses dari browser
- Buka alamat Cloudflare Tunnel (mis. `https://xxxx.trycloudflare.com`)
- Lakukan:
  - Register
  - Verifikasi email
  - Login
  - Upload video
  - Mainkan video di dashboard

---

## 7. Deploy Menggunakan Cloudflare Free Tunnel

### 7.1. Tujuan
Cloudflare Free Tunnel dipakai agar VM tidak perlu port-forward manual ke router.

### 7.2. Langkah umum (lokal / di VM)
1. Install `cloudflared`
2. Login
3. Buat tunnel
4. Buat ingress yang mem-forward traffic ke Flask port `5000`

Contoh prinsip konfigurasi ingress (konsep):
- HTTP(S) masuk -> service Flask di `http://localhost:5000`

> Tunnel Free umumnya melayani HTTP/HTTPS. Pada arsitektur proyek ini:
> - **Web (Flask) lewat HTTP tunnel**
> - Streaming video ditangani oleh Flask yang membungkus generator UDP. Pastikan link dari UDP server tetap dapat diakses dari VM.

### 7.3. Pastikan BASE_URL benar
Set `BASE_URL` di `.env` agar link verifikasi email mengarah ke URL tunnel.

---

## 8. Cara Uji Coba End-to-End (Checklist)

### 8.1. Setup awal
- DB sudah terbuat dan `mediashare.sql` sudah diimport
- `.env` sudah benar
- 3 service server sudah jalan:
  - Flask (5000)
  - TCP upload (5001)
  - UDP streaming (5002)

### 8.2. Uji fitur register & verifikasi email
1. Akses `/register`
2. Isi username/email/password
3. Buka email untuk verifikasi link
4. Cek akun sudah `is_verified=True`

### 8.3. Uji login
- Login menggunakan email + password
- Pastikan diarahkan ke dashboard: `/dashboard`

### 8.4. Uji upload
- Dari dashboard, upload file video
- Proses:
  - Flask menyimpan file sementara
  - Flask memanggil `TCPClient.upload_file()` ke TCP server
  - TCP server menyimpan ke `server/uploads/`
  - Flask menyimpan metadata ke tabel `videos`

### 8.5. Uji streaming video
- Pada dashboard, klik video
- Route streaming: `/stream/video_feed/<filename>`
- Flask mengirim Response mimetype `video/mp4`.

---

## 9. Troubleshooting (yang paling sering)

1) **Flask tidak bisa diakses dari internet**
- Pastikan Flask `host=0.0.0.0` sudah benar (di `app.py` sudah)
- Pastikan Cloudflare tunnel mengarah ke port 5000

2) **Upload gagal / TCP error**
- Cocokkan IP/port di:
  - `shared/constants.py` (SERVER_IP, TCP_PORT)
  - `.env` untuk `TCP_SERVER_IP/TCP_SERVER_PORT`

3) **Streaming gagal**
- Pastikan UDP server running di VM
- Pastikan firewall UDP 5002 terbuka

4) **Verifikasi email tidak masuk / link tidak benar**
- Pastikan SMTP settings di `.env` benar
- Pastikan `BASE_URL` sesuai URL tunnel

---

## 10. Referensi File Penting

- Flask: `app.py`
- Config `.env`: `client/web/config.py`
- Model DB:
  - `client/web/models/user.py`
  - `client/web/models/video.py`
- Route auth: `client/web/routes/auth.py`
- Route dashboard: `client/web/routes/dashboard.py`
- Route upload: `client/web/routes/upload.py`
- Route streaming: `client/web/routes/stream.py`
- TCP Server: `server/tcp_server/tcp_server.py`, `server/tcp_server/handlers.py`
- UDP Server: `server/udp_server/udp_server.py`
- UDP client generator (untuk streaming ke browser): `client/web/services/udp_service.py`
- TCP client upload helper: `client/web/services/tcp_service.py`

---

## How to Run (Ringkas)

### Di VM
1) Import DB
2) Edit `.env`
3) Run:
```bash
python app.py
python server\tcp_server\tcp_server.py
python server\udp_server\udp_server.py
```
4) Jalankan Cloudflare tunnel ke `localhost:5000`

### Di Browser
- Buka URL tunnel
- Login/Register -> Upload -> Play video

