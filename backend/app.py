from flask import Flask, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../frontend/templates')
app.config.from_object('config.Config')

CORS(app)
db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

