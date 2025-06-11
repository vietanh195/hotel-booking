from django.db import IntegrityError
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
import uuid

from .models import Nguoidung
from rooms.models import Loaiphong, Quanhuyen, Khachsan, Diadiem, Dondatphong, Hinhanh

def signup_view(request):
    if request.method == 'POST':
        email = request.POST['email'].strip()
        password = request.POST['password']
        repassword = request.POST['repassword']
        fullname = request.POST['fullname'].strip()
        phone = request.POST['phone'].strip()

        if password != repassword:
            messages.error(request, 'Mật khẩu không khớp.')
            return render(request, 'accounts/signup.html')

        if Nguoidung.objects.filter(email=email).exists():
            messages.error(request, 'Email đã tồn tại.')
            return render(request, 'accounts/signup.html')

        nguoidung_id = str(uuid.uuid4())[:8].upper()
        nguoidung = Nguoidung(
            nguoidung_id=nguoidung_id,
            tennguoidung=fullname,
            email=email,
            matkhau=password,
            dienthoai=phone,
            vaitro='user',
            ngaytaotk=timezone.now().date()
        )
        nguoidung.save()
        messages.success(request, 'Tạo tài khoản thành công.')
        return redirect('accounts:login')

    return render(request, 'accounts/signup.html')


from django.http import JsonResponse

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
        next_url = request.POST.get('next')

        try:
            user = Nguoidung.objects.get(email=email, matkhau=password)

            # Lưu session
            request.session['nguoidung_id'] = user.nguoidung_id
            request.session['tennguoidung'] = user.tennguoidung
            request.session['vaitro'] = user.vaitro
            request.session['is_logged_in'] = True

            # Trả JSON thay vì redirect
            if user.vaitro.strip().lower() == 'admin':
                return JsonResponse({'redirect_url': reverse('accounts:admin_dashboard')})
            else:
                return JsonResponse({'redirect_url': next_url or reverse('rooms:room_list')})

        except Nguoidung.DoesNotExist:
            return JsonResponse({'error': 'Email hoặc mật khẩu không đúng.'}, status=400)

    # Nếu GET request, vẫn trả về trang login bình thường
    return render(request, 'accounts/login.html', {
        'next': request.GET.get('next', '')
    })


# xóa session khi đăng xuất.
def logout_view(request):
    if 'is_logged_in' in request.session:
        del request.session['nguoidung_id']
        del request.session['tennguoidung']
        del request.session['is_logged_in']
    return redirect('rooms:room_list')


def user_profile(request):
    if 'nguoidung_id' not in request.session:
        return redirect('accounts:login')  # hoặc redirect về trang nào đó

    user = get_object_or_404(Nguoidung, pk=request.session['nguoidung_id'])

    if request.method == 'POST':
        ten = request.POST.get('tennguoidung')
        sdt = request.POST.get('dienthoai')
        mk = request.POST.get('matkhau')

        user.tennguoidung = ten
        user.dienthoai = sdt
        user.matkhau = mk
        user.save()

        messages.success(request, 'Cập nhật thông tin thành công.')
        return redirect('accounts:user_profile')  # Không cần truyền ID

    return render(request, 'accounts/user_profile.html', {'user': user})

from django.apps import apps
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest


from django.apps import apps
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.forms import ModelForm
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

def admin_dashboard(request):
    # Model mapping
    model_map = {
        'diadiem': Diadiem,
        'quanhuyen': Quanhuyen,
        'khachsan': Khachsan,
        'loaiphong': Loaiphong,
        'dondatphong': Dondatphong,
        'hinhanh': Hinhanh,
        'nguoidung': Nguoidung,
    }

    # Kiểm tra quyền (dựa trên phương thức đăng nhập tự tạo)
    if 'nguoidung_id' not in request.session or request.session.get('vaitro') != 'admin':
        messages.error(request, "Bạn không có quyền truy cập. Vui lòng đăng nhập với tài khoản quản trị.")
        return redirect('accounts:login')

    # Lấy model_key và model_class
    model_key = request.GET.get('model', 'diadiem')
    model_class = model_map.get(model_key, Diadiem)

    # Danh sách khóa ngoại cho form
    context = {
        'diadiem_list': Diadiem.objects.all(),
        'quanhuyen_list': Quanhuyen.objects.all(),
        'khachsan_list': Khachsan.objects.all(),
        'loaiphong_list': Loaiphong.objects.all(),
        'nguoidung_list': Nguoidung.objects.all(),
    }

    # Định nghĩa DynamicForm sau khi model_class được xác định
    class DynamicForm(ModelForm):
        class Meta:
            model = model_class
            fields = [f.name for f in model_class._meta.fields if f.name != 'ngaytaotk' and not f.auto_created]

    # DELETE
    if request.method == 'POST' and 'delete' in request.POST:
        pk = request.POST.get('delete')
        try:
            obj = get_object_or_404(model_class, pk=pk)
            obj.delete()
            messages.success(request, "Xóa thành công.")
        except IntegrityError:
            messages.error(request, "Không thể xóa do bản ghi đang được sử dụng bởi dữ liệu khác.")
        except model_class.DoesNotExist:
            messages.error(request, "Bản ghi không tồn tại.")
        except Exception as e:
            messages.error(request, f"Lỗi khi xóa: {str(e)}")
        return redirect(reverse('accounts:admin_dashboard') + f'?model={model_key}')

    # ADD / UPDATE
    if request.method == 'POST' and 'delete' not in request.POST:
        pk = request.POST.get('pk')
        try:
            if pk:
                instance = get_object_or_404(model_class, pk=pk)
                form = DynamicForm(request.POST, instance=instance)
            else:
                form = DynamicForm(request.POST)

            if form.is_valid():
                instance = form.save(commit=False)
                # Xử lý mật khẩu cho Nguoidung
                if model_key == 'nguoidung' and 'matkhau' in form.cleaned_data:
                    from django.contrib.auth.hashers import make_password
                    instance.matkhau = make_password(form.cleaned_data['matkhau'])
                instance.save()
                messages.success(request, "Thêm/cập nhật thành công.")
                return redirect(reverse('accounts:admin_dashboard') + f'?model={model_key}')
            else:
                messages.error(request, f"Lỗi: {form.errors.as_text()}")
        except Exception as e:
            messages.error(request, f"Lỗi khi thêm/cập nhật: {str(e)}")
            form = DynamicForm(request.POST)  # Giữ form với dữ liệu đã nhập

        # Render lại trang khi có lỗi
        objects_list = model_class.objects.all()
        paginator = Paginator(objects_list, 10)
        page_number = request.GET.get('page')
        objects = paginator.get_page(page_number)
        fields = [f.name for f in model_class._meta.fields if not f.auto_created and f.name != 'ngaytaotk']

        return render(request, 'accounts/admin_dashboard.html', {
            'model_name': model_key,
            'fields': fields,
            'objects': objects,
            'models': model_map.keys(),
            'form': form,
            **context,
        })

    # DISPLAY
    objects_list = model_class.objects.all()
    paginator = Paginator(objects_list, 10)
    page_number = request.GET.get('page')
    objects = paginator.get_page(page_number)
    fields = [f.name for f in model_class._meta.fields if not f.auto_created and f.name != 'ngaytaotk']

    return render(request, 'accounts/admin_dashboard.html', {
        'model_name': model_key,
        'fields': fields,
        'objects': objects,
        'models': model_map.keys(),
        'form': DynamicForm(),
        **context,
    })