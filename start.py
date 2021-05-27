# Обычно используется manage.py, но это будет лишнее для данного приложения.
from app import app

if __name__ == '__main__':
    app.run(debug=True, threaded=True)