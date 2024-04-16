import configparser
from typing import Any

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

config = configparser.ConfigParser()
config.read("config.ini")
# Validate VectorDB and Model are legal
if "LLM" not in config or "VectorDB" not in config["LLM"] or "Model" not in config["LLM"]:
    raise ValueError("Missing LLM configuration in config.ini, expected [LLM] section with VectorDB and Model keys.")
if config["LLM"]["VectorDB"] not in ["faiss", "chroma"]:
    raise ValueError(f"Invalid VectorDB in config.ini, expected 'faiss' or 'chroma'. Got {config['LLM']['VectorDB']}.")
if config["LLM"]["Model"] not in ["mistral", "llama2"]:
    raise ValueError(f"Invalid Model in config.ini, expected 'mistral' or 'llama2'. Got {config['LLM']['Model']}.")


class ChatBot:
    def __init__(self):
        self.model_name: str = config["LLM"]["Model"]
        self.llm = ChatOllama(model=self.model_name, temperature=0)
        self.prompt = ChatPromptTemplate.from_template(
            """[INST]
You get a user "query", and a list of most similar items to the user query under "context".
Your main task is to output the most similar SQL prompt assignment to the user, based on the given "context".
You are not suppose to generate SQL or python code, just take the most fitting assignment marked by "sql_prompt" in the context.
Use only the user query and the context to generate the output.
Your output should be markdown similar to "output_format".

<output_format>
Based on your query, the recommended SQL assignment is: `assignment`.
</output_format>

<context>
{docs}
</context>

<query>
"{user_query}"
</query>

[/INST]
"""
        )
        self.chain = self.prompt | self.llm | StrOutputParser()

    def invoke(self, user_query: str, context: Any) -> str:
        """Invoke the chatbot with a user query and context."""
        response = self.chain.invoke({"user_query": user_query, "docs": context})
        return response
