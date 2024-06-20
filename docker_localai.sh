docker run -ti --name local-ai -p 8080:8080 --gpus all localai/localai:latest-aio-gpu-nvidia-cuda-12

docker run -p 8080:8080 localai/localai:v2.17.1-ffmpeg-core

docker pull localai/localai:v2.17.1-cublas-cuda12-core

docker run -ti --name local-ai -p 8080:8080 --gpus all localai/localai:v2.17.1-cublas-cuda12-core

docker run -ti -p 8080:8080 --gpus all localai/localai:v2.9.0-cublas-cuda12-core phi-2

curl --location 'http://localhost:8080/models/apply' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": "TheBloke/Luna-AI-Llama2-Uncensored-GGML/luna-ai-llama2-uncensored.ggmlv3.q5_K_M.bin",
    "name": "lunademo"
}'


curl --location 'http://localhost:8080/models/apply' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": "QuantFactory/Meta-Llama-3-8B-Instruct-GGUF/blob/main/Meta-Llama-3-8B-Instruct.Q2_K.gguf.bin",
    "name": "thellama3"
}'

QuantFactory/Meta-Llama-3-8B-Instruct-GGUF/blob/main/Meta-Llama-3-8B-Instruct.Q2_K.gguf

curl http://localhost:8080/v1/chat/completions -H "Content-Type: application/json" -d '{ "model": "llama3-8b-instruct", "messages": [{"role": "user", "content": "How are you doing?", "temperature": 0.1}] }'