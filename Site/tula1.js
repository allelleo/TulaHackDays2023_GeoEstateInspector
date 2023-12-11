document.addEventListener('DOMContentLoaded', function() {
    
    pole1 = document.getElementById('pole_1');
token_1 = localStorage.getItem('token');
url_1 = 'https://a904-77-238-135-243.ngrok-free.app/api/v1/user/history?token=' + token_1;

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
        text_1.textContent = data[i].id;

        br1 = document.createElement('br');

        file_in = document.createElement('a');
        file_in.href = 'https://a904-77-238-135-243.ngrok-free.app' + data[i].input_photo;
        file_in.download =  'https://a904-77-238-135-243.ngrok-free.app' +data[i].input_photo;
        file_in.textContent = "Input File №" + data[i].id;

        br2 = document.createElement('br');

        file_out = document.createElement('a');
        file_out.href = 'https://a904-77-238-135-243.ngrok-free.app/' + data[i].output_photo;
        file_out.download = 'https://a904-77-238-135-243.ngrok-free.app/' + data[i].output_photo;
        file_out.textContent = "Output File №" + data[i].id;

        br3 = document.createElement('br');

        time_1 = document.createElement('div');
        time_1.textContent = data[i].time_created;
        div_1 = document.createElement('div');
        pole1.appendChild(text_1);
        pole1.appendChild(br1);
        pole1.appendChild(file_in);
        pole1.appendChild(br2);
        pole1.appendChild(file_out);
        pole1.appendChild(br3);
        pole1.appendChild(time_1);


            // добавляем на страницу
        }
    }
})