# main.py
from dotenv import load_dotenv
load_dotenv()

from agent.supervisor import run_tasks  # ✅ Import after adding supervisor.py to same directory

def main():
    tasks = []

    # Prompt user for complex tasks
    while True:
        task = input("Enter a complex task (or press Enter to finish): ")
        if not task.strip():
            break
        tasks.append(task)

    if not tasks:
        print("No tasks provided.")
        return

    # Run the supervisor
    run_tasks(tasks)

if __name__ == "__main__":
    main()
