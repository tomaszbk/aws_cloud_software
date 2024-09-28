from fastapi.routing import APIRouter
from llama_index.core.workflow import (
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step,
)
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer
from app.database.models import User

chat_store = SimpleChatStore()



router = APIRouter()
IN_AWS = False
if IN_AWS is True:
    from llama_index.llms.bedrock import Bedrock

    profile_name = "Your aws profile name"
    llm = Bedrock(model="amazon.titan-text-express-v1", profile_name=profile_name)
else:
    from llama_index.llms.ollama import Ollama

    llm = Ollama(model="llama3.1", base_url="http://aws-ollama:11434")

class JokeEvent(Event):
    joke: str


class UserInteractFlow(Workflow):
    llm=llm

    @step
    async def orchestrate_llm(self, ev: StartEvent) -> JokeEvent:
        chat_history = ev.chat_history

        prompt = f"chat_history"
        response = await self.llm.achat(chat_history)
        return JokeEvent(joke=str(response))

    @step
    async def critique_joke(self, ev: JokeEvent) -> StopEvent:
        joke = ev.joke

        prompt = f"Give a thorough analysis and critique of the following joke: {joke}"
        response = await self.llm.acomplete(prompt)
        return StopEvent(result=str(response))


@router.get("/user-message")
async def hanlde_user_message(user_prompt: str, user: User):

    chat_memory = ChatMemoryBuffer.from_defaults(
        token_limit=3000,
        chat_store=chat_store,
        chat_store_key=user.phone_number,
    )

    chat_history = chat_memory.get()
    if not chat_history:
        print("chat history is empty, creating new chat history")
        chat_history = [
            ChatMessage(role=MessageRole.USER, content=user_prompt),
        ]


    w = UserInteractFlow(timeout=60, verbose=False)
    result = await w.run(chat_history=chat_history)
    chat_history.append(ChatMessage(role=MessageRole.ASSISTANT, content=result))
    chat_memory.set(chat_history)

    return result

# prompt = ChatMessage(
#     role=MessageRole.USER,
#     text="What is the meaning of life?",
# )

# print(type(llm.complete("What is the meaning of life?")))
