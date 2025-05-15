from groq import Groq
from config import api_key

client = Groq(api_key=api_key)

# Initialize conversation with system message
messages = [
    {
        "role": "system",
        "content": "**USER INSTRUCTIONS**\n"
                   "ONLY respond to the current query. NEVER add:\n"
                   "- Apologies\n"
                   "- System status updates\n"
                   "- Explanations\n"
                   "- Unrequested information\n\n"
                   "**RESPONSE FORMAT**\n"
                   "Complete sentences with normal punctuation."
    }
]

def chat_with_history(prompt):
    # Add user message to history
    messages.append({"role": "user", "content": prompt})

    # Get streaming response
    response = client.chat.completions.create(
        model="llama3-70b-8192",  # Updated to current recommended model
        messages=messages,
        stream=True,
        temperature=0.7  # Added for more natural responses
    )

    assistant_response = ""
    print("\n\033[1m\033[94mChatbot ::\033[0m\033[0m ", end="")

    # Process streaming chunks
    for chunk in response:
        chunk_content = chunk.choices[0].delta.content or ""
        print(chunk_content, end="", flush=True)
        assistant_response += chunk_content

    # Add assistant response to history
    messages.append({"role": "assistant", "content": assistant_response})
    return assistant_response

if __name__ == "__main__":
    print("\033[1m\033[92mChatbot initialized. Type 'exit' to end.\033[0m")

    while True:
        try:
            prompt = input("\n\033[1m\033[92mYou: \033[0m")
            if prompt.lower() in ('exit', 'quit'):
                print("\n\033[1mThank you for using our chatbot!\033[0m\n")
                break

            chat_with_history(prompt)

        except KeyboardInterrupt:
            print("\n\033[1mSession ended by user.\033[0m")
            break
        except Exception as e:
            print(f"\n\033[91mError: {str(e)}\033[0m")
            continue