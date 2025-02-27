#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/2/27 14:28
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   json_chain.py
# @Desc     :

from langchain.output_parsers import ResponseSchema, StructuredOutputParser

from utilis.tools import template_setter, is_key, opener, Timer


def main() -> None:
    """ Main Function """
    # Check if the OpenAI API Key is set.
    if is_key():
        print("The API key within the environment is set.")

        # Initialize the OpenAI model via ChatOpenAI of LangChain.
        chat = opener()
        if chat is not None:
            print("OpenAI API Key is valid.")

            instruction: str = """
                For the following text, extract the following information:
            
                gift: Was the item purchased as a gift for someone else? Answer True if yes, False if not or unknown.
                delivery_days: How many days did it take for the product to arrive? if this information is not present, output -1.
                price_value: Extract any sentences about the value or price, and output them as a comma separated Python list.
            
                Format the output as JSON with the following keys:
                gift
                delivery_days
                price_value
                
                text: {text}
                """
            # Initialize the ChatPromptTemplate object with the given instruction.
            template = template_setter(instruction)

            review: str = """
                This leaf blower is pretty amazing. 
                It has four settings: candle blower, gentle breeze, windy city, and tornado. 
                It arrived in two days, just in time for my wife's anniversary present. 
                I think my wife liked it so much she was speechless. 
                So far I've been the only one using it. 
                And I've been using it every other morning to clear the leaves on our lawn. 
                It's slightly more expensive than the other leaf blowers out there. 
                However, I think it's worth it for the extra features.
                """
            # Use the ChatPromptTemplate object to format the messages.
            messages: list = template.format_messages(text=review)

            # Invoke the OpenAI model with the formatted messages.
            with Timer(2, description="Gather Json Information", ) as timer:
                result = chat.invoke(messages)
                # The json style cannot be used directly via the key and value.
                print(result.content)
                print(f"{'Input Tokens':<14}: {result.usage_metadata['input_tokens']:04d}")
                print(f"{'Output Tokens':<14}: {result.usage_metadata['output_tokens']:04d}")
                print(f"{'Total Tokens':<14}: {result.usage_metadata['total_tokens']:04d}")
            print(timer)

            # Parse the output content with the ResponseSchema object.
            schemas: list = []
            instruction_json: dict = {
                "gift": "Was the item purchased as a gift for someone else? Answer True if yes, False if not or unknown.",
                "delivery_days": "How many days did it take for the product to arrive? if this information is not present, output 0.",
                "price_value": "Extract any sentences about the value or price, and output them as a comma separated list.",
            }
            for name, description in instruction_json.items():
                schema = ResponseSchema(name=name, description=description)
                schemas.append(schema)

            # Initialize the StructuredOutputParser object with the ResponseSchema objects.
            with Timer(2, description="Generate Instruction of Json Format", ) as timer:
                parser = StructuredOutputParser.from_response_schemas(schemas)
                # Parse the output content with the StructuredOutputParser object as a part of instructions.
                instruction_format = parser.get_format_instructions()
                print(instruction_format)
            print(timer)

            instruction_new: str = """
                    For the following text, extract the following information:
    
                    gift: Was the item purchased as a gift for someone else? Answer True if yes, False if not or unknown.
                    delivery_days: How many days did it take for the product to arrive? if this information is not present, output -1.
                    price_value: Extract any sentences about the value or price, and output them as a comma separated Python list.
    
                    text: {text}
                    
                    {instruction_format}
                    """
            # Initialize the ChatPromptTemplate object with the new instruction.
            template_new = template_setter(instruction_new)
            # Use the ChatPromptTemplate object to format the messages.
            messages_new: list = template_new.format_messages(text=review, instruction_format=instruction_format)

            # Invoke the OpenAI model with the formatted messages.
            with Timer(2, description="Get the Result with Json Format", ) as timer:
                result = chat.invoke(messages_new)
                print(result.content)
                print(f"{'Input Tokens':<14}: {result.usage_metadata['input_tokens']:04d}")
                print(f"{'Output Tokens':<14}: {result.usage_metadata['output_tokens']:04d}")
                print(f"{'Total Tokens':<14}: {result.usage_metadata['total_tokens']:04d}")
            print(timer)

            # Parse the output content with the StructuredOutputParser object.
            result_json = parser.parse(result.content)
            # Due to using the instruction formate, the json style can be used directly via the key and value.
            print(result_json["delivery_days"])
        else:
            print("OpenAI API Key is invalid.")
    else:
        print("The API key within the environment is not set.")


if __name__ == "__main__":
    main()
