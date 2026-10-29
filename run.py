from app import app

if __name__ == "__main__":
    print("RUN.PY: Starting Flask")
    # Чомусь пропав вивід посилання в консолі, це єдина калька, яку я зміг придумати
    print("Сайт доступний за адресою: http://127.0.0.1:5000")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )
