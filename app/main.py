from app.orchestration.graph import graph


def run_app(query: str):

    result = graph.invoke(
        {
            "query": query,
        }
    )

    return result["final_answer"]


if __name__ == "__main__":

    query = input("What would you like me to do?\n> ")

    answer = run_app(query)

    print("\n==============================")
    print("OUTPUT")
    print("==============================\n")

    print(answer)
