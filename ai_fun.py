from langchain_deepseek.chat_models import ChatDeepSeek
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from prompt_model import creat_prompt
from chat_history import r, get_chat_history, add_chat_pair
from embending_fun import search_jobs


def format_context(similar_jobs):
    return "\n\n".join(
        item["document"] for item in similar_jobs
    )


def retrieve_context(question):
    similar_jobs = search_jobs(question=question, top_k=5)
    return format_context(similar_jobs)


def ai_fun(human_question):
    chat = ChatDeepSeek(model="deepseek-v4-pro")

    finally_prompt = creat_prompt()

    chain = (
        {
            "human_question": RunnablePassthrough(),
            "context": RunnablePassthrough() | RunnableLambda(retrieve_context),
            "chat_history": RunnableLambda(lambda _: get_chat_history(r)),
        }
        | finally_prompt
        | chat
    )

    res = chain.invoke(human_question)

    answer = res.content

    add_chat_pair(r, human=human_question, ai=answer)

    return answer