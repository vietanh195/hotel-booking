from django.shortcuts import render
from .models import Loaiphong, Dondatphong
from .forms import RoomFilterForm

def room_list(request):
    rooms = Loaiphong.objects.all()
    form = RoomFilterForm(request.GET or None)

    if (request.method == "POST") and (request.POST.get("locate")!="") :
        locate = request.POST.get("locate")
        both_locate = [x.strip() for x in locate.split(',')]
        rooms = rooms.filter(khachsankhachsan__quanhuyenquanhuyen__diadiemdiadiem__tendiadiem= both_locate[0])
        if len(both_locate) > 1:
            rooms = rooms.filter(khachsankhachsan__quanhuyenquanhuyen__tenquanhuyen= both_locate[1])

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
            # 'popular' could be implemented with a popularity metric if available
        
        beds = form.cleaned_data['beds']
        if beds:
            if beds == '1':
                rooms = rooms.filter(sogiuong='1')
            elif beds == '2':
                rooms = rooms.filter(sogiuong='2')
            elif beds == '3+':
                rooms = rooms.filter(sogiuong='3')

    context = {
        'form': form,
        'rooms': rooms,
        'room_count': rooms.count(),
    }
    return render(request, 'room_list.html', context)

def booking_history(request):
    book_hist = Dondatphong.objects.filter(nguoidungnguoidung="ND001")
    return render(request, "booking_history.html", {"bookings": book_hist})