import os

class Config:
    SECRET_KEY = 'kunci-rahasia-super-aman-absensi-2026'
    
    # Ini perintahnya: "Cari DATABASE_URL di server. Kalau tidak ada (saat di laptop), pakai SQLite."
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///absensi.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False