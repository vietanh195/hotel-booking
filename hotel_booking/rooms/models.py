# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Diadiem(models.Model):
    diadiem_id = models.CharField(primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    tendiadiem = models.CharField(db_column='tenDiaDiem', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DiaDiem'


class Dondatphong(models.Model):
    lichsu_id = models.CharField(primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    ngaydat = models.DateField(db_column='ngayDat', blank=True, null=True)  # Field name made lowercase.
    ngaytra = models.DateField(db_column='ngayTra', blank=True, null=True)  # Field name made lowercase.
    tongtien = models.FloatField(db_column='tongTien', blank=True, null=True)  # Field name made lowercase.
    trangthai = models.CharField(db_column='trangThai', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    thoigiandat = models.DateField(db_column='thoiGianDat', blank=True, null=True)  # Field name made lowercase.
    nguoidungnguoidung = models.ForeignKey('Nguoidung', models.DO_NOTHING, db_column='NguoiDungnguoidung_id', blank=True, null=True)  # Field name made lowercase.
    phongphong = models.ForeignKey('Loaiphong', models.DO_NOTHING, db_column='Phongphong_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DonDatPhong'


class Hinhanh(models.Model):
    anh_id = models.CharField(primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    urlhinhanh = models.CharField(db_column='urlHinhAnh', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    phongphong = models.ForeignKey('Loaiphong', models.DO_NOTHING, db_column='Phongphong_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HinhAnh'


class Khachsan(models.Model):
    khachsan_id = models.CharField(primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    tenkhachsan = models.CharField(db_column='tenKhachSan', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mota = models.CharField(db_column='moTa', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ngaythem = models.DateField(db_column='ngayThem', blank=True, null=True)  # Field name made lowercase.
    quanhuyenquanhuyen = models.ForeignKey('Quanhuyen', models.DO_NOTHING, db_column='QuanHuyenquanhuyen_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KhachSan'


class Loaiphong(models.Model):
    phong_id = models.CharField(primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    tenphong = models.CharField(db_column='tenPhong', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sogiuong = models.IntegerField(db_column='soGiuong', blank=True, null=True)  # Field name made lowercase.
    gia = models.FloatField(blank=True, null=True)
    mota = models.CharField(db_column='moTa', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ngaythemphong = models.DateField(db_column='ngayThemPhong', blank=True, null=True)  # Field name made lowercase.
    khachsankhachsan = models.ForeignKey(Khachsan, models.DO_NOTHING, db_column='KhachSankhachsan_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LoaiPhong'


class Nguoidung(models.Model):
    nguoidung_id = models.CharField(primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    tennguoidung = models.CharField(db_column='tenNguoiDung', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    matkhau = models.CharField(db_column='matKhau', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dienthoai = models.CharField(db_column='dienThoai', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    vaitro = models.CharField(db_column='vaiTro', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ngaytaotk = models.DateField(db_column='ngayTaoTK', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NguoiDung'


class Quanhuyen(models.Model):
    quanhuyen_id = models.CharField(primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    tenquanhuyen = models.CharField(db_column='tenQuanHuyen', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    diadiemdiadiem = models.ForeignKey(Diadiem, models.DO_NOTHING, db_column='DiaDiemdiadiem_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QuanHuyen'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)
