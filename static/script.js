let domen = "https://quizgame05.serveo.net";
let arrAnswer = []
let temp = ""
// опрашивание новых вопросов (новых вопросов не будет пока все пользователи не оветят на вопрос)
setInterval(async () => {
    try {
        console.log("опрос")
        const response = await fetch(domen + '/question'); // Замените на URL вашего API
        const data = await response.json();
        console.log(data)

        if (data.question && temp != data.answer) {
            document.querySelector('h3').innerText = data.question;
            data.incorrect.push(data.answer);
            shuffleArray(data.incorrect);
            console.log(arrAnswer)
            document.getElementById("one").innerText = data.incorrect[0];
            document.getElementById("one").style.backgroundColor = 'green';
            document.getElementById("two").innerText = data.incorrect[1];
            document.getElementById("two").style.backgroundColor = 'green';
            document.getElementById("three").innerText = data.incorrect[2];
            document.getElementById("three").style.backgroundColor = 'green';
            
            changeStatusDisableButton(false, document.querySelectorAll('.answer-btn'))

            console.log(data.question)
            temp = data.answer
        }
    } catch (error) {
        console.error('Ошибка при получении данных:', error);
    }
}, 2000);

// обработка нажатия ответа
document.addEventListener('DOMContentLoaded', function() {
    // Получаем все кнопки с классом answer-btn
    const buttons = document.querySelectorAll('.answer-btn');
    
    // Добавляем обработчик для каждой кнопки
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const answer = this.innerText;
            console.log(`Выбрано: ${answer}`);
            changeStatusDisableButton(true, buttons);
            if (answer == temp) {
                this.style.backgroundColor = 'blue';
            } 
            else {
                this.style.backgroundColor = 'red';
            }
            // Отправляем GET-запрос на сервер
            fetch(domen + `/check-answer/${encodeURIComponent(answer)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Ошибка сети');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Ответ сервера:', data);
                    console.log(data.status)
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                    alert('Произошла ошибка при отправке ответа');
                });
        });
    });
});

function changeStatusDisableButton(flag, buttons) {
    buttons.forEach(but => {
        but.disabled = flag
    }

    )
}

function shuffleArray(array) {
    for (var i = array.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}