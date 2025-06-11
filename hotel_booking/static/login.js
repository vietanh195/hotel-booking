document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('loginForm');
    if (!form) return;

    const message = document.createElement('p');
    message.id = "message";
    message.style.marginTop = "0.5rem";
    message.style.fontWeight = "bold";
    message.style.color = "red";
    form.appendChild(message);

    form.addEventListener('submit', function (e) {
        const email = document.getElementById('loginEmail').value.trim();
        const password = document.getElementById('loginPassword').value.trim();

        if (!email || !password) {
            e.preventDefault();  // ngăn gửi form nếu thiếu
            message.textContent = "Vui lòng nhập đầy đủ email và mật khẩu.";
        } else {
            message.textContent = "";  // xóa thông báo lỗi nếu hợp lệ
        }
    });
});
