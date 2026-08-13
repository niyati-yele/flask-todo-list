from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)

app.secret_key = "todo-list-secret-key"


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

database_dir = os.path.join(BASE_DIR, "database")

os.makedirs(database_dir, exist_ok=True)

db_path = os.path.join(database_dir, "todo.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


# ============================================================
# TASK MODEL
# ============================================================

class Task(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    completed = db.Column(
        db.Boolean,
        default=False
    )

    def __repr__(self):
        return f"<Task {self.title}>"


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

with app.app_context():

    db.create_all()


# ============================================================
# HOME / READ TASKS
# ============================================================

@app.route("/")
def home():

    tasks = Task.query.all()

    return render_template(
        "index.html",
        tasks=tasks
    )


# ============================================================
# ADD TASK
# ============================================================

@app.route("/add", methods=["GET", "POST"])
def add_task():

    if request.method == "POST":

        title = request.form.get("title")

        if not title or not title.strip():

            flash(
                "Task title cannot be empty.",
                "error"
            )

            return redirect(
                url_for("add_task")
            )

        new_task = Task(
            title=title.strip()
        )

        db.session.add(new_task)

        db.session.commit()

        flash(
            "Task added successfully!",
            "success"
        )

        return redirect(
            url_for("home")
        )

    return render_template(
        "add_task.html"
    )


# ============================================================
# EDIT TASK
# ============================================================

@app.route(
    "/edit/<int:task_id>",
    methods=["GET", "POST"]
)
def edit_task(task_id):

    task = Task.query.get_or_404(task_id)

    if request.method == "POST":

        title = request.form.get("title")

        if not title or not title.strip():

            flash(
                "Task title cannot be empty.",
                "error"
            )

            return redirect(
                url_for(
                    "edit_task",
                    task_id=task.id
                )
            )

        task.title = title.strip()

        db.session.commit()

        flash(
            "Task updated successfully!",
            "success"
        )

        return redirect(
            url_for("home")
        )

    return render_template(
        "edit_task.html",
        task=task
    )

#the Status Route
@app.route("/toggle/<int:task_id>")
def toggle_task(task_id):

    task = Task.query.get_or_404(task_id)

    task.completed = not task.completed

    db.session.commit()

    if task.completed:
        flash("Task marked as completed!", "success")
    else:
        flash("Task marked as pending!", "success")

    return redirect(url_for("home"))
# ============================================================
# DELETE TASK
# ============================================================

@app.route("/delete/<int:task_id>")
def delete_task(task_id):

    task = Task.query.get_or_404(task_id)

    db.session.delete(task)

    db.session.commit()

    flash(
        "Task deleted successfully!",
        "success"
    )

    return redirect(
        url_for("home")
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run()
    # app.run(debug=True)