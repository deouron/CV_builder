# CV_builder

Пример готового резюме: 
https://github.com/deouron/CV_builder/blob/main/cv.pdf

---

<img width="491" alt="Снимок экрана 2022-11-25 в 01 33 46" src="https://user-images.githubusercontent.com/70703745/203870700-adf52302-d232-47b8-adcd-891a03158c96.png">
<img width="1440" alt="Снимок экрана 2022-11-25 в 01 34 00" src="https://user-images.githubusercontent.com/70703745/203870710-a828b428-0fca-488a-a040-5587a0bd42fb.png">
---

Создайте сайт с помощью Flask или Django. Будем делать конструктор резюме!

Общая структура сайта:

1. Страничка с авторизацией и регистрацией

2. После авторизации, должна быть страница с формой, в которой необходимо заполнить форму (если пользователь уже заполнял форму, то в формы уже должен быть подгружен текст, который был заполнен, для этого должна быть отдельная кнопочка для сохранения в черновик)

3. Страница со скоинструированным резюме, который может быть превращен в PDF и выгружен (для этого можно использовать [pdfkit](https://pypi.org/project/pdfkit/))

На всякий случай: пользователь не может посмотреть чужие резюме
