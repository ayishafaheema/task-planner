class Task:
    def __init__(self,user_id,title,due_date,priority,id=None):
        self.id=id
        self.user_id=user_id
        self.title=title
        self.due_date=due_date
        self.priority=priority