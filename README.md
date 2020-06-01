requirements:
    pip install Flask
    pip install flask_sqlalchemy
    pip install flask_script
    pip install flask_migrate
    pip install psycopg2-binary
 
migration:
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade

run server:
    python manage.py runserver
    
add config:
    app.config.from_object(config.DevelopmentConfig())
    - in manage.py
    - in app.py
    sql config - SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:psqlpass@localhost:5432/postgres'
    