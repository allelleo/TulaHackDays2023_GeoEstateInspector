document.addEventListener('DOMContentLoaded', function() {
    
    pole2 = document.getElementById('pole2');
token_1 = localStorage.getItem('token');
url_1 = 'https://a904-77-238-135-243.ngrok-free.app/api/v1/user/feedbacks?token=' + token_1;

fetch(url_1, {
    method: 'POST',
    headers: {

    }
})
.then(response => response.json())
.then(data => {
    // Обработка данных
    processData(data);
})
.catch(error => {
    console.error('Ошибка при вызове API:', error);
});

// Обработка данных
function processData(data) {
    // Проходимся по массиву данных
    for (let i = 0; i < data.length; i++) {
        // Создаем HTML-элементы в зависимости от типа данных
        console.log(data[i]);
        text_1 = document.createElement('div');
        text_1.textContent = JSON.stringify(data[i]);

        br1 = document.createElement('br');
        
        pole2.appendChild(text_1);
        pole2.appendChild(br1);



            // добавляем на страницу
        }
    }
})