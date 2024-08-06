from django.core.mail import send_mail
from celery import shared_task
from decouple import config
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

@shared_task
def send_activation_code(email: str,activation_code: str):
    activation_url = f'{config("LINK")}api/v1/user/activate/{activation_code}'
    html_message = f'''
            <html>
            <head>
                <style>
                    /* Пример стилизации кнопки */
                    .activation-button {{
                        display: inline-block;
                        width: 140px;  /* Указание ширины кнопки */
                        height: 40px;  /* Указание высоты кнопки */
                        border-radius: 5px;
                        padding: 10px 25px;
                        background-color: #b03835;
                        color: #ffffff !important;
                        text-align: center;
                        text-decoration: none;
                        line-height: 40px; /* Вертикальное выравнивание текста */
                    }}
                    .activation-button:hover {{
                        background-color: #8c2c2b;
                    }}
                </style>
            </head>
            <body>
                <h2>Регистрация пользователя</h2>
                <h3>Рады приветствовать Вас на нашем сайте ToDoList! Для завершения регистрации, нажмите на кнопку ниже</h3>
                <a href="{activation_url}" class="activation-button">Активировать аккаунт</a>
            </body>
            </html>
        '''

    send_mail(
        subject="Активация аккаунта",
        message="",
        from_email='ashirova09.02@mail.ru',
        recipient_list=[email],
        html_message=html_message,
    )
