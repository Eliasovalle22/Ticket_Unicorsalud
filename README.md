# Ticket_Unicorsalud
 Turnos de atención al cliente Admisiones

# Crear un entorno virtual
    pip install virtualen
    python -m venv venv

# Activar el entorno (Windows)
    venv\Scripts\activate

# Instalar Django y el conector de PostgreSQL
    pip install django psycopg2

# Crear el proyecto
    django-admin startproject turnos_unicorsalud .

# Crear la app principal
    python manage.py startapp gestion_turnos

# Actualizar librerias e instalarlas
    pip install -r requirements.txt -- instalar las librerias
    pip freeze > requirements.txt -- actualizar la lista de librerias



# Creación de modulos
    python manage.py startapp nombre_del_modulo

# Creación de los modelos de la BD con el ORM de Django
    python manage.py makemigrations -- migración de las tablas
    python manage.py migrate -- creación de tablas en la BD

# Crear un superusuario (administrador)
    python manage.py createsuperuser


# Ejecución local
    python manage.py runserver