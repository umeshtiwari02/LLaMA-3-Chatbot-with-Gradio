from groq import GroqClient
import gradio as gr
from config import api_key, sys_prompt
import os

# Initialize Groq client
client = GroqClient(api_key=api_key)

# Load custom CSS
def load_css():
    css_file = os.path.join(os.path.dirname(__file__), "styles.css")
    with open(css_file, "r") as f:
        return f.read()

custom_css = load_css()
messages = [{"role": "system", "content": sys_prompt}]

with gr.Blocks(
    title="Chatbot",
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="lime",
        neutral_hue="slate"
    ),
    css=custom_css,
    head='<link rel="icon" href="https://cdn-icons-png.flaticon.com/512/13330/13330989.png" type="image/png">'
) as demo:

    # Header
    gr.Markdown("""<h1 class="title">Your Own Chatbot</h1>""")

    with gr.Column(elem_classes="chat-container", visible=False) as chat_column:
        chatbot = gr.Chatbot(
            elem_classes="chatbot",
            bubble_full_width=False,
            avatar_images=(None, "https://cdn-icons-png.flaticon.com/512/8943/8943377.png"),
            height="100%",
            show_label=False
        )

        with gr.Row():
            msg = gr.Textbox(
                placeholder="Write your message...",
                show_label=False,
                container=False,
                elem_classes="input-box",
                lines=1,
                max_lines=5,
                scale=8
            )
            submit = gr.Button(
                "Send",
                variant="primary",
                min_width=80,
                elem_classes="send-btn",
                scale=1
            )

    with gr.Column(elem_classes="center-container", visible=True) as init_column:
        gr.Markdown("""<h2 class="title">👋 Hii, I'm your chatbot.</h2>""")
        gr.Markdown("""<p>How can I help you today?</p>""", elem_classes="greeting-text")

        with gr.Row(elem_classes="input-row"):
            init_msg = gr.Textbox(
                placeholder="Write your message...",
                show_label=False,
                container=False,
                elem_classes="input-box",
                lines=1,
                max_lines=5,
                scale=8
            )
            init_submit = gr.Button(
                "Send",
                variant="primary",
                min_width=80,
                elem_classes="send-btn",
                scale=1
            )

        def toggle_visibility(message, chat_history):
            return gr.update(visible=False), gr.update(visible=True), chat_history

        def respond(message, chat_history):
            return message, gr.update(visible=True), gr.update(visible=False), chat_history

        def predict(message, chat_history):
            if not chat_history or chat_history[-1][0] != message:
                messages.append({"role": "user", "content": message})

            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=messages,
                stream=True,
                temperature=0.7
            )

            assistant_response = ""
            for chunk in response:
                chunk_content = chunk.choices[0].delta.content or ""
                assistant_response += chunk_content
                if chunk_content:
                    yield chat_history + [(message, assistant_response)]

            messages.append({"role": "assistant", "content": assistant_response})

        # Submit handlers
        for trigger in [init_msg.submit, init_submit.click]:
            trigger(
                respond,
                inputs=[init_msg, chatbot],
                outputs=[msg, chat_column, init_column, chatbot],
                queue=False
            ).then(
                predict,
                inputs=[msg, chatbot],
                outputs=chatbot
            ).then(lambda: "", None, msg)

        for trigger in [msg.submit, submit.click]:
            trigger(
                predict,
                inputs=[msg, chatbot],
                outputs=chatbot
            ).then(lambda: "", None, msg)

    # Footer
    gr.Markdown("""<div class='footer'>AI-generated, for reference only</div>""")


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 8080)),
        auth=("admin", "password123") if os.getenv("RENDER") else None
    )
