from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from datetime import datetime, date
from django.conf import settings
from django.utils import timezone
from django.db.models import Q, Prefetch
from django.core.paginator import Paginator

from .models import Loaiphong, Quanhuyen, Khachsan, Diadiem, Dondatphong, Hinhanh
from .forms import RoomFilterForm
from accounts.models import Nguoidung


def home(request):
    return redirect('rooms:room_list',)


def room_list(request):
    search_query = request.GET.get('q', '')

    rooms = Loaiphong.objects.select_related(
        'khachsankhachsan__quanhuyenquanhuyen__diadiemdiadiem'
    ).prefetch_related(
        Prefetch('hinhanh_set', queryset=Hinhanh.objects.all(), to_attr='images')
    )

    if search_query:
        rooms = rooms.filter(
            Q(khachsankhachsan__quanhuyenquanhuyen__tenquanhuyen__icontains=search_query) |
            Q(khachsankhachsan__quanhuyenquanhuyen__diadiemdiadiem__tendiadiem__icontains=search_query)
        )

    form = RoomFilterForm(request.GET or None)
    if form.is_valid():
        price_range = form.cleaned_data['price_range']
        if price_range:
            if price_range == 'under_1000000':
                rooms = rooms.filter(gia__lt=1000000)
            elif price_range == '1000000_2000000':
                rooms = rooms.filter(gia__range=(1000000, 2000000))
            elif price_range == '2000000_3000000':
                rooms = rooms.filter(gia__range=(2000000, 3000000))
            elif price_range == 'over_3000000':
                rooms = rooms.filter(gia__gt=3000000)

        sort_by = form.cleaned_data['sort_by']
        if sort_by:
            if sort_by == 'price_low_high':
                rooms = rooms.order_by('gia')
            elif sort_by == 'price_high_low':
                rooms = rooms.order_by('-gia')

        beds = form.cleaned_data['beds']
        if beds:
            if beds == '1':
                rooms = rooms.filter(sogiuong=1)
            elif beds == '2':
                rooms = rooms.filter(sogiuong=2)
            elif beds == '3+':
                rooms = rooms.filter(sogiuong__gte=3)

    # Đảm bảo thứ tự cố định nếu người dùng không chọn sort_by
    if not form.is_valid() or not form.cleaned_data.get('sort_by'):
        rooms = rooms.order_by('phong_id')

    paginator = Paginator(rooms, 5) # Số phòng 4
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    is_logged_in = request.session.get('is_logged_in', False)
    tennguoidung = request.session.get('tennguoidung', '')

    context = {
        'form': form,
        'rooms': page_obj.object_list,  # Chỉ 4 phòng mỗi trang
        'room_count': paginator.count,
        'page_obj': page_obj,           # Dùng để hiển thị phân trang
        'is_logged_in': is_logged_in,
        'tennguoidung': tennguoidung,
        'search_query': search_query,
    }
    return render(request, 'room_list.html', context)


def room_detail(request, room_id):
    if 'is_logged_in' not in request.session:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    
    room = get_object_or_404(
        Loaiphong.objects.prefetch_related(
            Prefetch('hinhanh_set', queryset=Hinhanh.objects.all(), to_attr='images')
        ),
        phong_id=room_id
    )
    
    hotel = room.khachsankhachsan
    user = get_object_or_404(Nguoidung, nguoidung_id=request.session['nguoidung_id'])
    
    default_checkin = date.today()
    default_checkout = default_checkin + timezone.timedelta(days=1)
    nights = 1
    room_rate = room.gia * nights
    total = room_rate * 0.3
    
    context = {
        'room': room,
        'hotel': hotel,
        'user': user,
        'checkin_date': default_checkin,
        'checkout_date': default_checkout,
        'room_rate': room_rate,
        'total': total,
        'nights': nights,
    }
    return render(request, 'room_detail.html', context)

def display_about(request):
    return render(request, "footer/about_us.html")

def display_contact(request):
    return render(request, "footer/contact.html")

def display_services(request):
    return render(request, "footer/services.html")