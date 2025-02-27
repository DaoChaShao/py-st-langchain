#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/2/27 15:54
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   memory_chat.py
# @Desc     :

from uuid import uuid4

from utilis.tools import is_key, opener, histories_chat_getter, conversations_summary_getter, Timer


def main() -> None:
    """ Main Function """
    if is_key():
        print("The API key within the environment is set.")

        chat = opener(temperature=0.0)
        if chat is not None:
            print("OpenAI API Key is valid.")

            # Set up the id number of the whole conversation
            session_id = str(uuid4())
            # Set up the memory object
            histories: dict = {}
            # Set up the memory store
            memory = histories_chat_getter(session_id, histories)

            # Star the conversation
            prompts: list[str] = [
                "Please give me 3 random numbers",
                "Please sum the numbers",
            ]
            with Timer(2, "Conversation in Chat Counter", ) as timer:
                conversations_summary_getter(chat, memory, prompts, session_id)
            print(timer)
        else:
            print("OpenAI API Key is invalid.")
    else:
        print("The API key within the environment is not set.")


if __name__ == "__main__":
    main()
