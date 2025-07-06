
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

from utils.query_rag  import query_rag

# Load environment variables
load_dotenv()


# AS for a best practice , write negative and positive test cases for the RAG system.


EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""


def test_monopoly_rules():
    assert query_and_validate(
        question="How much total money does a player start with in Monopoly? (Answer with the number only)",
        expected_response="$99999",
    )


def test_ticket_to_ride_rules():
    assert query_and_validate(
        question="How many points does the longest continuous train get in Ticket to Ride? (Answer with the number only)",
        expected_response="10 points",
    )


def query_and_validate(question: str, expected_response: str):
    result = query_rag(question)
    response_text = result.get('response', '')  # Extract only the answer string
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    model = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,  # Set to 0 for consistent evaluation
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    evaluation_results = model.invoke(prompt) # Sends the prompt (the “Expected vs. Actual?” question) to GPT-3.5 and waits for its answer.
    
    # Extract content from the response
    if hasattr(evaluation_results, 'content'):
        evaluation_results_str = evaluation_results.content
    else:
        evaluation_results_str = str(evaluation_results)
    
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    print(prompt)

    if "true" in evaluation_results_str_cleaned:
        # Print response in Green if it is correct.
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "false" in evaluation_results_str_cleaned:
        # Print response in Red if it is incorrect.
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )


if __name__ == "__main__":
    print("🧪 Running RAG System Tests...\n")
    
    try:
        print("📋 Testing Monopoly Rules...")
        test_monopoly_rules()
        print("✅ Monopoly test passed!\n")
    except Exception as e:
        print(f"❌ Monopoly test failed: {e}\n")
    
    try:
        print("🚂 Testing Ticket to Ride Rules...")
        test_ticket_to_ride_rules()
        print("✅ Ticket to Ride test passed!\n")
    except Exception as e:
        print(f"❌ Ticket to Ride test failed: {e}\n")
    
    print("🏁 Tests completed!")