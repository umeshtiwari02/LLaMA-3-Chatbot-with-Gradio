from groq import Groq
import gradio as gr
from config import api_key
from config import sys_prompt
import os

client = Groq(api_key=api_key)

# Initialize conversation with system message
system_prompt = sys_prompt

# Read CSS from external file
def load_css():
    css_file = os.path.join(os.path.dirname(__file__), "styles.css")
    with open(css_file, "r") as f:
        return f.read()

custom_css = load_css()

messages = [{"role": "system", "content": system_prompt}]

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

    # Chat container (initially hidden)
    with gr.Column(elem_classes="chat-container", visible=False) as chat_column:
        # Chat history
        chatbot = gr.Chatbot(
            elem_classes="chatbot",
            bubble_full_width=False,
            avatar_images=(None, "https://cdn-icons-png.flaticon.com/512/8943/8943377.png"),
            height="100%",
            show_label=False
        )

        # Input area inside chat container
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

    # Initial centered input (visible at start)
    with gr.Column(elem_classes="center-container", visible=True) as init_column:

        gr.Markdown(
            """<h2 class="title">👋 Hii, I'm your chatbot.</h2>"""
        )

        gr.Markdown(
            """<p>How can I help you today?</p>""",
            elem_classes="greeting-text"
        )

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
            return (
                gr.update(visible=False),
                gr.update(visible=True),
                chat_history
            )

        def respond(message, chat_history):
            return (
                message,
                gr.update(visible=True),
                gr.update(visible=False),
                chat_history
            )

        def predict(message, chat_history):
            # Add user message to history (only if not already present)
            if not chat_history or chat_history[-1][0] != message:
                messages.append({"role": "user", "content": message})

            # Get streaming response
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=messages,
                stream=True,
                temperature=0.7
            )

            assistant_response = ""

            # Stream the response
            for chunk in response:
                chunk_content = chunk.choices[0].delta.content or ""
                assistant_response += chunk_content
                # Only yield if we have new content
                if chunk_content:
                    yield chat_history + [(message, assistant_response)]

            # Update full message history
            messages.append({"role": "assistant", "content": assistant_response})

        # Initial submit handling
        init_msg.submit(
            respond,
            inputs=[init_msg, chatbot],
            outputs=[msg, chat_column, init_column, chatbot],
            queue=False
        ).then(
            predict,
            inputs=[msg, chatbot],
            outputs=chatbot
        ).then(
            lambda: "",
            None,
            msg
        )

        init_submit.click(
            respond,
            inputs=[init_msg, chatbot],
            outputs=[msg, chat_column, init_column, chatbot],
            queue=False
        ).then(
            predict,
            inputs=[msg, chatbot],
            outputs=chatbot
        ).then(
            lambda: "",
            None,
            msg
        )

        # Regular chat submit handling
        msg.submit(
            predict,
            inputs=[msg, chatbot],
            outputs=chatbot
        ).then(
            lambda: "",
            None,
            msg
        )

        submit.click(
            predict,
            inputs=[msg, chatbot],
            outputs=chatbot
        ).then(
            lambda: "",
            None,
            msg
        )

    # Footer
    gr.Markdown("""
    <div class='footer'>
        AI-generated, for reference only
    </div>
    """)


if __name__ == "__main__":
    demo.launch(
        auth=("admin", "password123"),
        auth_message="Please log in with valid username and password.",
        share=True
    )