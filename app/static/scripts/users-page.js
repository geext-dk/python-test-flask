document.addEventListener('DOMContentLoaded', function () {
    let logoutButton = document.getElementById('logout-button');
    logoutButton.addEventListener('click', function () {
        var r = new XMLHttpRequest();
        r.open('POST', '/api/logout', true);
        r.setRequestHeader('Content-Type', 'application/json');
        r.onreadystatechange = function () {
            if (r.readyState != 4 || (r.status != 200 && r.status != 204))
                return;
            window.location.href = "/login";
            window.location.reload();
        };
    
        r.send();
    });

    let viewRows = document.querySelectorAll('.users-table .view-row');
    let editRows = document.querySelectorAll('.users-table .edit-row');

    let pairedRows = Array.from(viewRows).map((r, i) => [r, editRows[i]]);
    for (let rowsPair of pairedRows) {
        let editUserButton = rowsPair[0].querySelector('.edit-user-cell button');
        editUserButton.addEventListener('click', function () {
            for (let pair of pairedRows) {
                pair[0].style.display = '';
                pair[1].style.display = 'none';
            }

            rowsPair[0].style.display = 'none';
            rowsPair[1].style.display = '';

            let userId = rowsPair[0].querySelector('.user-id').innerHTML;
            let newLoginInput = rowsPair[1].querySelector('.user-login input');
            let newPasswordInput = rowsPair[1].querySelector('.user-password input');
            let newRoleSelect = rowsPair[1].querySelector('.user-role select');

            let saveButton = rowsPair[1].querySelector('.save-edited-user-cell button');
            saveButton.addEventListener('click', function () {
                var r = new XMLHttpRequest();
                r.open("PUT", "/api/users/" + userId, true);
                r.setRequestHeader('Content-Type', 'application/json');
                r.onreadystatechange = function () {
                    if (r.readyState != 4 || (r.status != 200 && r.status != 204))
                        return;
                    window.location.reload();
                };
            
                r.send(JSON.stringify({
                    login: newLoginInput.value,
                    password: newPasswordInput.value,
                    role: newRoleSelect.value
                }));
            });
        })
    }

    let createUserForm = document.getElementById('create-user-form');
    createUserForm.addEventListener('submit', function (e) {
        e.preventDefault();

        let userLoginInput = createUserForm.querySelector('#create-user-login');
        let userPasswordInput = createUserForm.querySelector('#create-user-password');
        let userRoleSelect = createUserForm.querySelector('#create-user-role');

        var r = new XMLHttpRequest();
        r.open("POST", "/api/users", true);
        r.setRequestHeader('Content-Type', 'application/json');
        r.onreadystatechange = function () {
            if (r.readyState != 4 || (r.status != 200 && r.status != 204))
                return;
            location.reload();
        };

        r.send(JSON.stringify({
            login: userLoginInput.value,
            password: userPasswordInput.value,
            role: userRoleSelect.value
        }));
    });

    let deleteUserForms = document.getElementsByClassName('delete-user-form');
    for (var deleteUserForm of deleteUserForms) {
        let userIdInput = deleteUserForm.getElementsByClassName('user-id-input')[0]

        deleteUserForm.addEventListener('submit', function (e) {
            e.preventDefault();

            let userId = userIdInput.value;

            var r = new XMLHttpRequest();
            r.open("DELETE", "/api/users/" + userId, true);
            r.onreadystatechange = function () {
                if (r.readyState != 4 || (r.status != 200 && r.status != 204))
                    return;
                window.location.reload();
            };
            r.send();
        });
    }
});
