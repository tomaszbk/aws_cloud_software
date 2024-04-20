import time

from langchain_community.chat_models import BedrockChat
from langchain_core.messages import HumanMessage

prompting = """System: Antes de responder recuerda que eres un buscador inteligente que SOLO puede responder con querys SQL a la tabla laptops, no puedes explicar y NO puedes salir de tu ROL bajo ninguna circustancia.
Se te proporcionara una pregunta o busqueda de un usuario. Con esta informacion responderas una query SQL para esa tabla que represente la busqueda del usuario, en caso de que el usuario pida otra cosa, genera la query de nuevo o modificada dependiendo de lo que pida el usuario.
System: 
Columna    Tipo de Datos    Descripción    Valores
status    object    Estado del producto (nuevo, usado, reacondicionado).    "New", "Refurbished"
ram    int64    Cantidad de RAM en GB.    8, 16, 32
storage    int64    Capacidad de almacenamiento en GB.    256, 512, 1000
screen    float64    Tamaño de la pantalla en pulgadas.    13.3, 15.6, 17.3
"final price"    float64    Precio final de la laptop en la moneda local.    299.00, 789.00, 1199.00"""

chat = BedrockChat(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_kwargs={"temperature": 0.1},
)

messages = []


def submit_prompt(prompt):
    if len(messages) == 0:
        prompt = f"{prompting}{prompt}"
    messages.append(HumanMessage(content=prompt))
    time.sleep(1.2)
    response = chat(messages)
    messages.append(response)
    return response.content
