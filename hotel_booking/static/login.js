document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('loginForm');
    const message = document.createElement('p');
    message.id = "message";
    message.style.marginTop = "0.5rem";
    message.style.fontWeight = "bold";
    form.appendChild(message);

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const email = document.getElementById('loginEmail').value.trim();
        const password = document.getElementById('loginPassword').value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/;

        if (!emailRegex.test(email)) {
            message.style.color = "red";
            message.textContent = "Email không hợp lệ.";
            return;
        }

        if (!passwordRegex.test(password)) {
            message.style.color = "red";
            message.textContent = "Mật khẩu phải ít nhất 6 ký tự, có chữ và số.";
            return;
        }

        try {
            const formData = new FormData();
            formData.append('email', email);
            formData.append('password', password);
            formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);

            const response = await fetch(form.action, {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                window.location.href = data.redirect_url;
            } else {
                message.style.color = "red";
                message.textContent = data.error || "Lỗi khi đăng nhập.";
            }
        } catch (err) {
            message.style.color = "red";
            message.textContent = "Lỗi khi đăng nhập, thử lại sau.";
        }
    });
});
