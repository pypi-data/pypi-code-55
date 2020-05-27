import requests 
from bs4 import BeautifulSoup
import json

questions=[]
answers=[]
questions_collector=requests.get("https://www.toptal.com/algorithms/interview-questions")
print(questions_collector)
soup= BeautifulSoup(questions_collector.content, 'html.parser')

question_list=soup.find_all('div', class_='interview_question-content for-question content_body')
answer_list=soup.find_all('div', class_='interview_question-answer')
def put_ag_inlist():
    
    
    for question in question_list:
        all_questions=question.text.strip('\n')
        questions.append(all_questions)

        

    for answer in answer_list:
        all_answers=answer.text.strip('\n')
        answers.append(all_answers)

put_ag_inlist()
#print(questions)
with open('questions.json', 'w') as questions_file:
    json.dump(questions, questions_file)
with open('questions.json') as questions_file:
    read_questions=json.load(questions_file)

with open('answers.json', 'w' )as answers_file:
    json.dump(answers, answers_file)
with open('answers.json') as answers_file:
    read_answers=json.load(answers_file)