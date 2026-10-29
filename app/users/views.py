from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    make_response,
)
from app.users import user_bp


@user_bp.route("/hi/<name>")
def greetings(name):
    age = request.args.get("age", default="", type=str)

    return render_template(
        "users/hi.html",
        name=name.upper(),
        age=age,
        title="Привітання",
    )


@user_bp.route("/admin")
def admin():
    return redirect(
        url_for("users.greetings", name="ADMINISTRATOR", age=45)
    )

# Облікові дані — без бази даних
DEMO_USERNAME = "student"
DEMO_PASSWORD = "qwerty123"


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if (
            username == DEMO_USERNAME
            and password == DEMO_PASSWORD
        ):
            session["username"] = username
            flash("Ви успішно увійшли в систему.", "success")
            return redirect(url_for("users.profile"))

        flash("Неправильне ім'я користувача або пароль.", "error")
        return redirect(url_for("users.login"))

    return render_template(
        "users/login.html",
        title="Вхід",
    )


@user_bp.route("/profile")
def profile():
    username = session.get("username")

    if not username:
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    theme = request.cookies.get("theme", "light")

    return render_template(
        "users/profile.html",
        username=username,
        theme=theme,
        title="Профіль",
    )


@user_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("users.login"))