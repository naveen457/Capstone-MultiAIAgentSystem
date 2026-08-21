from app.orchestration.graph import graph
from langchain_core.messages import HumanMessage, SystemMessage

config = {
    "configurable": {
        "thread_id": "admin",
    },
}


def run_app(query: str):
    result = graph.invoke(
        {
            "query": query,
            "messages": [
                HumanMessage(content=query),
            ],
        },
        config=config,
    )

    return result["final_answer"]


if __name__ == "__main__":

    print("What would you like me to do?")

    while True:
        query = input("> ")

        if query.lower() == "exit":
            break

        answer = run_app(query)

        print(answer)
