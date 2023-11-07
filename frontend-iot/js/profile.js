// ui logic
const togglePassword = document.querySelectorAll('.togglePassword');
const password = document.querySelectorAll('.password');

togglePassword.forEach((btn, index) => {
    btn.addEventListener('click', () => {
        if (password[index].type === 'password') {
            password[index].type = 'text';
            btn.classList.remove('fa-eye');
            btn.classList.add('fa-eye-slash');
        } else {
            password[index].type = 'password';
            btn.classList.remove('fa-eye-slash');
            btn.classList.add('fa-eye');
        }
    });
});

// call api logic
callAPI('api/authen/me', 'GET', null, function () {
    if (this.readyState === 4) {
        data = JSON.parse(this.responseText);
        if (this.status == 200) {
            document.querySelector('.username-title').innerText = data['username'];
            document.querySelector('.username-description').innerText = data['username'];
            document.querySelector('.email').innerText = data['email'];
            document.querySelector('.phone').innerText = formatPhoneNumber(data['phone']);

            const isAdmin = data['isAdmin'];
            if (isAdmin) {
                document.querySelector('.role').innerText = 'Admin';
                document.querySelector('.avatar-img').src = '/assets/img/admin_avatar.jpg';
            } else {
                document.querySelector('.role').innerText = 'Sinh viên Học Viện Công Nghệ Bưu Chính Viễn Thông';
            }
        }
        else if (this.status == 401) {
            unauthorizedPage();
        }
    }
});

function formatPhoneNumber(phone) {
    return phone.replace(/(\d{3})(\d{3})(\d{4})/, '$1 $2 $3');
}

document.querySelector('#btn-change-pasword').onclick = () => {
    const currentPassword = document.querySelector('#current-password').value;
    const newPassword = document.querySelector('#new-password').value;
    const confirmPassword = document.querySelector('#confirm-password').value;

    const data = JSON.stringify({
        "currentPassword": currentPassword,
        "newPassword": newPassword,
        "confirmPassword": confirmPassword,
    });

    callAPI('api/authen/change-password', 'POST', data, function () {
        if (this.readyState === 4) {
            response = JSON.parse(this.responseText);
            if (this.status == 201) {
                alert(response['message']);
            }
            else if (this.status == 400) {
                alert(response['message']);
            }
            else if (this.status == 401) {
                unauthorizedPage();
            }
        }
    });
}
