from flask import redirect, url_for,session
from models.user import User
from werkzeug.security import generate_password_hash
from services.db_service import DBService
from werkzeug.security import check_password_hash

class UserService :
    
    def signUp(self, user: User):
        db = DBService()

        user.password = generate_password_hash(user.password)
        #print(user.password)
        db.insertUserIntoDb(user)
        return redirect(url_for("auth.signin"))

    def signIn(self,email,password):
        #users = self.getAllUsers()
        #print("All users:", users)
        #print("Looking for email:", email)

        db=DBService()
        user_row=db.getUserByEmail(email)
        
        if user_row is None:
            return "user is not found"
        
        #convert tuple to user object
        user=User(
            full_name=user_row[1],
            email=user_row[2],
            password=user_row[3]   
        )
        
        user.id = user_row[0]

        hashed_password=user_row[3]
        if check_password_hash(hashed_password,password):
            session["user_id"]=user.id
            session["full_name"]=user.full_name
            
            return redirect(url_for("index"))
        else:
            return "invalid email or password"
        
        
        

