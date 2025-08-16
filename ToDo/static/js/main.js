document.addEventListener('DOMContentLoaded', () => {

    const taskForm = document.querySelector('.tasksform form');
    const taskList = document.querySelector('.taskslist');
    const taskURL = document.getElementById('tasksbox').dataset.taskUrl;
    console.log('task URL: ', taskURL);
    console.log('taskList id:', taskList.id);

    // ---------------- CREATE TASK ---------------- //

    taskForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(taskForm);
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        const response = await fetch(taskURL, {
            method : 'POST',
            headers : {
                'X-CSRFToken': csrfToken
            },
            body: formData
        });

        const data = await response.json();

        if(data.status == 'success')
        {
            const taskContainer = document.querySelector('.taskslist');
            const newTask = document.createElement('div');
            newTask.textContent = data.task.taskTitle;

            // newTask.innerHTML = `
            //     <span class="taskTitle">${data.task.taskTitle}</span>
            //     ${data.task.creationTime}
            //     <input type="checkbox" class="taskDoneChckBox" data-task-id="${data.task.id}" ${data.task.isDone ? 'checked' : ''}>
            //     <input type="submit" class="deleteTaskBtn" data-task-id="${data.task.id}" value="Delete">`;

            taskContainer.prepend(newTask);
            
            // clear form
            taskForm.reset();
        }
        else 
        {
            alert(data.error || 'Failed to create task');
        }
    });

    // ---------------- UPDATE TASK ---------------- //

    taskList.addEventListener('change', async (e) => {

        if(e.target.classList.contains('taskDoneChckBox'))
        {
            e.preventDefault();
            const taskID = e.target.dataset.taskId;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;            
            
            const response = await fetch(taskURL, {
                method: 'PUT',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({task_id: taskID})
            });

            const data = await response.json();

            if(data.status == 'success')
            {
                // toggle strikethrough
                const taskText = e.target.previousElementSibling;

                if(e.target.checked)
                {
                    taskText.style.textDecoration = 'line-through';
                }
                else 
                {
                    taskText.style.textDecoration = 'none';
                }
            }
            else
            {
                alert(data.error || 'Failed to edit task');   
            }
        }
    });

    // ---------------- DELETE TASK ---------------- //

    taskList.addEventListener('click', async (e) => {

        if(e.target.classList.contains('deleteTaskBtn'))
        {
            e.preventDefault();
            const taskID = e.target.dataset.taskId;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;            
            
            const respose = await fetch(taskURL, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                },
                body : JSON.stringify({task_id : taskID})
            });
            
            const data = await respose.json();
            
            if(data.status == 'success')
            {
                // remove the entire task from DOM
                e.target.parentElement.remove();
            }
            else 
            {
                alert(data.error || 'Failed to delete task');
            }
        }
    }); 


});