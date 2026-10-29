from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
)


class ContactForm(FlaskForm):
    name = StringField(
        "Ваше ім'я",
        validators=[
            DataRequired(message="Введіть ім'я."),
            Length(min=2, max=80, message="Ім'я має містити від 2 до 80 символів."),
        ],
    )

    email = StringField(
        "Електронна пошта",
        validators=[
            DataRequired(message="Введіть електронну пошту."),
            Email(message="Введіть коректну електронну адресу."),
        ],
    )

    subject = SelectField(
        "Тема звернення",
        choices=[
            ("question", "Запитання"),
            ("cooperation", "Співпраця"),
            ("feedback", "Відгук"),
        ],
        validators=[
            DataRequired(message="Оберіть тему звернення."),
        ],
    )

    message = TextAreaField(
        "Повідомлення",
        validators=[
            DataRequired(message="Введіть повідомлення."),
            Length(min=10, max=3000, message="Повідомлення має містити від 10 до 3000 символів."),
        ],
    )

    submit = SubmitField("Надіслати")