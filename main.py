import os
import traceback
from dotenv import load_dotenv
from google import genai


# Load API key from .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=GEMINI_API_KEY
)


def detect_errors(code):

    errors = []

    try:

        compiled_code = compile(
            code,
            "user_code.py",
            "exec"
        )

    except SyntaxError as error:

        errors.append({
            "error_type": "SyntaxError",
            "message": error.msg,
            "line": error.lineno
        })

        return errors

    try:

        exec(compiled_code)

    except Exception as error:

        trace = traceback.extract_tb(
            error.__traceback__
        )

        line = trace[-1].lineno

        errors.append({
            "error_type": type(error).__name__,
            "message": str(error),
            "line": line
        })

    return errors


def explain_error(error):

    prompt = f"""
You are a beginner-friendly Python teacher.

Explain this error briefly and clearly.

Error type: {error["error_type"]}
Error message: {error["message"]}
Line number: {error["line"]}

Use exactly these 4 sections:

**What happened:**
Explain the error in 1 short sentence.

**Why:**
Explain the reason in 1 short sentence.

**How to fix:**
Give the solution in 1-2 short sentences.

**Example:**
Give a very small corrected code example.

Rules:
- Keep the entire explanation under 120 words.
- Use simple English.
- Do not add unnecessary information.
- Do not discuss other possible errors.
- Focus only on this error.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# Test SobanPy
# This section runs only when main.py is executed directly.

if __name__ == "__main__":

    code = '''
x = 10
print(x)
print(y)
'''

    print("SobanPy")
    print("=" * 30)

    errors = detect_errors(code)

    if errors:

        print("\nDetected Errors:")

        for error in errors:

            print("\nError Type:", error["error_type"])
            print("Message:", error["message"])
            print("Line:", error["line"])

            print("\nGemini Explanation:")

            explanation = explain_error(error)

            print(explanation)

    else:

        print("\nNo errors detected.")