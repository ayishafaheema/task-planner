from models.task import Task
import sqlite3

class TaskService:
    
    def addTask(self,task:Task):
        with sqlite3.connect("database.db") as connection:
            cursor=connection.cursor()
            
            if not  task.title or task.title.strip()=="":
                return False
            
            cursor.execute("INSERT INTO tasks (user_id, title, due_date, priority) VALUES (?, ?, ?, ?)",
                (task.user_id, task.title, task.due_date, task.priority)
    )
        
        return True
        
        
    
    def getTaskByUserId(self,user_id):
        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()
        
        cursor.execute("SELECT * FROM tasks WHERE user_id=?" , (user_id,))
        rows=cursor.fetchall()
        connection.close()
        
        tasks=[]
        for row in rows:
            task=Task(
                user_id=row[1],
                title=row[2],
                due_date=row[3],   
                priority=row[4]
        )
            task.id = row[0]  
            tasks.append(task)
        
        return tasks
    
    def updateTask(self,task):
        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()
        
        cursor.execute(
            """
            UPDATE tasks 
            SET title=?,due_date=?,priority=? 
            WHERE id=? AND user_id=? 
            """,
            ( task.title, task.due_date, task.priority,task.id, task.user_id)
        )
        
        connection.commit()
        connection.close()
        
    
    def deleteTask(self,task_id,user_id):
        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()
        
        cursor.execute(
            """
            DELETE FROM tasks
            WHERE id=? AND user_id=?
            """,
            (task_id,user_id)
            
        )
        connection.commit()
        connection.close()
        
        
        