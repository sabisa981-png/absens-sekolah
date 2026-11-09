from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()
    
    # Membuat 1 akun admin/guru jika database masih kosong
    if not User.query.first():
        admin = User(
            username="admin", 
            password_hash=generate_password_hash("admin123"), 
            role="guru", 
            nama_lengkap="Administrator Sekolah"
        )
        db.session.add(admin)
        db.session.commit()
        print("Database kosong terdeteksi. Akun Admin berhasil dibuat: admin / admin123")

if __name__ == '__main__':
    app.run(debug=True, port=5000)