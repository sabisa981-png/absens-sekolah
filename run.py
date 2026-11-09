from app import create_app, db

# Inisialisasi aplikasi di tingkat modul agar bisa dibaca oleh Gunicorn
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Ini hanya untuk menjalankan di laptop lokal Anda
    app.run(debug=True, port=5000)
