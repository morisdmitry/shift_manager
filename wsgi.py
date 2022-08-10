from app import create_app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config.get('DEBUG'), host="0.0.0.0", port=app.config.get('BACKEND_PORT'))
