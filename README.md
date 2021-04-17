Приложение создано с использованием виртуального окружения
> virtualenv venv --python=python3.9

Активация виртуального окружения
> source venv/bin/activate

Установка зависимостей
> pip install -r requirements.txt

Запуск приложения с использованием Gunicorn
> gunicorn -w 4 app.main:application --bind 127.0.0.1:8080

Название фреймворка Gungner, который вынесен в отдельный каталог. Само приложение находитсяя в каталоге app.