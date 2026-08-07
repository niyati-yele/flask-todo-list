from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

db_path = os.path.join(BASE_DIR, "database", "todo.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Task {self.title}>"

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "<h1>Database Connected Successfully!</h1>"


if __name__ == "__main__":
    app.run(debug=True)