from flask import json, request, Flask
import mysql.connector
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

""" db_user = os.getenv('USER_DB')
db_pass = os.getenv('KEY_DB')
db_host = os.getenv('HOST_DB')
db_port = os.getenv('PORT_DB')
db_database = os.getenv('NAME_DB') """

db_user = 'poke'
db_pass = 'poke'
db_host = 'poke-db'
db_port = 3306
db_database = 'poke'


def get_db_connection():
    conn = mysql.connector.connect(
        host=db_host,
        user=db_user,
        passwd=db_pass,
        port=db_port,
        database=db_database
    )
    return conn

PREFIX = "/api/poke"

@app.route(PREFIX + '/')
def getHolaMundo():
    return json.dumps({"message": 'Hola Mundo Python, un Saludo desde el Microservicio que conecta con la Bakugan-DB!'}), 200


@app.route(PREFIX + '/get-all-bakugan')
def get_all_bakugans():
    con = get_db_connection()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM bakugan")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    res = json.dumps([dict(zip(column_names, row)) for row in rows])

    return res


@app.route(PREFIX + '/insert-bakugan', methods=['POST'])
def insertbakugan():
    data = request.get_json()  # Obtener los datos del cuerpo de la solicitud
    name = data.get('name')
    type_primary = data.get('type_primary')
    type_secondary = data.get('type_secondary')

    if not name or not type_primary:
        return json.dumps({"error": "Faltan campos requeridos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''INSERT INTO bakugan (name, type_primary, type_secondary)
                          VALUES (%s, %s, %s)''', (name, type_primary, type_secondary))
        conn.commit()
        conn.close()
        return json.dumps({"message": "Bakugan insertado con éxito"}), 201
    except mysql.connector.Error as e:
        conn.close()
        return json.dumps({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route(PREFIX + '/delete-bakugan/<int:id>', methods=['DELETE'])
def deletebakugan(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM bakugan WHERE id = ?', (id,))
        conn.commit()

        if cursor.rowcount == 0:
            conn.close()
            return json.dumps({"error": "Bakugan no encontrado"}), 404

        conn.close()
        return json.dumps({"message": "Bakugan eliminado con éxito"}), 200
    except mysql.connector.Error as e:
        conn.close()
        return json.dumps({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
