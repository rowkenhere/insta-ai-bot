from instagrapi import Client
import requests
import time
import random

USERNAME="benx.ai0"
PASSWORD="tajmiya12345"

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
cl.login(USERNAME, PASSWORD)
print("Instagram login successful")
time.sleep(15)

memory=[]

def ask_ai(message):

    memory.append({"role":"user","content":message})

    url="https://openrouter.ai/api/v1/chat/completions"

    headers={
 "Authorization":f"Bearer {API_KEY}",
 "HTTP-Referer":"https://railway.app",
 "X-Title":"instagram-ai-bot",
 "Content-Type":"application/json"
}

    data={
 "model":MODEL,
 "messages":[
  {"role":"system","content":SYSTEM_PROMPT}
 ]+memory[-6:],
 "temperature":0.7,
 "max_tokens":500
}

    r=requests.post(url,headers=headers,json=data)

    res=r.json()

    if "choices" in res:
        reply=res["choices"][0]["message"]["content"]
    else:
        print("OpenRouter response:",res)
        reply="AI error bro"

    memory.append({"role":"assistant","content":reply})

    return reply


last_message_id=None

while True:

    threads=cl.direct_threads()

    for thread in threads:

        msg=thread.messages[0]

        text = (msg.text or "").lower()

        if msg.id!=last_message_id:

            if BOT_NAME in text:

                delay=random.randint(2,5)
                time.sleep(delay)

                reply=ask_ai(text)

                cl.direct_send(reply,thread_ids=[thread.id])

            last_message_id=msg.id

    time.sleep(8)
