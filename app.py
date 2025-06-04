from groq import Groq
from config import api_key  # import from config.py

client = Groq(api_key=api_key)

def main():
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "Explain the importance of low latency LLMs"}
        ],
        model="llama3-8b-8192",
    )

    print(chat_completion.choices[0].message.content)

if __name__ == "__main__":
    main()
