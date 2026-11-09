from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    nis = StringField('NIS Siswa', validators=[DataRequired()])
    username = StringField('Username Baru', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    konfirmasi_password = PasswordField('Konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Daftar Sebagai', choices=[('murid', 'Murid'), ('orangtua', 'Orang Tua')], validators=[DataRequired()])
    submit = SubmitField('Daftar Sekarang')

class PesanForm(FlaskForm):
    isi = TextAreaField('Pesan', validators=[DataRequired()])
    submit = SubmitField('Kirim')

class BalasForm(FlaskForm):
    balasan = TextAreaField('Balasan', validators=[DataRequired()])
    submit = SubmitField('Balas')

class AbsensiForm(FlaskForm):
    siswa_id = SelectField('Siswa', coerce=int, validators=[DataRequired()])
    tanggal = StringField('Tanggal', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Hadir','Hadir'),('Izin','Izin'),('Sakit','Sakit'),('Alpa','Alpa')], validators=[DataRequired()])
    keterangan = TextAreaField('Keterangan', validators=[Optional()])
    submit = SubmitField('Simpan')

class NilaiForm(FlaskForm):
    siswa_id = SelectField('Siswa', coerce=int, validators=[DataRequired()])
    mata_pelajaran = StringField('Mata Pelajaran', validators=[DataRequired()])
    nilai = IntegerField('Nilai', validators=[DataRequired()])
    tanggal = StringField('Tanggal', validators=[DataRequired()])
    jenis = SelectField('Jenis', choices=[('Harian','Harian'),('UTS','UTS'),('UAS','UAS')], validators=[DataRequired()])
    submit = SubmitField('Simpan')

class SiswaForm(FlaskForm):
    nis = StringField('NIS', validators=[DataRequired()])
    nama = StringField('Nama Lengkap', validators=[DataRequired()])
    kelas = StringField('Kelas', validators=[DataRequired()])
    jenis_kelamin = SelectField('Jenis Kelamin', choices=[('L','Laki-laki'),('P','Perempuan')], validators=[DataRequired()])
    submit = SubmitField('Tambah Data Siswa')

class ChangePasswordForm(FlaskForm):
    password_lama = PasswordField('Password Lama', validators=[DataRequired()])
    password_baru = PasswordField('Password Baru', validators=[DataRequired(), Length(min=6)])
    konfirmasi_password = PasswordField('Konfirmasi Password Baru', validators=[DataRequired(), EqualTo('password_baru')])
    submit = SubmitField('Ubah Password')

class PrestasiForm(FlaskForm):
    siswa_id = SelectField('Siswa', coerce=int, validators=[DataRequired()])
    judul = StringField('Nama Prestasi / Juara', validators=[DataRequired()])
    deskripsi = TextAreaField('Deskripsi (Opsional)', validators=[Optional()])
    tanggal = StringField('Tanggal (YYYY-MM-DD)', validators=[DataRequired()])
    submit = SubmitField('Simpan Prestasi')

class PelanggaranForm(FlaskForm):
    siswa_id = SelectField('Siswa', coerce=int, validators=[DataRequired()])
    jenis = StringField('Jenis Pelanggaran', validators=[DataRequired()])
    poin = IntegerField('Poin Pelanggaran', validators=[DataRequired()])
    keterangan = TextAreaField('Keterangan (Opsional)', validators=[Optional()])
    tanggal = StringField('Tanggal (YYYY-MM-DD)', validators=[DataRequired()])
    submit = SubmitField('Simpan Pelanggaran')