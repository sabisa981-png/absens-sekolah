from datetime import datetime
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'guru', 'murid', 'orangtua'
    nama_lengkap = db.Column(db.String(100), nullable=False)
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'), nullable=True)
    siswa = db.relationship('Siswa', backref='users')

class Siswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nis = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    kelas = db.Column(db.String(20), nullable=False)
    jenis_kelamin = db.Column(db.String(10), nullable=False)
    tanggal_lahir = db.Column(db.String(20), nullable=True)
    alamat = db.Column(db.Text, nullable=True)

    absensi = db.relationship('Absensi', backref='siswa', lazy=True, cascade='all, delete-orphan')
    nilai = db.relationship('Nilai', backref='siswa', lazy=True, cascade='all, delete-orphan')
    prestasi = db.relationship('Prestasi', backref='siswa', lazy=True, cascade='all, delete-orphan')
    pelanggaran = db.relationship('Pelanggaran', backref='siswa', lazy=True, cascade='all, delete-orphan')

class Absensi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'), nullable=False)
    tanggal = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # Hadir, Izin, Sakit, Alpa
    keterangan = db.Column(db.Text, nullable=True)

class Nilai(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'), nullable=False)
    mata_pelajaran = db.Column(db.String(50), nullable=False)
    nilai = db.Column(db.Integer, nullable=False)
    tanggal = db.Column(db.String(20), nullable=False)
    jenis = db.Column(db.String(20), nullable=False)  # Harian, UTS, UAS

class Prestasi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'), nullable=False)
    judul = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.Text, nullable=True)
    tanggal = db.Column(db.String(20), nullable=False)

class Pelanggaran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'), nullable=False)
    jenis = db.Column(db.String(100), nullable=False)
    poin = db.Column(db.Integer, nullable=False)
    tanggal = db.Column(db.String(20), nullable=False)
    keterangan = db.Column(db.Text, nullable=True)

class Pesan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pengirim_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'), nullable=True)
    isi = db.Column(db.Text, nullable=False)
    tanggal = db.Column(db.String(20), default=datetime.now().strftime("%Y-%m-%d %H:%M"))
    balasan = db.Column(db.Text, nullable=True)
    tanggal_balasan = db.Column(db.String(20), nullable=True)

    pengirim = db.relationship('User', foreign_keys=[pengirim_id])
    siswa = db.relationship('Siswa')