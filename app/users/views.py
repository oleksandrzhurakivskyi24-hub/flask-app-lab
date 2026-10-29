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

    # Приховуємо службову cookie session, щоб не показувати в таблиці підписані дані Flask-сесії.
    cookies = {
        key: value
        for key, value in request.cookies.items()
        if key not in {"session"}
    }

    return render_template(
        "users/profile.html",
        username=username,
        theme=theme,
        cookies=cookies,
        title="Профіль",
    )


@user_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("users.login"))

@user_bp.route("/profile/cookies/add", methods=["POST"])
def add_cookie():
    if not session.get("username"):
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "").strip()
    max_age_raw = request.form.get("max_age", "").strip()

    if not key or not value:
        flash("Ключ і значення cookie обов'язкові.", "error")
        return redirect(url_for("users.profile"))

    # Не дозволяємо перезаписувати службові cookies застосунку.
    if key in {"session", "theme"}:
        flash("Цей ключ зарезервований для застосунку.", "error")
        return redirect(url_for("users.profile"))

    try:
        max_age = int(max_age_raw)
        if max_age <= 0:
            raise ValueError
    except ValueError:
        flash("Термін дії має бути додатним цілим числом секунд.", "error")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        httponly=True,
        samesite="Lax",
    )

    flash(f"Cookie «{key}» успішно додано.", "success")
    return response


@user_bp.route("/profile/cookies/delete", methods=["POST"])
def delete_cookie():
    if not session.get("username"):
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()

    if not key:
        flash("Укажіть ключ cookie для видалення.", "error")
        return redirect(url_for("users.profile"))

    if key in {"session", "theme"}:
        flash("Цей ключ зарезервований для застосунку.", "error")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))

    if key in request.cookies:
        response.delete_cookie(key)
        flash(f"Cookie «{key}» видалено.", "success")
    else:
        flash(f"Cookie «{key}» не знайдено.", "warning")

    return response


@user_bp.route("/profile/cookies/delete-all", methods=["POST"])
def delete_all_cookies():
    if not session.get("username"):
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    response = make_response(redirect(url_for("users.profile")))

    # Видаляємо cookies, створені для лабораторної.
    # Службову cookie session зберігаємо, щоб не втратити авторизацію.
    for key in request.cookies:
        if key not in {"session", "theme"}:
            response.delete_cookie(key)

    flash("Користувацькі cookies видалено.", "success")
    return response