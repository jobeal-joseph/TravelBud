from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')

CORS(app)
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)