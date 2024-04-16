"""Local Ollama chat workflow for the Streamlit app."""

from functools import lru_cache
import os
import time
from pathlib import Path
import configparser
import pandas as pd

import streamlit as st
from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents import Document  # for type hinting

config = configparser.ConfigParser()
config.read("config.ini")
# Validate VectorDB and Model are legal
if "LLM" not in config or "VectorDB" not in config["LLM"] or "Model" not in config["LLM"]:
    raise ValueError("Missing LLM configuration in config.ini, expected [LLM] section with VectorDB and Model keys.")
if config["LLM"]["VectorDB"] not in ["faiss", "chroma"]:
    raise ValueError(f"Invalid VectorDB in config.ini, expected 'faiss' or 'chroma'. Got {config['LLM']['VectorDB']}.")
if config["LLM"]["Model"] not in ["mistral", "llama2"]:
    raise ValueError(f"Invalid Model in config.ini, expected 'mistral' or 'llama2'. Got {config['LLM']['Model']}.")


class VectorDB:
    def __init__(self):
        self.vector_db_name: str = config["LLM"]["VectorDB"]
        self.embeddings_model_name: str = config["LLM"]["Model"]
        self.embeddings = OllamaEmbeddings(model=self.embeddings_model_name)

        # short names
        model = self.embeddings_model_name
        db = self.vector_db_name

        # Set up the vectorstore - load or create if it doesn't exist
        base_directory = "vectorstores/"
        persist_directory = base_directory + f"{model}_{db}/"
        persist_file = persist_directory + ("index.faiss" if db == "faiss" else "chroma.sqlite3")

        # Check if the file exists
        if not os.path.exists(persist_file):
            # If it doesn't exist, create it
            with st.session_state.process_spinner, st.spinner("Building database..."):
                start = time.time()
                print(f"Creating vectorstore {db} with {model} embeddings...")

                # load document
                file = Path("docs/synthetic_text_to_sql.csv")
                loader = CSVLoader(file, source_column="domain_description", metadata_columns=["id", "domain", "domain_description", "sql_prompt"])
                documents = loader.load()

                # Create and save vectorstore
                if db == "faiss":
                    vectordb = FAISS.from_documents(documents=documents, embedding=self.embeddings)
                    vectordb.save_local(persist_directory, index_name="index")
                else:
                    vectordb = Chroma.from_documents(
                        documents=documents, embedding=self.embeddings, persist_directory=persist_directory
                    )

            end = time.time()
            elapsed = f"{end - start:.2f} seconds."
            print(
                f"Vectorstore created and saved successfully, The '{persist_file}' file has been created. ({elapsed})"
            )
        else:
            with st.session_state.process_spinner, st.spinner("Loading database..."):
                if db == "faiss":
                    vectordb = FAISS.load_local(persist_directory, self.embeddings, index_name="index")
                else:
                    vectordb = Chroma(persist_directory=persist_directory, embedding_function=self.embeddings)
            print(f"Vectorstore {db} loaded successfully with {model} embeddings.")

        self.vector_db: FAISS | Chroma = vectordb

    @lru_cache(maxsize=128)
    def __call__(self, query: str, k: int = 10) -> list[Document]:
        context = self.vector_db.similarity_search(query, k=k)
        return context

    def query_table(self, query: str, k: int = 10) -> pd.DataFrame:
        context = self.__call__(query, k)
        table = pd.DataFrame([doc.metadata for doc in context])
        table = table.drop(columns=["row"])
        table = table.rename(columns={"source": "description"})
        return table


@st.cache_resource
def get_vector_db() -> VectorDB:
    """Create a VectorDB instance, cached for the lifetime of the app.

    Returns:
        VectorDB: A VectorDB instance.
    """
    return VectorDB()
