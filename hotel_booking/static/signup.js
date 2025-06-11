document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('registerForm');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const fullname = document.getElementById('fullname').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();
        const repassword = document.getElementById('repassword').value.trim();
        const phone = document.getElementById('phone').value.trim();
        const message = document.getElementById('message');

        const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/;

        if (!passwordPattern.test(password)) {
            message.textContent = "Mật khẩu phải có ít nhất 6 ký tự, bao gồm chữ và số";
            return;
        }

        if (!fullname || !email || !password || !repassword || !phone) {
            message.textContent = "Vui lòng điền đầy đủ thông tin";
            return;
        }

        if (password !== repassword) {
            message.textContent = "Mật khẩu và xác nhận mật khẩu không khớp";
            return;
        }

        form.submit(); // Hợp lệ, gửi form
    });
});
