from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

dataframe = pd.read_csv("sample.csv")
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = ".\chroma_db"
add_docs = not os.path.exists(db_location)

if add_docs:
    documents = []
    ids = []
    for i, row in dataframe.iterrows():
        doc = Document(
            page_content=row["Title"] + " " + row["Review"], 
            metadata={"rating": row["Rating"], "date": row["Date"]}, 
            id = str(i)
        )
        documents.append(doc)
        ids.append(str(i))

vectorstore = Chroma(
    collection_name="sample",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_docs:
    vectorstore.add_documents(documents=documents, ids=ids)

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    