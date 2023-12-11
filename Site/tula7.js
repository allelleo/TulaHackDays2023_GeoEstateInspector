document.addEventListener('DOMContentLoaded', function() {
    fileForm = document.getElementById("file_");
    divFiles = document.getElementById("div_files");

    token_7 = localStorage.getItem('token');
    fileForm.addEventListener('submit', function (e) {
    e.preventDefault(); // Предотвращаем стандартное поведение формы (перезагрузку страницы)
    url_7 = 'https://a904-77-238-135-243.ngrok-free.app/api/v1/ml/new?token=' + token_7;
    // Получаем файл из элемента input
    //var fileInput = document.getElementById('file_input_');
    var fileInput = document.querySelector('input[name="file"]');
    var file = fileInput.files[0];
    // Создаем объект FormData и добавляем в него файл
    var formData = new FormData();
    formData.append('file', file);

    // Отправляем файл на сервер с использованием AJAX
    fetch(url_7, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        // Обработка ответа от сервера
        console.log(data);
        br1_1 = document.createElement('br');
        file_in_1 = document.createElement('a');
        file_in_1.href = 'https://a904-77-238-135-243.ngrok-free.app' + data.photo;
        file_in_1.download =  'https://a904-77-238-135-243.ngrok-free.app' +data.photo;
        file_in_1.textContent = "Output File";
        divFiles.appendChild(br1_1);
        divFiles.appendChild(file_in_1);
        
    })
    .catch(error => {
        console.error('Ошибка при отправке файла:', error);
    });
});
})