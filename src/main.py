# flask-app.py
from flask import Flask
from handlers import handlers_blueprint

# create a Flask instance
app = Flask(__name__)

# Register blueprints
app.register_blueprint(handlers_blueprint)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=1995)
