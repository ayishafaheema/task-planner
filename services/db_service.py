from models.user import User
import sqlite3
import os

class DBService:

    def insertUserIntoDb(self, user :User):
        query = "INSERT INTO users(full_name,email,password)VALUES(?,?,?)"
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        
        
        print("USING DB FILE:", os.path.abspath("database.db"))


        cursor.execute(query, (user.full_name, user.email, user.password))
        connection.commit()
        connection.close()

    def getUserByEmail(self,email):
        #query=("SELECT * FROM users WHERE email= ? ")
        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()
        
        cursor.execute("SELECT * FROM users WHERE EMAIL=?" ,(email,))
        row=cursor.fetchone()
        connection.close()
        
        
        return row
        
        