from Rag.llm import get_llm


def review_output(question: str, answer: str):

    llm = get_llm()

    prompt = f"""
You are the final output reviewer for an enterprise AI assistant.

Review the response before it is shown to the user.

Your responsibilities:

1. Check that the response is relevant to the user's request.
2. Check that the response is understandable and professionally written.
3. Preserve factual content unless there is an obvious formatting problem.
4. Clean presentation issues.

IMPORTANT FORMATTING RULES:

- Do not return raw HTML.
- Remove or convert HTML tags such as:
  <br>
  <br/>
  <br />
  <b>
  </b>
  <strong>
  </strong>
  <p>
  </p>
  <li>
  </li>

- Convert HTML line breaks into normal Markdown line breaks.
- Convert HTML bullet formatting into normal Markdown bullets.
- Convert HTML bold formatting into Markdown bold only when useful.
- Do not expose HTML tags to the user.
- Avoid LaTeX unless the user explicitly asks for mathematical notation.
- Use simple readable Markdown.
- Preserve links.
- Preserve tables when present.
- Do not unnecessarily rewrite a correct answer.

User question:
{question}

Assistant response:
{answer}

Return your result in exactly this format:

STATUS: pass

CLEANED_ANSWER:
<final cleaned answer>

If the response is seriously incorrect, unsafe, irrelevant, or unusable, return:

STATUS: fail

CLEANED_ANSWER:
<cleaned answer if possible>
"""

    response = llm.invoke(prompt)

    text = response.content.strip()


    # --------------------------------------------------
    # PARSE STATUS
    # --------------------------------------------------

    if "STATUS: fail" in text:
        status = "fail"
    else:
        status = "pass"


    # --------------------------------------------------
    # PARSE CLEANED ANSWER
    # --------------------------------------------------

    marker = "CLEANED_ANSWER:"

    if marker in text:

        cleaned_answer = text.split(
            marker,
            1
        )[1].strip()

    else:

        cleaned_answer = answer


    return {
        "status": status,
        "answer": cleaned_answer
    }