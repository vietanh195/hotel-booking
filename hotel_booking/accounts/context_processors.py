def auth_info(request):
    return {
        'is_logged_in': request.session.get('is_logged_in', False),
        'tennguoidung': request.session.get('tennguoidung', ''),
    }
