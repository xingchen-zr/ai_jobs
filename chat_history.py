import json
import time
import uuid
from datetime import datetime

from langchain_core.messages import HumanMessage, AIMessage
from redis import Redis


r = Redis(decode_responses=True)

DEFAULT_SESSION_ID = "default"
CHAT_TTL_SECONDS = 60 * 60 * 24
MAX_HISTORY_TURNS = 10


def add_chat_pair(r, human: str, ai: str):
    session_id = DEFAULT_SESSION_ID

    now = time.time()
    turn_key = f"chat:turn:{session_id}:{int(now * 1000)}:{uuid.uuid4().hex[:8]}"
    index_key = f"chat:turns:{session_id}"

    data = {
        "human": human,
        "ai": ai,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    r.set(turn_key, json.dumps(data, ensure_ascii=False), ex=CHAT_TTL_SECONDS)
    r.zadd(index_key, {turn_key: now})

    return turn_key


def get_chat_history(r):
    session_id = DEFAULT_SESSION_ID
    index_key = f"chat:turns:{session_id}"

    turn_keys = r.zrevrange(index_key, 0, MAX_HISTORY_TURNS - 1)

    chat_hisstory = []
    expired_keys = []

    for key in reversed(turn_keys):
        raw = r.get(key)

        if raw is None:
            expired_keys.append(key)
            continue

        data = json.loads(raw)

        chat_hisstory.append(HumanMessage(content=data["human"]))
        chat_hisstory.append(AIMessage(content=data["ai"]))

    if expired_keys:
        r.zrem(index_key, *expired_keys)

    return chat_hisstory