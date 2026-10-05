const API_URL = "/api";

const taskForm = document.getElementById("task-form");
const taskInput = document.getElementById("task-input");
const taskList = document.getElementById("task-list");
const message = document.getElementById("message");


async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/tasks`);

        if (!response.ok) {
            throw new Error("Failed to load tasks");
        }

        const tasks = await response.json();

        renderTasks(tasks);

    } catch (error) {
        message.textContent = "Could not connect to backend.";
        console.error(error);
    }
}


function renderTasks(tasks) {
    taskList.innerHTML = "";

    tasks.forEach(task => {

        const li = document.createElement("li");

        const title = document.createElement("span");

        title.textContent = task.title;

        if (task.completed) {
            title.classList.add("completed");
        }

        const actions = document.createElement("div");

        actions.classList.add("actions");

        const toggleButton = document.createElement("button");

        toggleButton.textContent = task.completed
            ? "Undo"
            : "Done";

        toggleButton.onclick = () => toggleTask(task.id);


        const deleteButton = document.createElement("button");

        deleteButton.textContent = "Delete";

        deleteButton.onclick = () => deleteTask(task.id);


        actions.appendChild(toggleButton);
        actions.appendChild(deleteButton);

        li.appendChild(title);
        li.appendChild(actions);

        taskList.appendChild(li);
    });
}


taskForm.addEventListener("submit", async (event) => {

    event.preventDefault();

    const title = taskInput.value.trim();

    if (!title) {
        return;
    }

    try {

        const response = await fetch(`${API_URL}/tasks`, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                title: title
            })
        });

        if (!response.ok) {
            throw new Error("Failed to create task");
        }

        taskInput.value = "";

        await loadTasks();

    } catch (error) {
        message.textContent = "Could not create task.";
        console.error(error);
    }
});


async function toggleTask(id) {

    try {

        await fetch(`${API_URL}/tasks/${id}/toggle`, {
            method: "PUT"
        });

        await loadTasks();

    } catch (error) {
        console.error(error);
    }
}


async function deleteTask(id) {

    try {

        await fetch(`${API_URL}/tasks/${id}`, {
            method: "DELETE"
        });

        await loadTasks();

    } catch (error) {
        console.error(error);
    }
}


loadTasks();