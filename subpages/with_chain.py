#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/2/26 23:45
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   with_chain.py
# @Desc     :   

from utilis.tools import is_key, opener, template_setter, Timer


def main():
    if is_key():
        print("The API key within the environment is set.")

        chat = opener()
        if chat is not None:
            print("OpenAI API Key is valid.")

            instruction: str = "Translate the content of {text} with {tone} from English to Chinese."
            template = template_setter(instruction)

            text: str = (
                "Arrr, I be fuming that me blender lid flew off and splattered me kitchen walls with smoothie! "
                "And to make matters worse, the warranty don't cover the cost of cleaning up me kitchen. "
                "I need yer help right now, matey!")
            tone: str = "a polite tone"
            content: dict = {
                "text": text,
                "tone": tone,
            }

            with Timer(2, description="Translation", ) as timer:
                chain = template | chat
                result = chain.invoke(content)
                print(result.content)
                print(f"{'Input Tokens':<14}: {result.usage_metadata['input_tokens']:04d}")
                print(f"{'Output Tokens':<14}: {result.usage_metadata['output_tokens']:04d}")
                print(f"{'Total Tokens':<14}: {result.usage_metadata['total_tokens']:04d}")
            print(timer)
        else:
            print("OpenAI API Key is invalid.")
    else:
        print("The API key within the environment is not set.")


if __name__ == "__main__":
    main()
