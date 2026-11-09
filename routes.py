from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import User, Siswa, Absensi, Nilai, Prestasi, Pelanggaran, Pesan
from app.forms import (LoginForm, RegisterForm, PesanForm, BalasForm, AbsensiForm, 
                       NilaiForm, SiswaForm, ChangePasswordForm, PrestasiForm, PelanggaranForm)
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Username atau Password salah!', 'danger')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        siswa = Siswa.query.filter_by(nis=form.nis.data).first()
        if not siswa:
            flash('NIS tidak ditemukan. Pastikan Anda meminta NIS ke Guru/Admin.', 'danger')
            return redirect(url_for('main.register'))
        
        if User.query.filter_by(username=form.username.data).first():
            flash('Username sudah digunakan, silakan pilih yang lain.', 'danger')
            return redirect(url_for('main.register'))
            
        new_user = User(
            username=form.username.data,
            password_hash=generate_password_hash(form.password.data),
            role=form.role.data,
            nama_lengkap=siswa.nama if form.role.data == 'murid' else f"Ortu {siswa.nama}",
            siswa_id=siswa.id
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Pendaftaran berhasil! Silakan login.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'guru': return redirect(url_for('main.dashboard_guru'))
    elif current_user.role == 'orangtua': return redirect(url_for('main.dashboard_orangtua'))
    elif current_user.role == 'murid': return redirect(url_for('main.dashboard_murid'))
    return "Role tidak dikenali"

@main.route('/ubah_password', methods=['GET', 'POST'])
@login_required
def ubah_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.password_hash, form.password_lama.data):
            current_user.password_hash = generate_password_hash(form.password_baru.data)
            db.session.commit()
            flash('Password berhasil diubah! Silakan login kembali.', 'success')
            return redirect(url_for('main.logout'))
        else:
            flash('Password lama salah!', 'danger')
    return render_template('ubah_password.html', form=form)

# ================== AREA GURU ==================
@main.route('/guru')
@login_required
def dashboard_guru():
    if current_user.role != 'guru': return redirect(url_for('main.dashboard'))
    semua_siswa = Siswa.query.all()
    pesan_masuk = Pesan.query.order_by(Pesan.id.desc()).all()
    return render_template('dashboard_guru.html', siswa=semua_siswa, pesan=pesan_masuk)

@main.route('/guru/tambah_siswa', methods=['GET', 'POST'])
@login_required
def guru_tambah_siswa():
    if current_user.role != 'guru': return redirect(url_for('main.dashboard'))
    form = SiswaForm()
    if form.validate_on_submit():
        if Siswa.query.filter_by(nis=form.nis.data).first():
            flash('NIS sudah terdaftar di sistem!', 'danger')
            return redirect(url_for('main.guru_tambah_siswa'))
        siswa_baru = Siswa(nis=form.nis.data, nama=form.nama.data, kelas=form.kelas.data, jenis_kelamin=form.jenis_kelamin.data)
        db.session.add(siswa_baru)
        db.session.commit()
        flash('Data siswa berhasil ditambahkan!', 'success')
        return redirect(url_for('main.dashboard_guru'))
    return render_template('tambah_siswa.html', form=form)

@main.route('/guru/absensi', methods=['GET', 'POST'])
@login_required
def guru_absensi():
    if current_user.role != 'guru': return redirect(url_for('main.dashboard'))
    form = AbsensiForm()
    form.siswa_id.choices = [(s.id, f"{s.nama} ({s.kelas})") for s in Siswa.query.all()]
    if form.validate_on_submit():
        absen = Absensi(siswa_id=form.siswa_id.data, tanggal=form.tanggal.data, status=form.status.data, keterangan=form.keterangan.data)
        db.session.add(absen)
        db.session.commit()
        flash('Absensi berhasil disimpan!', 'success')
        return redirect(url_for('main.guru_absensi'))
    riwayat = Absensi.query.order_by(Absensi.tanggal.desc()).limit(20).all()
    return render_template('absensi.html', form=form, riwayat=riwayat)

@main.route('/guru/nilai', methods=['GET', 'POST'])
@login_required
def guru_nilai():
    if current_user.role != 'guru': return redirect(url_for('main.dashboard'))
    form = NilaiForm()
    form.siswa_id.choices = [(s.id, f"{s.nama} ({s.kelas})") for s in Siswa.query.all()]
    if form.validate_on_submit():
        nilai = Nilai(siswa_id=form.siswa_id.data, mata_pelajaran=form.mata_pelajaran.data, nilai=form.nilai.data, tanggal=form.tanggal.data, jenis=form.jenis.data)
        db.session.add(nilai)
        db.session.commit()
        flash('Nilai berhasil disimpan!', 'success')
        return redirect(url_for('main.guru_nilai'))
    riwayat = Nilai.query.order_by(Nilai.tanggal.desc()).limit(20).all()
    return render_template('nilai.html', form=form, riwayat=riwayat)

@main.route('/guru/prestasi', methods=['GET', 'POST'])
@login_required
def guru_prestasi():
    if current_user.role != 'guru': return redirect(url_for('main.dashboard'))
    form = PrestasiForm()
    form.siswa_id.choices = [(s.id, f"{s.nama} ({s.kelas})") for s in Siswa.query.all()]
    if form.validate_on_submit():
        prestasi = Prestasi(siswa_id=form.siswa_id.data, judul=form.judul.data, deskripsi=form.deskripsi.data, tanggal=form.tanggal.data)
        db.session.add(prestasi)
        db.session.commit()
        flash('Prestasi berhasil ditambahkan!', 'success')
        return redirect(url_for('main.guru_prestasi'))
    riwayat = Prestasi.query.order_by(Prestasi.tanggal.desc()).limit(20).all()
    return render_template('prestasi.html', form=form, riwayat=riwayat)

@main.route('/guru/pelanggaran', methods=['GET', 'POST'])
@login_required
def guru_pelanggaran():
    if current_user.role != 'guru': return redirect(url_for('main.dashboard'))
    form = PelanggaranForm()
    form.siswa_id.choices = [(s.id, f"{s.nama} ({s.kelas})") for s in Siswa.query.all()]
    if form.validate_on_submit():
        pelanggaran = Pelanggaran(siswa_id=form.siswa_id.data, jenis=form.jenis.data, poin=form.poin.data, keterangan=form.keterangan.data, tanggal=form.tanggal.data)
        db.session.add(pelanggaran)
        db.session.commit()
        flash('Pelanggaran berhasil dicatat!', 'success')
        return redirect(url_for('main.guru_pelanggaran'))
    riwayat = Pelanggaran.query.order_by(Pelanggaran.tanggal.desc()).limit(20).all()
    return render_template('pelanggaran.html', form=form, riwayat=riwayat)

@main.route('/guru/pesan', methods=['GET', 'POST'])
@login_required
def guru_pesan():
    if current_user.role != 'guru': return redirect(url_for('main.dashboard'))
    form_balas = BalasForm()
    if form_balas.validate_on_submit():
        pesan_id = request.form.get('pesan_id')
        pesan = Pesan.query.get(pesan_id)
        if pesan:
            pesan.balasan = form_balas.balasan.data
            pesan.tanggal_balasan = datetime.now().strftime("%Y-%m-%d %H:%M")
            db.session.commit()
            flash('Balasan terkirim!', 'success')
            return redirect(url_for('main.guru_pesan'))
    semua_pesan = Pesan.query.order_by(Pesan.id.desc()).all()
    return render_template('pesan.html', pesan=semua_pesan, form_balas=form_balas)

# ================== AREA ORANG TUA ==================
@main.route('/orangtua', methods=['GET', 'POST'])
@login_required
def dashboard_orangtua():
    if current_user.role != 'orangtua': return redirect(url_for('main.dashboard'))
    form = PesanForm()
    if form.validate_on_submit():
        pesan = Pesan(pengirim_id=current_user.id, siswa_id=current_user.siswa_id, isi=form.isi.data)
        db.session.add(pesan)
        db.session.commit()
        flash('Pesan terkirim ke Guru!', 'success')
        return redirect(url_for('main.dashboard_orangtua'))
    siswa = current_user.siswa
    absensi = Absensi.query.filter_by(siswa_id=siswa.id).order_by(Absensi.tanggal.desc()).all() if siswa else []
    nilai = Nilai.query.filter_by(siswa_id=siswa.id).order_by(Nilai.tanggal.desc()).all() if siswa else []
    prestasi = Prestasi.query.filter_by(siswa_id=siswa.id).all() if siswa else []
    pelanggaran = Pelanggaran.query.filter_by(siswa_id=siswa.id).all() if siswa else []
    riwayat_pesan = Pesan.query.filter_by(pengirim_id=current_user.id).order_by(Pesan.id.desc()).all()
    return render_template('dashboard_orangtua.html', siswa=siswa, absensi=absensi, nilai=nilai, prestasi=prestasi, pelanggaran=pelanggaran, pesan=riwayat_pesan, form=form)

# ================== AREA MURID ==================
@main.route('/murid')
@login_required
def dashboard_murid():
    if current_user.role != 'murid': return redirect(url_for('main.dashboard'))
    siswa = current_user.siswa
    absensi = Absensi.query.filter_by(siswa_id=siswa.id).order_by(Absensi.tanggal.desc()).all() if siswa else []
    prestasi = Prestasi.query.filter_by(siswa_id=siswa.id).all() if siswa else []
    hari_ini = datetime.now().strftime("%Y-%m-%d")
    sudah_absen = Absensi.query.filter_by(siswa_id=siswa.id, tanggal=hari_ini).first() is not None if siswa else True
    return render_template('dashboard_murid.html', siswa=siswa, absensi=absensi, prestasi=prestasi, sudah_absen=sudah_absen)

@main.route('/murid/absen', methods=['POST'])
@login_required
def murid_absen():
    if current_user.role != 'murid': return redirect(url_for('main.dashboard'))
    siswa = current_user.siswa
    hari_ini = datetime.now().strftime("%Y-%m-%d")
    status = request.form.get('status')
    existing = Absensi.query.filter_by(siswa_id=siswa.id, tanggal=hari_ini).first()
    if existing:
        flash('Anda sudah melakukan absensi hari ini.', 'warning')
    else:
        absen_baru = Absensi(siswa_id=siswa.id, tanggal=hari_ini, status=status)
        db.session.add(absen_baru)
        db.session.commit()
        flash(f'Absensi berhasil! Status: {status}', 'success')
    return redirect(url_for('main.dashboard_murid'))