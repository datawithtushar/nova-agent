from Graph.rag_workflow import app


def test_rag():

    question = "What is my company policy for bonus"

    result = app.invoke(
        {
            "question": question,
            "retry_count": 0
        }
    )

    print("\nQUESTION:")
    print(question)

    print("\nANSWER:")
    print(result.get("answer"))

    print("\nSOURCES:")
    print(result.get("sources", []))


if __name__ == "__main__":
    test_rag()