from flask import Flask ,render_template,request,redirect, url_for,session
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash
from models.user import User
from services.user_service import UserService
from services.task_service import TaskService

from routes.auth_routes import auth_bp
from routes.task_routes import task_bp
import secrets


app=Flask(__name__)

@app.route("/")
def home():
    return render_template("welcome.html")

@app.route("/index")
def index():
    user_id = session.get("user_id")

    if "user_id" not in session:
        return redirect(url_for("auth.signin"))

    task_service = TaskService()
    tasks = task_service.getTaskByUserId(user_id)  
    return render_template("index.html",tasks=tasks)


app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)

app.secret_key=secrets.token_hex(16)

if __name__=="__main__":
    app.run(debug=True)