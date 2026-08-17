from app.orchestration.graph import graph


def run_app(query: str):

    result = graph.invoke(
        {
            "query": query,
            "messages": [],
        }
    )

    return result["final_answer"]


if __name__ == "__main__":

    query = input("What would you like me to research?\n> ")

    answer = run_app(query)

    print("\n==============================")
    print("RESEARCH REPORT")
    print("==============================\n")

    print(answer)
