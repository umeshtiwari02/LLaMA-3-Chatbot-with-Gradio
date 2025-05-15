from groq import Groq
from config import api_key

client = Groq( api_key = api_key )

def chat(prompt):
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "system",
                "content": "ONLY respond to the current query. NEVER add:\n"
                        "- Apologies\n"
                        "- System status updates\n"
                        "- Explanations\n"
                        "- Unrequested information\n"
                        "Format: Complete sentences with normal punctuation."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True,
        temperature=0.7
    )

    for chunk in response:
        print(chunk.choices[0].delta.content or "", end="")



if __name__ == "__main__":
    print("Running...")
    start = True

    while start:
        prompt = input("\n\n\033[1m\033[92mAsk your question? or Type 'exit': \033[0m\033[0m ")
        if (prompt == 'exit'):
            print("\nThank you for using our chatbot!!\n")
            exit()
        print("\n\033[1m\033[94mChatbot ::\033[0m\033[0m \n")
        chat(prompt)
