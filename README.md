# hotel-booking
A. SQL Server:
Cấu hình SQL Server:
1. Ánh xạ tài khoản đến database Hotel_Booking:
!!! Nếu dùng Windows Authentication để kết nối vào SSMS:
Mở Security → Logins → Chọn tài khoản: ten_may_chu\Admin → User Mapping → tích vào file sql của dự án → tích db ower

!!! Nếu dùng tài khoản user/password để kết nối vào SSMS: chọn tài khoản đã đăn nhập trong logins và thiết lập User Mapping như trên.
 
2. Mở TCP/IP để Django giao tiếp với SQL Server:
	Vào SQL Server Configuration Manager → SQL Server Services → đảm bảo SQL Server đang chạy (running) và SQL Server Browser đang chạy
 
	Vào SQL Server Network Configuration → kích đúp Protocols for A (A: instance đang dùng) → bật TCP/IP và Named Pipes thành Enabled
 
⚠ Nếu không mở được SQL Server Browser sang trạng thái running thì dùng cách sau: 
 
B. Django
Bước 1: Khởi tạo và kích hoạt môi trường:
	+)  python -m venv .venv
	+) Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
	   venv\Scripts\activate
Bước 2: Tải các gói cần thiết:
	+) pip install Django
	+) pip install mssql-django 
	+) pip install pyodbc
	+) Đảm bảo đã cài Microsoft ODBC Driver for SQL Server trên máy tính (kiểm tra 	trong programs and features)
	(Hoặc mở cmd gõ ODBC Data Source vào tap Drives ktra xem có ODBC Driver 		17…)
Bước 3: Cấu hình settings.py
	DATABASE = {
		‘default’ : {
			‘ENGINE’ : ‘mssql’,
			‘NAME’ : ‘ten_database’, // database có sẵn trong SQL Server
			‘USER’ : ‘  ’, // Nếu dùng SQL Server Authentication, ko cần nếu 						dùng WINDOWS AUTHENTICATION
			‘PASSWORD’ : ‘  ’, // Nếu dùng SQL Server Authentication, ko cần 						nếu dùng WINDOWS AUTHENTICATION

			‘HOST’ : ‘ten_may_chu’, // Có thể để localhost
			‘PORT’ : ‘  ’, // Để trống hoặc dùng cổng mặc định 1433
			‘OPTIONS’ : {
				‘driver’ : ‘ODBC Driver 17 for SQL Server’, 
				‘trusted_connection’ : ‘yes’, // khi sử dụng WINDOWS 									AUTHENTICATION
			}
		}
	} 
Bước 4: Dùng inspectdb tạo models.py:
	+) python manage.py inspectdb > rooms/models.py 
	+) python manage.py makemigrations
	+) python manage.py migrate
