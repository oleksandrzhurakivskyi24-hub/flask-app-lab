from app import app

if __name__ == "__main__":
    print("RUN.PY: запуск Flask")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )