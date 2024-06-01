import fastapi
from llama_cpp import Llama

app = fastapi.FastAPI()

# https://huggingface.co/bartowski/Llama-3-Smaug-8B-GGUF
llm = Llama.from_pretrained(
    # model_path="/root/.cache/huggingface/hub/models--bartowski--Llama-3-Smaug-8B-GGUF/snapshots/9f84c65352518dd31e56d9d3da09f03774ccb2c6/Llama-3-Smaug-8B-Q6_K.gguf",  # Download the model file first
    repo_id="SanctumAI/Meta-Llama-3-8B-Instruct-GGUF",
    filename="*instruct.Q3_K_M.gguf",
    n_threads=8,  # The number of CPU threads to use, tailor to your system and the resulting performance
    n_gpu_layers=-1,  # The number of layers to offload to GPU, if GPU available
    n_ctx=1500,  # The context length, the maximum number of tokens to consider in the context window
    chat_format="llama-3",
)

# Simple inference example
prompt_template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
Te llamas kukebot
contexto:{context}<|eot_id|>
<|start_header_id|>user<|end_header_id|>
{prompt}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>

"""
config = {
    "repeat_penalty": 1.1,
    "temperature": 0.1,
    "top_k": 10,
    "top_p": 0.95,
    "echo": False,
    "max_tokens": 1500,
}


def get_response(prompt, context):
    output = llm(
        prompt_template.format(context=context, prompt=prompt),
        stop=["<|eot_id|>"],
        **config,
    )
    return output["choices"][0]["text"]


@app.post("/submit-prompt")
def generate_answer(prompt: str, context: str = None):
    return get_response(prompt, context)
