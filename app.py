from flask import Flask, render_template, request, session, redirect, url_for
from flask import jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Conexión a MongoDB
uri = "mongodb+srv://admin:upt2023@bdtranferapp.ovcij6h.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.bdrelampago
usuario = db.usuario

@app.route('/obtener_equipos', methods=['GET'])
def obtener_equipos():
    if 'user_id' in session:
        user_id = ObjectId(session['user_id'])
        user_data = usuario.find_one({"_id": user_id})

        if user_data and 'equipos' in user_data:
            equipos = user_data['equipos']
            print(f"JSONNNN{equipos}")
            return jsonify({'equipos': equipos})

    return jsonify({'error': 'No se pudieron obtener los equipos'})

# Nueva ruta para guardar partidosRonda1 en la base de datos
@app.route('/guardar_partidos_ronda1', methods=['POST'])
def guardar_partidos_ronda1():
    if request.is_json:
        data = request.get_json()
        partidos_ronda1 = data.get('partidosRonda1')

        if 'user_id' in session:
            user_id = ObjectId(session['user_id'])
            usuario.update_one(
                {"_id": user_id},
                {"$set": {"partidos_ronda1": partidos_ronda1}}
            )
            return jsonify({'success': True})

    return jsonify({'error': 'Error al guardar partidosRonda1'})


@app.route('/guardar_equipos', methods=['POST'])
def guardar_equipos():
    if 'user_id' in session:
        user_id = ObjectId(session['user_id'])
        user_data = usuario.find_one({"_id": user_id})
        
        if user_data:
            equipos_data = request.json.get('equipos')
            
            # Verificar si ya hay datos en la clave "equipos"
            if 'equipos' in user_data:
                # Actualizar el documento del usuario con la nueva información de equipos
                usuario.update_one(
                    {"_id": user_id},
                    {"$set": {"equipos": equipos_data}}
                )
            else:
                # Insertar la nueva información de equipos
                usuario.update_one(
                    {"_id": user_id},
                    {"$set": {"equipos": equipos_data}}
                )

            return jsonify({'mensaje': 'Datos guardados correctamente en MongoDB'})
    
    return jsonify({'error': 'Usuario no autenticado o datos no proporcionados'})







# Ruta para la página de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtiene los datos del formulario
        username = request.form['username']
        password = request.form['password']

        # Consulta el usuario en la base de datos
        user_data = usuario.find_one({"user": username, "password": password})

        if user_data:
            # Inicia sesión y redirige a la página de inicio
            session['user_id'] = str(user_data['_id'])
            print(f"Usuario autenticado: {user_data}")
            print(f"Sesión establecida: {session}")
            return redirect(url_for('home'))
        else:
            # Mensaje de error si las credenciales son incorrectas
            error_message = 'Credenciales incorrectas. Inténtalo de nuevo.'
            print(f"Error de autenticación: {error_message}")
            return render_template('login.html', error_message=error_message)

    # Renderiza la plantilla de inicio de sesión
    return render_template('login.html')

# Ruta para la página de inicio después de iniciar sesión
@app.route('/')
def home():
    # Verifica si el usuario está autenticado
    if 'user_id' in session:
        # Obtiene el nombre de usuario del usuario autenticado
        user_id = ObjectId(session['user_id'])
        user_data = usuario.find_one({"_id": user_id})
        print(f"Datos del usuario autenticado: {user_data}")
        
        if user_data:
            username = user_data['user']
            equipos = user_data.get('equipos', [])
            print(f"ASDASDASDASDASDASDASDASDASD{equipos}")
            # Renderiza la página de inicio con el nombre de usuario
            return render_template('index.html', username=username,equipos=equipos)
        else:
            print("No se encontraron datos del usuario en la base de datos.")
            session.pop('user_id', None)  # Elimina la sesión
            return redirect(url_for('login'))
    else:
        # Si el usuario no está autenticado, redirige al inicio de sesión
        print("El usuario no está autenticado. Redirigiendo al inicio de sesión.")
        return redirect(url_for('login'))

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    # Elimina la sesión y redirige al inicio de sesión
    session.pop('user_id', None)
    print("Sesión cerrada. Redirigiendo al inicio de sesión.")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


