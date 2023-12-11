document.addEventListener('DOMContentLoaded', function() {
    
    var name_0_4 = document.getElementById("name0_4");
    var name_1_4 = document.getElementById("name1_4");
    var name_2_4 = document.getElementById("name2_4");
    var emai_1_4 = document.getElementById("email1_4");
    var is_admin_4 = document.getElementById("admin_4");
    var create_4 = document.getElementById('create');

    token_4 = localStorage.getItem("token");
    url_4 = "https://a904-77-238-135-243.ngrok-free.app/api/v1/user/me?token=" + token_4;

        fetch(url_4, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',  
 //СУКА КУДА ЭТОТ ЕБУЧИЙ ТОКЕН 

            },
          })
          .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            return response.json(); // Заменяем на response.text()
        })
        .then(data => {
                
            userID = data.id;
            name0_4 = data.username;
            name1_4 = data.first_name;
            name2_4 = data.last_name;
            email_4 = data.email;
            isAdmin = data.is_admin;
            console.log(data.username);
            name_0_4.value = name0_4;
            name_1_4.value = name1_4;
            name_2_4.value = name2_4;
            emai_1_4.value = email_4;
            if (is_admin_4)
            {
                is_admin_4.value = "Админ";
                create_4.style.visibility = 'visible';

            } else
            {
                is_admin_4.value = "Не админ";
            }
        })
        .catch(error => {
            // Обработка ошибки
            console.error('Validation Error:', error);
            console.log(token_4);

        });
});