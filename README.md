# CRUD-python
Цель проекта - создать программный модуль, который будет обеспечивать автоматизацию процессов управления бригадами скорой помощи, модуль, который будет являться CRUD приложением
Предметом автоматизации является деятельность диспетчера скорой неотложной медицинской помощи.
В данной работе представлен программный модуль для автоматизации процессов управления бригадами скорой помощи, созданный в рамках курсового проекта. 
<br> Спецификации и функциональные системные требования к проектированию для системы управления вызовами и бригадами скорой помощи, предназначенной для использования диспетчерами скорой помощи.
<br> Система должна быть разработана на языке программирования Python с использованием библиотек Flask для создания веб-приложения и psycopg2 для взаимодействия с базой данных PostgreSQL. Система должна представлять из себя CRUD приложение. Фронтенд должен быть написан на языках: HTML, CSS, JavaScript.
# Основные функциональные требования к приложению:
1) Управление вызовами.
Создание вызова: диспетчер может зарегистрировать новый вызов, вводя информацию о пациенте, адресе, состоянии и времени вызова. Эта информация сохраняется в базе данных.
Чтение вызовов: диспетчер может просматривать список всех зарегистри-рованных вызовов. Также доступна возможность просмотра деталей каждого вызова.
Обновление вызова: диспетчер может обновить информацию о вызове. Также можно редактировать информацию о пациенте или адресе. Возможность назначить несколько бригад на вызов.
Удаление вызова: диспетчер может удалить вызов из системы, если он больше не актуален или был зарегистрирован ошибочно.
2) Мониторинг бригад: 
Диспетчер может просматривать список всех бригад с их статусами и составом.
# ER диаграмма системы
![image](https://github.com/user-attachments/assets/d91234e5-5687-4a86-a2e7-7fab6520fe33)
# Структура проекта
![image](https://github.com/user-attachments/assets/27388b99-46bb-445c-9d2d-60a3fcc2551f)
# Главная страница приложения
![image](https://github.com/user-attachments/assets/c7578f31-3ac0-4a70-bb3d-6222b73495a2)

# Главная страница приложения с деталями вызова
![image](https://github.com/user-attachments/assets/b5cb7046-1418-4994-9d9a-d4b889583a14)

# Детализация бригад
![image](https://github.com/user-attachments/assets/06e0fba5-22c7-4008-a891-6cb84e4cdd3f)

# Страница добавления вызова
![image](https://github.com/user-attachments/assets/9ecd9ba3-e2d3-4774-80b0-8204babc34df)

# Страница редактирования вызова
![image](https://github.com/user-attachments/assets/ed59a1d6-88c3-48b4-9f71-af2c3291d6d5)
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
