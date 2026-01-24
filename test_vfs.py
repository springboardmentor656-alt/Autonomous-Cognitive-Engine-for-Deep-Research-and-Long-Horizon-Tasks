"""
Local test for Milestone-2 Virtual File System (VFS)

This file is ONLY for local verification.
It does NOT create LangSmith traces.
"""

from agent.filesystem import write_file, read_file


def main():
    # Initialize virtual in-memory state
    state = {
        "files": {}
    }

    print("--- Testing Write File ---")

    # Call tool's underlying function using .func
    write_file.func(
        filename="bmw_notes.txt",
        content="BMW focuses on EV strategy",
        state=state
    )

    print("Write successful.")

    print("\n--- Testing Read File ---")

    content = read_file.func(
        filename="bmw_notes.txt",
        state=state
    )

    print("Read Result:", content)

    print("\n--- Current State ---")
    print(state)


if __name__ == "__main__":
    main()
