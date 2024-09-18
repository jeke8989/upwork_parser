from sqlalchemy import create_engine

conn = psycopg2.connect(
    dbname="your_database",
    user="your_username",
    password="your_password",
    host="localhost",
    port="5432"
)

# Формат строки подключения: postgresql://<user>:<password>@<host>:<port>/<dbname>
engine = create_engine('postgresql://your_username:your_password@localhost:5432/your_database_name')