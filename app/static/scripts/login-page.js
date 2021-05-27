document.addEventListener('DOMContentLoaded', function () {
    let loginButton = document.getElementById('login-form');
    let userLoginInput = document.getElementById('user-login-input');
    let userPasswordInput = document.getElementById('user-password-input');
    loginButton.addEventListener('submit', function (e) {
        e.preventDefault();

        var r = new XMLHttpRequest();
        r.open('POST', '/api/login', true);
        r.setRequestHeader('Content-Type', 'application/json');
        r.onreadystatechange = function () {
            if (r.readyState != 4 || (r.status != 200 && r.status != 204))
                return;
            window.location.href = '/users';
            window.location.reload();
        };
    
        r.send(JSON.stringify({
            login: userLoginInput.value,
            password: userPasswordInput.value
        }));
    })
});
