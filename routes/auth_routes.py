from flask import Blueprint,request,render_template ,redirect,url_for,current_app,session
from services.user_service import UserService 
from models.user import User


auth_bp=Blueprint("auth",__name__)

@auth_bp.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        user_service=UserService()
        user=User(
            request.form.get("full_name"),
            request.form.get("email"),
            request.form.get("password")
        )
        return user_service.signUp(user)
    return render_template("signup.html")
         

@auth_bp.route("/signin",methods=["GET","POST"])
def signin():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        
        print("Login email:", email)

        user_service = UserService()
        return user_service.signIn(email,password)
    
    return render_template("Signin.html") 

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.signin"))
