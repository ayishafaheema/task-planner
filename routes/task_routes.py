from flask import Blueprint,request,render_template ,redirect,url_for,current_app,session,jsonify
from services.task_service import TaskService 
from models.task import Task

task_bp=Blueprint("task",__name__)

@task_bp.route("/addTask",methods=["POST"])
def addTask():
      print("🎯 /addTask route called")  
        
      if "user_id" not in session:
         return redirect(url_for("auth.signin"))
      user_id = session.get("user_id")
        

      data=request.get_json()
      print("Received JSON:", data)

      title=data.get("title")
      due_date=data.get("due_date")
      priority=data.get("priority")
                  
         
                  
      print("Title:", title, "Due date:", due_date, "Priority:", priority, "User ID:", user_id)
         
      task=Task(
            user_id=user_id,
            title=title,
            due_date=due_date,
            priority=priority
      ) 
      task_service=TaskService()  
      success=task_service.addTask(task)  
      
      if not success:
        print("no success")
        return "Title is required", 400
  
      return jsonify({
            "message": "Task Saved",
            "task": {
                  "id": task.id,
                  "title": task.title,
                  "due_date": task.due_date,
                  "priority": task.priority
            }
            }), 200
                  
   
        
    
@task_bp.route("/getTask",methods=["GET"])
def getTask():
      user_id = session.get("user_id")

      if "user_id" not in session:
         return redirect(url_for("auth.signin"))
        
      task_service=TaskService() 
      tasks=task_service.getTaskByUserId(user_id)
      
      tasks_json=[
         {
            "id":task.id,
            "title":task.title,
            "due_date":task.due_date,
            "priority":task.priority
         }
         for task in tasks
      ]
   
      return jsonify(tasks_json)
            
        
@task_bp.route("/updateTask",methods=["POST"]) 
def updateTask():

      if "user_id" not in session:
            return redirect(url_for("auth.signin"))
      user_id = session.get("user_id") 
      
      data = request.get_json()
      task_id = data.get("task_id")  
      title = data.get("title")      
      due_date = data.get("due_date")
      priority = data.get("priority")

      task = Task(
        id=task_id,
        title=title,
        due_date=due_date,
        priority=priority,
        user_id=user_id
    )
      task_service=TaskService()
      task_service.updateTask(task)
      
      return redirect(url_for("index"))

@task_bp.route("/deleteTask/<int:task_id>",methods=["POST"])
def deleteTask(task_id):
      if "user_id" not in session:
            return redirect(url_for("auth.signin"))
      user_id = session.get("user_id") 
      
      
      task_service=TaskService()
      task_service.deleteTask(task_id,user_id)
      
      return redirect(url_for("index"))
      
      
         
      
          
              