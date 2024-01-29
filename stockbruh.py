from openai import OpenAI
from dotenv import load_dotenv
import os
import time


load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
assistant_id = os.environ.get("STOCKBRUH_ASSISTANT_ID")

client = OpenAI()

def initialize_thread():
    thread = client.beta.threads.create()

    return thread


def submit_message(thread, user_input):
    # Create message
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )
    return run


def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="desc")


def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


def pretty_print(messages):
    for m in messages:
        if m.role == "assistant":
            return m.content[0].text.value
