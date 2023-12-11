document.addEventListener('DOMContentLoaded', function() {
    
    var messageForm = document.getElementById('message_form');
    token_5 = localStorage.getItem('token');

    messageForm.addEventListener('submit', function(event) {
        event.preventDefault();
        message_5_ = document.getElementById('message_5').value;

        // Получаем данные из формы
        let test = {
            message: message_5_,
            token: token_5,
        }
        console.log(JSON.stringify(test));

        // Отправляем запрос на сервер FastAPI
        fetch('https://a904-77-238-135-243.ngrok-free.app/api/v1/user/feedback/auth', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
            },
            body: JSON.stringify({
                token: token_5,
                message: message_5_,
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
        })
        .catch(error => {
            // Обработка ошибки
            console.error('Validation Error:', error);
        });
    });
})