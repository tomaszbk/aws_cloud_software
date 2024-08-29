import gradio as gr


def llm_response(message, histoy):
    return f"I'm sorry, I don't understand your messasge {message}"


gr.ChatInterface(llm_response).launch()
