from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.secret_key = "todo-list-secret-key"

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
    tasks = Task.query.all()

    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["GET", "POST"])
def add_task():

    if request.method == "POST":

        title = request.form.get("title")

        if not title or not title.strip():
            flash("Task title cannot be empty.", "error")
            return redirect(url_for("add_task"))

        new_task = Task(title=title.strip())

        db.session.add(new_task)
        db.session.commit()

        flash("Task added successfully!", "success")

        return redirect(url_for("home"))

    return render_template("add_task.html")


if __name__ == "__main__":
    app.run(debug=True)