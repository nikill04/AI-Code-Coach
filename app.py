"""Command-line version of AI Code Coach:  python app.py"""
from logic import process_query

TASKS = {"1": "Debug Code", "2": "Translate Code", "3": "Explain Algorithm"}


def main():
    print("\nAI Code Coach")
    for number, task in TASKS.items():
        print(f"{number}) {task}")

    choice = input("Choose (1/2/3): ").strip()
    if choice not in TASKS:
        print("Please enter 1, 2 or 3.")
        return
    query = input("Describe your problem: ")

    answer, docs = process_query(TASKS[choice], query)

    print("\n--- AI Response ---\n")
    print(answer)

    print("\n--- Relevant Code ---")
    for source in sorted({doc.metadata["source"] for doc in docs}):
        print(f"- {source}")


if __name__ == "__main__":
    main()
