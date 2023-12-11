document.addEventListener('DOMContentLoaded', function() {
    
    var messageForm = document.getElementById('message_form_1');

    messageForm.addEventListener('submit', function(event) {
        event.preventDefault();
        message_6__ = document.getElementById('message_6_').value;
        message_6_ = document.getElementById('message_6').value;




        // Отправляем запрос на сервер FastAPI
        fetch('https://a904-77-238-135-243.ngrok-free.app/api/v1/user/feedback/anonumys', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
            },
            body: JSON.stringify({
                email: message_6__,
                message: message_6_,
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