document.addEventListener('DOMContentLoaded', function() {
    
    var authForm = document.querySelector('.login-form');

    authForm.addEventListener('submit', function(event) {
        event.preventDefault();

        // Получаем данные из формы
        email = document.getElementById('username').value;
        password = document.getElementById('password').value;
        let test = {
            email: email,
            password: password,
        }
        console.log(JSON.stringify(test));

        // Отправляем запрос на сервер FastAPI
        fetch('https://a904-77-238-135-243.ngrok-free.app/api/v1/auth/sign-in', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
            },
            body: JSON.stringify({
                email: email,
                password: password,
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Обработка успешного ответа
            console.log('Successful Response:', data);
            localStorage.setItem('token', data.token);
            window.location.replace('tula2.html');
        })
        .catch(error => {
            // Обработка ошибки
            console.error('Validation Error:', error);
        });
    });

    var registerForm = document.querySelector('.register-form');

    registerForm.addEventListener('submit', function(event) {
        event.preventDefault();

        // Получаем данные из формы
        name0 = document.getElementById('name0').value;
        name1 = document.getElementById('name1').value;
        name2 = document.getElementById('name2').value;
        email1 = document.getElementById('email1').value;
        password1 = document.getElementById('password1').value;



        // Отправляем запрос на сервер FastAPI
        fetch('https://a904-77-238-135-243.ngrok-free.app/api/v1/auth/sign-up', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
            },
            body: JSON.stringify({
                username: name0,
                first_name: name1,
                last_name: name2,
                email: email1,
                password: password1,
              
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Обработка успешного ответа
            console.log('Successful Response:', data);
            location.reload();
        })
        .catch(error => {
            // Обработка ошибки
            console.error('Validation Error:', error);
        });
    });

    
});