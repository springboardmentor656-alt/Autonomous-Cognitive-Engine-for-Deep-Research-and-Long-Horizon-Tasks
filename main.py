from dotenv import load_dotenv
load_dotenv()

from agent.supervisor import run_tasks

def main():

    task = input("Enter a complex task: ").strip()

    if not task:
        print("No task provided.")
        return

    run_tasks(task)


if __name__ == "__main__":
    main()
