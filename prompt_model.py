#ai提示词
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def creat_prompt(human_question: str | None = None):
    finally_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "你是一个求职职位分析助手。你只能根据提供的职位信息回答问题，"
            "不能编造职位、公司、薪资或要求。若职位信息不足，请明确说明信息不足。"
        ),
        MessagesPlaceholder("chat_history"),
        (
            "human",
            "用户问题：{human_question}\n\n"
            "检索到的职位信息：\n{context}"
        )
    ])

    return finally_prompt