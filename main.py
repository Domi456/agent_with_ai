from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
#from vector import retriever

model = OllamaLLM(model="Gemma3:1b")

template = """
You are a helpful assistant. Answer the following question based on the context provided.
Context: {context}
Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

context_multiline = input("Enter context: ")
context = " ".join(context_multiline.splitlines())
print("\n-----------------------------------------")

while True:
    print("\n-----------------------------------------")
    question = input("Enter your question (or 'bye' to quit): ")
    if question.lower() == 'bye' or context.lower() == 'bye':
        print("Goodbye!")
        break

    result = chain.invoke({
    "context": context,
    "question": question
    })
    print("\n")
    print(result)
