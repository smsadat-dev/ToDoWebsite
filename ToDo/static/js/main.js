document.addEventListener('DOMContentLoaded', ()=> {

    const taskslist = document.getElementById('taskslist');
   
    // ---------- CHECKBOX AUTO-UPDATE ----------
    taskslist.addEventListener('change', (e) => {
        if(e.target.classList.contains('taskDoneChckBox'))
        {
            const taskID = e.target.dataset.taskID;
            const isDone = e.target.chekced;
            
            fetch("{% url 'base:task' %}", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: new URLSearchParams({
                    'action': 'update',
                    'task_id': taskID,
                    'is_done': isDone
                })
            })
            .then(res => res.json)
            .then(data => {
                if(data.status == 'Success')
                {
                    const li = document.getElementById(`task-${taskID}`);
                    if(isDone)
                    {
                        li.querySelector('s')?.remove();
                        li.innerHTML = `<s>${li.textContent}</s>` + li.innerHTML.slice(li.innerHTML.indexOf('<input'));
                    }
                }
                else 
                {
                    // Remove <s> if unchecked
                    const sTag = li.querySelector('s');
                    if(sTag){
                        const text = sTag.textContent;
                        sTag.replaceWith(document.createTextNode(text));
                    }
                }
            });
            
        }
    });

    // ---------- DELETE TASK ----------
    taskslist.addEventListener('click', (e) => {
        if(e.target.classList.contains('deleteTaskBtn'))
        {
            const taskID = e.target.dataset.taskID;

            fetch("{% url 'base:task' %}", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: new URLSearchParams({
                    'action': 'delete',
                    'task_id': taskID
                })
            })
            .then(res => res.json)
            .then(data => {
                if(data.status == 'Success')
                {
                    document.getElementById(`task-${taskID}`).remove();
                }
            })
        }
    });

});