import os

class Config:
    SECRET_KEY = 'kunci-rahasia-super-aman-absensi-2026'
    # Gunakan SQLite untuk PythonAnywhere
    SQLALCHEMY_DATABASE_URI = 'sqlite:///absensi.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
