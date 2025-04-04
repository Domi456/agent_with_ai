from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
#from vector import retriever
import inquirer

model = OllamaLLM(model="Gemma3:1b")

template = """
You are a helpful assistant. Answer the following question based on the context provided.
Context: {context}
Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

questions = [
  inquirer.List('size',
                message="What size do you need?",
                choices=['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
            ),
]
answers = inquirer.prompt(questions)
print(answers)

context_multiline = input("Enter context (or 'bye' to quit): ")
context = " ".join(context_multiline.splitlines())

while True:
    if context.lower() == 'bye':
        print("Goodbye!")
        break

    print("-----------------------------------------")
    question = input("Enter your question (or 'bye' to quit): ")
    if question.lower() == 'bye':
        print("Goodbye!")
        break

    result = chain.invoke({
    "context": context,
    "question": question
    })
    print("\n")
    print(result)
