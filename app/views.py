import logging
from pathlib import Path

from flask import render_template, request, redirect, url_for, flash
from app import app
from app.forms import ContactForm


@app.route("/")
def home():
    return render_template("homepage.html", title="Головна")


@app.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме")


@app.route("/contacts")
def contacts():
    return render_template("contacts.html", title="Контакти")

LOG_DIR = Path(app.root_path).parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(LOG_DIR / "contact.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    encoding="utf-8",
)

contact_logger = logging.getLogger("contact_form")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        try:
            contact_logger.info(
                "Contact form submitted: name=%r email=%r subject=%r message=%r",
                form.name.data,
                form.email.data,
                form.subject.data,
                form.message.data,
            )

            flash(
                "Повідомлення успішно перевірено та записано в журнал.",
                "success",
            )

        except OSError:
            app.logger.exception("Не вдалося записати контактне повідомлення")
            flash(
                "Не вдалося зберегти повідомлення. Спробуйте ще раз.",
                "error",
            )

        return redirect(url_for("contact"))

    if request.method == "POST":
        flash(
            "Форма містить помилки. Перевірте поля нижче.",
            "error",
        )

    return render_template(
        "contact.html",
        form=form,
        title="Контакти",
    )