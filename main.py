import json
import webbrowser
from difflib import get_close_matches
from pprint import pprint
from time import sleep

def backup() -> dict:
    with open('info.json', 'r', encoding="utf-8") as f:
        dat: dict = json.load(f)
        return dat


def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r', encoding="utf-8") as file:
        data: dict = json.load(file)
    return data


def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=2)
        
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None


print(None)
def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    toml: dict = backup()
    pprint(toml, sort_dicts=False)
    
    while True:
        user_input: str = input("You: ")
        
        if user_input.lower() == 'quit':
            break
        
        best_match: str = find_best_match(user_input, [q['question'] for q in knowledge_base["questions"]])
        
        if best_match:
            if best_match == "Play Jeopardy!":
                webbrowser.open("https://pizzaprogrammer.itch.io/jeopardy")
            sleep(1.0)
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            sleep(1.0)
            print('Bot: I don\'t know the answer. Can you please clarify?')
            new_answer: str = input('Type the answer or "skip" to skip: ')
            
            if new_answer.lower() != 'skip':
                knowledge_base['questions'].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I learned a new response!')


chat_bot()
