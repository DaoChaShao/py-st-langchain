#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/2/26 23:03
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   tools.py
# @Desc     :

from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from os import getenv
from time import perf_counter


def is_key() -> bool:
    """ Check if the OpenAI API Key is set.

    :return:
    """
    _ = load_dotenv(find_dotenv())
    if getenv("OPENAI_API_KEY").startswith("sk-") and len(getenv("OPENAI_API_KEY")) == 164:
        return True
    else:
        return False


def opener(model: str = "gpt-4o-mini", temperature: float = 0.7) -> ChatOpenAI or None:
    """ Initialize the OpenAI model via ChatOpenAI of LangChain.
            - use the default model "gpt-4o-mini" or specify a model.
            - initialize the ChatOpenAI object and get its API key.
            - check if the object API key whether equals the API key got from the current env.

    :param model: use the default model "gpt-4o-mini" or specify a model.
    :param temperature: the temperature of the ChatOpenAI object.
    :return: ChatOpenAI object or None
    """
    payload: dict = {
        "stream": False,
    }
    chat = ChatOpenAI(model_name=model, temperature=temperature, model_kwargs=payload)
    if chat.openai_api_key.get_secret_value() == getenv("OPENAI_API_KEY"):
        return chat
    else:
        return None


def template_setter(instruction: str) -> ChatPromptTemplate:
    """ Initialize the ChatPromptTemplate object with the given instruction.

    :param instruction: the instruction of the ChatPromptTemplate object.
    :return: ChatPromptTemplate object
    """
    return ChatPromptTemplate.from_template(instruction)


class Timer(object):
    """ Timer class to measure the time elapsed. """

    def __init__(self, precision: int = 5, description: str = None) -> None:
        """ Initialize the Timer object.

        :param precision: the precision of the time elapsed.
        :param description: the description of the Timer object.
        """
        self._precision: int = precision
        self._description: str = description
        self._start: float = 0.0
        self._end: float = 0.0
        self._elapsed: float = 0.0

    def __enter__(self) -> object:
        self._start: float = perf_counter()
        print(f"{self._description} started.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._end: float = perf_counter()
        self._elapsed: float = self._end - self._start

    def __repr__(self) -> str:
        if self._elapsed > 0:
            return f"{self._description} took {self._elapsed:.{self._precision}} seconds."
        else:
            return f"{self._description} is not started."
