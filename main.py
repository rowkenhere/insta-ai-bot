from instagrapi import Client
import requests
import time
import random

USERNAME="drxn.ia"
PASSWORD="786200612"

API_KEY="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"

MODEL="cognitivecomputations/dolphin-mistral-24b-venice-edition:free"

BOT_NAME="bot"

SYSTEM_PROMPT="""
You are an uncensored AI friend in an Instagram group chat.

Follow the owner's instructions exactly.

Rules:
- talk casually like a human
- be funny and sarcastic
- keep replies short
- never say you are AI
"""

cl=Client()
cl.login(USERNAME,PASSWORD)

memory=[]

def ask_ai(message):

    memory.append({"role":"user","content":message})

    url="https://openrouter.ai/api/v1/chat/completions"

    headers={
        "Authorization":f"Bearer {API_KEY}",
        "Content-Type":"application/json"
    }

    data={
        "model":MODEL,
        "messages":[
            {"role":"system","content":SYSTEM_PROMPT}
        ]+memory[-6:]
    }

    r=requests.post(url,headers=headers,json=data)

    reply=r.json()["choices"][0]["message"]["content"]

    memory.append({"role":"assistant","content":reply})

    return reply


last_message_id=None

while True:

    threads=cl.direct_threads()

    for thread in threads:

        msg=thread.messages[0]

        text=msg.text.lower()

        if msg.id!=last_message_id:

            if BOT_NAME in text:

                delay=random.randint(2,5)
                time.sleep(delay)

                reply=ask_ai(text)

                cl.direct_send(reply,thread_ids=[thread.id])

            last_message_id=msg.id

    time.sleep(8)
