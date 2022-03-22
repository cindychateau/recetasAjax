from flask import Flask

app = Flask(__name__)

app.secret_key = "Mi clave secreta wuuuuu"

app.config['UPLOAD_FOLDER'] = 'flask_app/static/img/'