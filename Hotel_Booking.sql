USE MASTER;
GO
CREATE DATABASE Hotel_Booking;
GO
USE Hotel_Booking;
GO

-- Bảng DiaDiem
CREATE TABLE DiaDiem (
    diadiem_id VARCHAR(20) PRIMARY KEY,
    tenDiaDiem NVARCHAR(100)
);

-- Bảng QuanHuyen
CREATE TABLE QuanHuyen (
    quanhuyen_id VARCHAR(20) PRIMARY KEY,
    tenQuanHuyen NVARCHAR(100),
    DiaDiemdiadiem_id VARCHAR(20)
	FOREIGN KEY (DiaDiemdiadiem_id) REFERENCES DiaDiem(diadiem_id)
);

-- Bảng KhachSan
CREATE TABLE KhachSan (
    khachsan_id VARCHAR(20) PRIMARY KEY,
    tenKhachSan NVARCHAR(200),
    moTa NVARCHAR(1000),
    ngayThem DATE,
    QuanHuyenquanhuyen_id VARCHAR(20), -- Khóa ngoại tham chiếu đến bảng DiaDiem
    FOREIGN KEY (QuanHuyenquanhuyen_id) REFERENCES QuanHuyen(quanhuyen_id)
);

-- Bảng LoaiPhong
CREATE TABLE LoaiPhong (
    phong_id VARCHAR(20) PRIMARY KEY,
    tenPhong VARCHAR(100),
    soGiuong INTEGER,
    gia FLOAT,
    moTa VARCHAR(1000),
    ngayThemPhong DATE,
    KhachSankhachsan_id VARCHAR(20), -- Khóa ngoại tham chiếu đến bảng KhachSan
    FOREIGN KEY (KhachSankhachsan_id) REFERENCES KhachSan(khachsan_id)
);

-- Bảng HinhAnh
CREATE TABLE HinhAnh (
    anh_id VARCHAR(20) PRIMARY KEY,
    urlHinhAnh VARCHAR(300),
    Phongphong_id VARCHAR(20), -- Khóa ngoại tham chiếu đến bảng LoaiPhong
	FOREIGN KEY (Phongphong_id) REFERENCES LoaiPhong(phong_id)
);

-- Bảng NguoiDung
CREATE TABLE NguoiDung (
    nguoidung_id VARCHAR(20) PRIMARY KEY,
    tenNguoiDung VARCHAR(100),
    email VARCHAR(100),
    matKhau VARCHAR(100),
    dienThoai VARCHAR(100),
    vaiTro VARCHAR(10),
    ngayTaoTK DATE
);

-- Bảng lichsuDatPhong
CREATE TABLE DonDatPhong (
    lichsu_id VARCHAR(20) PRIMARY KEY,
    ngayDat DATE,
    ngayTra DATE,
    tongTien FLOAT,
    trangThai VARCHAR(20),
    thoiGianDat DATE, 
    NguoiDungnguoidung_id VARCHAR(20), -- Khóa ngoại tham chiếu đến bảng NguoiDung
    Phongphong_id VARCHAR(20), -- Khóa ngoại tham chiếu đến bảng LoaiPhong
    FOREIGN KEY (NguoiDungnguoidung_id) REFERENCES NguoiDung(nguoidung_id),
    FOREIGN KEY (Phongphong_id) REFERENCES LoaiPhong(phong_id)
);

-- Xóa bảng
DROP TABLE DonDatPhong;
DROP TABLE HinhAnh;
DROP TABLE LoaiPhong;
DROP TABLE KhachSan;
DROP TABLE QuanHuyen;
DROP TABLE DiaDiem;
DROP TABLE NguoiDung;

-- Xóa dữ liệu trong bảng DonDatPhong
DELETE FROM DonDatPhong;

-- Xóa bảng HinhAnh (phụ thuộc vào LoaiPhong)
DELETE FROM HinhAnh;

-- Xóa bảng LoaiPhong (phụ thuộc vào KhachSan)
DELETE FROM LoaiPhong;

-- Xóa bảng KhachSan (phụ thuộc vào QuanHuyen)
DELETE FROM KhachSan;

-- Xóa bảng QuanHuyen (phụ thuộc vào DiaDiem)
DELETE FROM QuanHuyen;

-- Xóa bảng DiaDiem (bảng cha gốc)
DELETE FROM DiaDiem;

-- Xóa bảng NguoiDung (không có phụ thuộc ngoài DonDatPhong đã xóa ở trên)
DELETE FROM NguoiDung;


-- Dữ liệu mẫu cho bảng DiaDiem
INSERT INTO DiaDiem VALUES
('DD01', N'Hà Nội'),
('DD02', N'Đà Nẵng'),
('DD03', N'TP. Hồ Chí Minh');


-- Dữ liệu mẫu cho bảng QuanHuyen
-- Hà Nội
INSERT INTO QuanHuyen VALUES
('QH01', N'Hoàn Kiếm', 'DD01'),
('QH02', N'Ba Đình', 'DD01'),
-- Đà Nẵng
('QH03', N'Hải Châu', 'DD02'),
('QH04', N'Ngũ Hành Sơn', 'DD02'),
-- TP.HCM
('QH05', N'Quận 1', 'DD03'),
('QH06', N'Quận 3', 'DD03');


-- Dữ liệu mẫu cho bảng KhachSan
INSERT INTO KhachSan VALUES
('KS01', 'The Royal Lotus', N'123 Phố Huế, Hoàn Kiếm, Hà Nội', '2025-06-01', 'QH01'),
('KS02', 'Emerald Palace', N'45 Kim Mã, Ba Đình, Hà Nội', '2025-06-01', 'QH02'),
('KS03', 'Sunset Boutique', N'88 Bạch Đằng, Hải Châu, Đà Nẵng', '2025-06-01', 'QH03'),
('KS04', 'Ocean Serenity', N'12 Trường Sa, Ngũ Hành Sơn, Đà Nẵng', '2025-06-01', 'QH04'),
('KS05', 'Golden Orchid', N'159 Lý Tự Trọng, Quận 1, TP. HCM', '2025-06-01', 'QH05'),
('KS06', 'Crystal Grand', N'77 Nguyễn Đình Chiểu, Quận 3, TP. HCM', '2025-06-01', 'QH06');


-- Dữ liệu mẫu cho bảng LoaiPhong
-- KS01: The Royal Lotus
INSERT INTO LoaiPhong VALUES
('P001', 'Deluxe King', 1, 1200000, 'Spacious room with city view. Room size: 35m2.', '2025-06-01', 'KS01'),
('P002', 'Executive Suite', 2, 2000000, 'Luxury suite with lounge access. Room size: 50m2.', '2025-06-01', 'KS01'),
('P003', 'Presidential Room', 2, 3500000, 'Top-tier room with premium amenities. Room size: 75m2.', '2025-06-01', 'KS01'),

-- KS02: Emerald Palace
('P004', 'Superior Room', 1, 1000000, 'Comfortable room with elegant design. Room size: 30m2.', '2025-06-01', 'KS02'),
('P005', 'Royal Suite', 2, 2200000, 'Spacious suite with premium services. Room size: 60m2.', '2025-06-01', 'KS02'),
('P006', 'Luxury Twin', 2, 1800000, 'Modern room with twin beds. Room size: 40m2.', '2025-06-01', 'KS02'),

-- KS03: Sunset Boutique
('P007', 'Seaside Deluxe', 1, 1400000, 'Ocean view with private balcony. Room size: 35m2.', '2025-06-01', 'KS03'),
('P008', 'Sunset Suite', 2, 2100000, 'Perfect for couples. Room size: 45m2.', '2025-06-01', 'KS03'),
('P009', 'Beachfront Villa', 2, 3000000, 'Private villa by the beach. Room size: 80m2.', '2025-06-01', 'KS03'),

-- KS04: Ocean Serenity
('P010', 'Ocean View', 1, 1600000, 'Room with panoramic ocean view. Room size: 38m2.', '2025-06-01', 'KS04'),
('P011', 'Premium Suite', 2, 2500000, 'Elegant suite with sea view. Room size: 55m2.', '2025-06-01', 'KS04'),
('P012', 'Serenity Room', 1, 1300000, 'Quiet and cozy room. Room size: 32m2.', '2025-06-01', 'KS04'),

-- KS05: Golden Orchid
('P013', 'City View', 1, 1100000, 'View of central district. Room size: 34m2.', '2025-06-01', 'KS05'),
('P014', 'Business Suite', 2, 1900000, 'Ideal for business trips. Room size: 50m2.', '2025-06-01', 'KS05'),
('P015', 'Penthouse', 2, 4000000, 'Top-floor luxury apartment. Room size: 90m2.', '2025-06-01', 'KS05'),

-- KS06: Crystal Grand
('P016', 'Classic Room', 1, 1050000, 'Traditional decor. Room size: 30m2.', '2025-06-01', 'KS06'),
('P017', 'Junior Suite', 2, 1750000, 'Comfort and convenience. Room size: 42m2.', '2025-06-01', 'KS06'),
('P018', 'Crystal Executive', 2, 2800000, 'High-class executive room. Room size: 60m2.', '2025-06-01', 'KS06');


-- Dữ liệu mẫu cho bảng HinhAnh
INSERT INTO HinhAnh VALUES
('IMG01', 'https://anviethouse.vn/wp-content/uploads/2021/12/Thiet-ke-phong-ngu-khach-san-sang-trong-2-2.jpg', 'P001'),
('IMG02', 'https://anviethouse.vn/wp-content/uploads/2022/01/thiet-ke-phong-khach-san-5-sao_2-giuong-1.jpg', 'P002'),
('IMG03', 'https://ik.imagekit.io/tvlk/generic-asset/dgXfoyh24ryQLRcGq00cIdKHRmotrWLNlvG-TxlcLxGkiDwaUSggleJNPRgIHCX6/hotel/asset/20012109-e835a504776df3d229ac83120e0cffda.jpeg?_src=imagekit&tr=dpr-2,c-at_max,f-jpg,h-460,pr-true,q-40,w-724', 'P003'),
('IMG04', 'https://www.hoteljob.vn/files/Anh-Hoteljob-Ni/Nam-2021/Thang-3/Cac-lo%E1%BA%A1i-phong-khach-san-02.jpg', 'P004'),
('IMG05', 'https://krass.vn/wp-content/uploads/2024/03/mau-giuong-don-khach-san-5-sao-dep.jpg', 'P005'),
('IMG06', 'https://noithatminhkhoi.com/upload/images/tieu-chuan-giuong-ngu-dep-cho-khach-san-5-sao.jpg', 'P006'),
('IMG07', 'https://img.homedy.com/store/images/2020/04/16/phong-ngu-khach-san-5-sao-9-637226036786137900.jpg', 'P007'),
('IMG08', 'https://saomaihotel.com.vn/wp-content/uploads/2024/02/cca54162cd9560cb3984.jpg', 'P008'),
('IMG09', 'https://ik.imagekit.io/tvlk/generic-asset/dgXfoyh24ryQLRcGq00cIdKHRmotrWLNlvG-TxlcLxGkiDwaUSggleJNPRgIHCX6/hotel/asset/10019241-1600x1200-FIT_AND_TRIM-0bb1a9dbb2930b930cc2fe125d7ffac3.jpeg?_src=imagekit&tr=dpr-2,c-at_max,f-jpg,h-460,pr-true,q-40,w-724', 'P009'),
('IMG10', 'https://dyf.vn/wp-content/uploads/2021/11/noi-that-khach-san-5-sao-19.jpg', 'P010'),
('IMG11', 'https://krass.vn/wp-content/uploads/2024/03/mau-giuong-don-khach-san-5-sao-dep.jpg', 'P011'),
('IMG12', 'https://sayhi.vn/wp-content/uploads/2019/01/2190907_17080416040054901823-min.jpg', 'P012'),
('IMG13', 'https://d2e5ushqwiltxm.cloudfront.net/wp-content/uploads/sites/86/2018/12/18031433/deluxe-king-bed-room-cottage-at-pullman-danang-beach-resort-vietnam-5-star-hotel.jpg', 'P013'),
('IMG14', 'https://acihome.vn/uploads/15/mau-thiet-ke-noi-that-phong-2-giuong-don-ben-trong-khach-san-3-4-5-sao-4.jpg', 'P014'),
('IMG15', 'https://saomaihotel.com.vn/wp-content/uploads/2024/02/885b8bfa000dad53f41c.jpg', 'P015'),
('IMG16', 'https://img.homedy.com/store/images/2020/04/16/phong-ngu-khach-san-5-sao-1-637226034544698696.jpg', 'P016'),
('IMG17', 'https://ik.imagekit.io/tvlk/blog/2025/03/cac-loai-phong-khach-san-5-sao-01.jpg?tr=q-70,c-at_max,w-500,h-300,dpr-2', 'P017'),
('IMG18', 'https://canaryhanoihotel.vn/wp-content/uploads/2019/06/aPX_03411.jpg', 'P018');

-- Dữ liệu mẫu cho bảng NguoiDung
INSERT INTO NguoiDung VALUES
-- Admin
('U001', 'Admin One', 'admin1@gmail.com', 'pass123', '0901234567', 'admin', '2025-05-01'),
('U002', 'Admin Two', 'admin2@gmail.com', 'pass123', '0902345678', 'admin', '2025-05-02'),
('U003', 'Admin Three', 'admin3@gmail.com', 'pass123', '0903456789', 'admin', '2025-05-03'),
-- Khách hàng
('U004', 'John Doe', 'john@gmail.com', 'pass123', '0911111111', 'user', '2025-06-01'),
('U005', 'Jane Smith', 'jane@gmail.com', 'pass123', '0922222222', 'user', '2025-06-02'),
('U006', 'Alice Nguyen', 'alice@gmail.com', 'pass123', '0933333333', 'user', '2025-06-03'),
('U007', 'Bob Tran', 'bob@gmail.com', 'pass123', '0944444444', 'user', '2025-06-04'),
('U008', 'Chris Lee', 'chris@gmail.com', 'pass123', '0955555555', 'user', '2025-06-05');

-- Dữ liệu mẫu cho bảng DonDatPhong
INSERT INTO DonDatPhong VALUES
('DP001', '2025-06-09', '2025-06-11', 360000, 'Da dat', '2025-06-01', 'U001', 'P001'),
('DP002', '2025-06-10', '2025-06-12', 300000, 'Da dat', '2025-06-02', 'U002', 'P004'),
('DP003', '2025-06-11', '2025-06-13', 420000, 'Da dat', '2025-06-03', 'U003', 'P007'),
('DP004', '2025-06-12', '2025-06-14', 750000, 'Cho xac nhan', '2025-06-04', 'U004', 'P011'),
('DP005', '2025-06-13', '2025-06-15', 525000, 'Cho xac nhan', '2025-06-05', 'U005', 'P017');


-- Chọn tất cả dữ liệu từ bảng DiaDiem
SELECT * FROM DiaDiem;

-- Chọn tất cả dữ liệu từ bảng QuanHuyen
SELECT * FROM QuanHuyen;

-- Chọn tất cả dữ liệu từ bảng KhachSan
SELECT * FROM KhachSan;

-- Chọn tất cả dữ liệu từ bảng LoaiPhong
SELECT * FROM LoaiPhong;

-- Chọn tất cả dữ liệu từ bảng HinhAnh
SELECT * FROM HinhAnh;

-- Chọn tất cả dữ liệu từ bảng NguoiDung
SELECT * FROM NguoiDung;

-- Chọn tất cả dữ liệu từ bảng DonDatPhong
SELECT * FROM DonDatPhong;