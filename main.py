from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import inquirer
import time
import threading
from context_source import ContextSource

def loading(stop_event):
    animation = "/-\|"
    idx = 0
    while not stop_event.is_set():
        print(animation[idx % len(animation)], end="\r")
        idx += 1
        time.sleep(0.1)
        if idx == len(animation):
            idx = 0


model = OllamaLLM(model="Gemma3:1b")

template = """
You are a helpful assistant. Answer the following question. Primarily try to answer based on the context provided.
Context: {context}
Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

questions = [
  inquirer.List('src',
                message="Context?",
                choices=['from file', 'from text input'],
            ),
]
answers = inquirer.prompt(questions)

BLUE = "\x1b[0;36m"
RESET = "\x1b[0m"
context = ""

if answers['src'] == 'from file':
    context_path = input(f"\n{BLUE}Enter path (or 'bye' to quit): {RESET}")
    if context_path.lower() == 'bye':
        print("Goodbye!")
        exit()
    else:
        context_source = ContextSource(context_path)
        try:
            context = context_source.parse_to_string()
        except ValueError as e:
            print(e)
            exit(0)
elif answers['src'] == 'from text input':
    context_multiline = input("Enter context (or 'bye' to quit): ")
    context = " ".join(context_multiline.splitlines())

while True:
    if context.lower() == 'bye':
        print("Goodbye!")
        break

    print("-----------------------------------------")
    
    question = input(f"{BLUE}Enter your question (or 'bye' to quit): {RESET}")
    if question.lower() == 'bye':
        print("Goodbye!")
        break

    stop_event = threading.Event()
    loading_thread = threading.Thread(target=loading, args=(stop_event,))
    loading_thread.start()

    try:
        result = chain.invoke({
            "context": context,
            "question": question
        })
    finally:
        stop_event.set()
        loading_thread.join()
    
    print("\n")
    print(result)
