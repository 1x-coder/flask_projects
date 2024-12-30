addTaskBtn = document.querySelector(".add-task-btn");

body = document.querySelector("body")

addTaskBtn.addEventListener('click', () => {
    taskTitle = document.querySelector(".task-title-input").value;
    taskDescription = document.querySelector(".task-description-input").value;
    fetch("/add", {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            task_title: taskTitle,
            task_description: taskDescription
        })
    })
    .then(() => {
        window.location.reload();
    })
});