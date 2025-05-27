from django.shortcuts import render
from .models import Loaiphong, Quanhuyen, Khachsan, Diadiem
from .forms import RoomFilterForm

def room_list(request):
    rooms = Loaiphong.objects.all()
    form = RoomFilterForm(request.GET or None)

    if form.is_valid():
        if form.cleaned_data['district']:
            rooms = rooms.filter(khachsankhachsan__quanhuyenquanhuyen__tenquanhuyen="Cau Giay")
        
        price_range = form.cleaned_data['price_range']
        if price_range:
            if price_range == 'under_1000000':
                rooms = rooms.filter(price_per_night__lt=1000000)
            elif price_range == '1000000_2000000':
                rooms = rooms.filter(price_per_night__range=(1000000, 2000000))
            elif price_range == '2000000_3000000':
                rooms = rooms.filter(price_per_night__range=(2000000, 3000000))
            elif price_range == 'over_3000000':
                rooms = rooms.filter(price_per_night__gt=3000000)
        
        sort_by = form.cleaned_data['sort_by']
        if sort_by:
            if sort_by == 'price_low_high':
                rooms = rooms.order_by('price_per_night')
            elif sort_by == 'price_high_low':
                rooms = rooms.order_by('-price_per_night')
            # 'popular' could be implemented with a popularity metric if available
        
        beds = form.cleaned_data['beds']
        if beds:
            if beds == '1':
                rooms = rooms.filter(bed_configuration__icontains='1')
            elif beds == '2':
                rooms = rooms.filter(bed_configuration__icontains='2')
            elif beds == '3+':
                rooms = rooms.filter(bed_configuration__icontains='3')

    context = {
        'form': form,
        'rooms': rooms,
        'room_count': rooms.count(),
    }
    return render(request, 'room_list.html', context)

# def room_list(request):
#     return render(request, 'room_list.html')