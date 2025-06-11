from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime, date, timedelta
import uuid
from accounts import models
from rooms.models import Loaiphong, Quanhuyen, Khachsan, Diadiem, Dondatphong
from accounts.models import Nguoidung
from .models import Dondatphong

def payment(request, room_id):
    if 'is_logged_in' not in request.session:
        return redirect('accounts:login')

    room = get_object_or_404(Loaiphong, phong_id=room_id)
    hotel = room.khachsankhachsan
    user = get_object_or_404(Nguoidung, nguoidung_id=request.session['nguoidung_id'])

    # Giá mặc định khi lần đầu load trang
    default_checkin = date.today()
    default_checkout = default_checkin + timedelta(days=1)
    nights_default = (default_checkout - default_checkin).days
    price = int(room.gia * nights_default)
    total_default = int(price * 0.3)

    booking_data = {
        'checkin_date': default_checkin,
        'checkout_date': default_checkout,
        'nights': nights_default,
        'price': price,
        'total': total_default,
    }

    context = {
        'room': room,
        'hotel': hotel,
        'nguoidung': user,
        'booking_data': booking_data
    }

    if request.method == 'POST':
        checkin_str = request.POST.get('checkin_date')
        checkout_str = request.POST.get('checkout_date')

        try:
            checkin = datetime.strptime(checkin_str, '%Y-%m-%d').date()
            checkout = datetime.strptime(checkout_str, '%Y-%m-%d').date()

            if checkin < date.today():
                messages.error(request, 'Ngày check-in không được nhỏ hơn ngày hiện tại.')
            elif checkout <= checkin:
                messages.error(request, 'Ngày check-out phải lớn hơn ngày check-in.')
            else:
                trungs = Dondatphong.objects.filter(
                    phongphong=room,
                    ngaydat__lt=checkout,
                    ngaytra__gt=checkin,
                    trangthai__in=['PENDING', 'CONFIRMED']
                )
                if trungs.exists():
                    messages.error(request, 'Phòng đã được đặt trong thời gian này.')
                else:
                    nights = (checkout - checkin).days
                    price = int(room.gia * nights)
                    total = int(price*0.3)

                    booking_data = {
                        'checkin_date': checkin,
                        'checkout_date': checkout,
                        'nights': nights,
                        'price': price,
                        'total': total
                    }
                    context['booking_data'] = booking_data

        except ValueError:
            messages.error(request, 'Định dạng ngày không hợp lệ. Vui lòng chọn lại.')
        except Exception as e:
            messages.error(request, f'Đã xảy ra lỗi: {e}')

    return render(request, 'payment.html', context)

def confirm_booking(request):
    if 'is_logged_in' not in request.session:
        return redirect('accounts:login')
        
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        checkin_date = request.POST.get('checkin_date')  # yyyy-mm-dd
        checkout_date = request.POST.get('checkout_date')  # yyyy-mm-dd
        total = float(request.POST.get('total'))
        
        # Lấy user từ session
        nguoidung_id = request.session.get('nguoidung_id')
        user = get_object_or_404(Nguoidung, nguoidung_id=nguoidung_id)

        try:
            phong = Loaiphong.objects.get(phong_id=room_id)
        except Loaiphong.DoesNotExist:
            messages.error(request, "Phòng không tồn tại")
            return redirect('bookings:payment', room_id=room_id)

        # Sinh giá trị lichsu_id duy nhất bằng uuid (chỉ lấy 20 ký tự)
        lichsu_id = str(uuid.uuid4()).replace('-', '').upper()[:20]

        # Chuyển đổi string thành date
        try:
            checkin_date = datetime.strptime(checkin_date, '%Y-%m-%d').date()
            checkout_date = datetime.strptime(checkout_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Định dạng ngày không hợp lệ")
            return redirect('bookings:payment', room_id=room_id)

        # Tạo đơn đặt phòng
        try:
            Dondatphong.objects.create(
                lichsu_id=lichsu_id,
                ngaydat=checkin_date,
                ngaytra=checkout_date,
                tongtien=total,
                trangthai='Đã thanh toán',
                thoigiandat=date.today(),
                nguoidung=user,
                phongphong=phong
            )
            return redirect('bookings:booking_history')
        except Exception as e:
            messages.error(request, f'Lỗi khi lưu đơn đặt phòng: {e}')
            return redirect('bookings:payment', room_id=room_id)

    return redirect('/')

def booking_history(request):
    if not request.session.get('is_logged_in'):
        return redirect(f'/accounts/login/?next={request.path}')
    
    # Lấy user theo id trong session
    nguoidung_id = request.session.get('nguoidung_id')
    user = get_object_or_404(Nguoidung, nguoidung_id=nguoidung_id)
    
    # Lấy các đơn đặt phòng của user
    bookings = Dondatphong.objects.filter(nguoidung=user).order_by('-ngaydat')
    
    return render(request, 'booking_history.html', {
        'bookings': bookings
    })