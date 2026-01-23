from langsmith import traceable

@traceable
def hello():
    return "hello world"

if __name__ == "__main__":
    print(hello())
