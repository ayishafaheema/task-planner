const colors = ["#fbcad9ff", "#E4F9E8", "#CDE7FF", "#FFF3C7"];
let count = 0;



let tasks=[];
function updateUI(){
        const emptySpace=document.getElementById("empty-state");    
            if (tasks.length==0){
                emptySpace.style.display="block";
            }else{
                emptySpace.style.display="none";
            }
        }



function showPopup(message){
    console.log("Popup called:", message); 
    document.getElementById("popup-message").innerText=message;
    document.getElementById("popup-overlay").style.display="flex";
}  
function closePopup(){
    document.getElementById("popup-overlay").style.display="none";
}



async function loadTask() {
    const response = await fetch("/getTask")
    tasks = await response.json();
    console.log(tasks);

    updateUI();

    const taskContainer = document.getElementById("task-container");
    taskContainer.innerHTML = "";

    count = 0;

    tasks.forEach(task => {
        const box = document.createElement("div");
        box.classList.add("task-box");

        box.style.backgroundColor = colors[count % colors.length];
        count++;

        box.innerHTML = `
            <input type="text" class="task-title" value="${task.title}" disabled>
            <input type="date" class="task-date" value="${task.due_date}" disabled>

            <select class="task-priority" disabled>
                <option value="high" ${task.priority === "high" ? "selected" : ""}>High</option>
                <option value="medium" ${task.priority === "medium" ? "selected" : ""}>Medium</option>
                <option value="low" ${task.priority === "low" ? "selected" : ""}>Low</option>
            </select>
            <button class="save-btn">saved</button>
            <div class="small-btn">
                 <button class="edit-btn">Edit</button>
                 <button class="delete-btn">Delete</button>
            </div>
        `;

        
        
    

        /*EDIT*/

        box.querySelector(".edit-btn").addEventListener("click", () => {

            box.querySelectorAll(".task-title,.task-date,.task-priority").forEach(item => item.disabled = false);
            box.querySelector(".save-btn").innerText = "Save";
            box.querySelector(".small-btn").style.display = "none";

            box.querySelector(".save-btn").onclick = async () => {
                try {
                    const response = await fetch("/updateTask", {
                        method: "POST",
                        headers: { "content-Type": "application/json" },
                        body: JSON.stringify({
                            task_id: task.id,
                            title: box.querySelector(".task-title").value,
                            due_date: box.querySelector(".task-date").value,
                            priority: box.querySelector(".task-priority").value

                        })
                    });
                    if (!response.ok) {
                        /*alert("Error saving task");*/ // always show generic message
                        showPopup("Error saving task. Please try again.");

                        return;
                    }




                    box.querySelector(".save-btn").onclick = null;

                    box.querySelectorAll(".task-title,.task-date,.task-priority").forEach(item => item.disabled = true);
                    box.querySelector(".save-btn").innerText = "Saved";
                    box.querySelector(".small-btn").style.display = "flex";

                } catch (error) {
                    console.error(error);
                }
            };

        });
        /*DELETE*/

        box.querySelector(".delete-btn").addEventListener("click", async () => {
            const response = await fetch(`/deleteTask/${task.id}`, {
                method: "POST"

            });

            if (response.ok)
                box.remove();
                loadTask();
        });

        taskContainer.appendChild(box);

    });
}



document.querySelector('.add-btn').addEventListener('click', () => {
    updateUI();

    const newBox = document.createElement('div');
    newBox.classList.add('task-box');

    newBox.style.backgroundColor = colors[count % colors.length];
    count++;

    newBox.innerHTML = `
            <input type="text" placeholder="task title" class="task-title">
            <input type="date" class="task-date">
            <select class="task-priority">
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
            </select>
            <button class="save-button">Save</button>`;


    const saveBtn = newBox.querySelector('.save-button');
    saveBtn.addEventListener('click', async () => {

        console.log("Save button clicked!");

        const title = newBox.querySelector('.task-title').value;
        const due_date = newBox.querySelector('.task-date').value;
        const priority = newBox.querySelector('.task-priority').value;

        const response = await fetch("/addTask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: title,
                due_date: due_date,
                priority: priority
            })
        });
        console.log(response);

        if (!response.ok) {
            /*alert("Error saving task");*/
            showPopup("Task title is required");

            return;
        }
        loadTask();


    }


    );
    document.querySelector('#task-container').appendChild(newBox)

});
window.onload = loadTask;