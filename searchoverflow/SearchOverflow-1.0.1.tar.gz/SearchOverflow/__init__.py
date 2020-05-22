from __future__ import print_function, unicode_literals

from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
import requests 
import json
import html2text
import sys

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

url_first_half = "https://api.stackexchange.com/2.2/search?pagesize=20&order=desc&sort=relevance&intitle="
url_second_half = "&filter=default&site=stackoverflow&key=aN0B8QKN8Pz4UNqgu0YcxA(("
question_url_first = "https://api.stackexchange.com/2.2/questions/"
question_url_second = "?order=desc&sort=activity&site=stackoverflow&filter=!9_bDDxJY5&key=aN0B8QKN8Pz4UNqgu0YcxA(("
answer_url_first = "https://api.stackexchange.com/2.2/questions/"
answer_url_second =  "/answers?order=desc&sort=activity&site=stackoverflow&filter=!9_bDE(fI5&key=aN0B8QKN8Pz4UNqgu0YcxA(("

#To print json response:
#print(json.dumps(json_data, indent=4, sort_keys=True))
def make_request(url):
    return requests.get(url).json()


def main():
    first = True
    initial_search = ""
    for i in range(1, len(sys.argv)):
        initial_search = initial_search + " " + sys.argv[i]
        
    while(True):
        if(len(initial_search) <= 0 or (first == False)):
            questions = [
                {   'type': 'input',
                    'name': 'search_terms',
                    'message': 'Search: ',
                    'validate': lambda answer: 'You must enter search terms.' \
                        if len(answer) == 0 else True
                }
            ]

            #Dictionary that contains the user input
            answer = prompt(questions, style=style)

            #We substitute spaces with "-" to add it to an url
            search_key_words = answer['search_terms'].replace(" ", "-", -1)

        elif(first):
            search_key_words = initial_search[1:].replace(" ", "-", -1)

        first = False

        #We form the url
        url_complete = url_first_half + search_key_words + url_second_half

        json_data = make_request(url_complete)

        #Now we have an array of items, item -> questions
        q_data = json_data['items']
        if(len(q_data) > 0):
            break
        else:
            print("No results for " + search_key_words.replace("-", " ", -1))


    #Making an array with the titles to make the selection
    question_titles = []
    question_dictionary = {}

    i = 0
    for data in q_data:
        question_titles.append(data['title'])
        question_dictionary[data['title']] = data['question_id']

    if (len(question_titles) > 9): 
        max_questions = 9 
    else: 
        max_questions = len(question_titles) 

    while(True):

        questions =[
            {
                'type': 'rawlist',
                'name': 'Results',
                'message': 'Results',
                'choices': question_titles[:max_questions]
            },
        ]

        selection = prompt(questions)

        question_url = question_url_first + str(question_dictionary[selection['Results']]) + question_url_second

        #Make the response into JSON format
        question_json = make_request(question_url)

        if(question_json['items'][0]['is_answered']):
            print("\n" + html2text.html2text(question_json['items'][0]['body']))

            answer_url = answer_url_first + str(question_json['items'][0]['question_id']) + answer_url_second

            #Make the response into JSON format
            answer_json = make_request(answer_url)

            print("<===================================================================>")

            print("ANSWER:\n")

            #print(json.dumps(answer_json, indent=4, sort_keys=True))
            print(html2text.html2text(answer_json['items'][0]['body']))

        else:
            print('Not answered')

        back_confirmation =[
            {
                'type': 'confirm',
                'name': 'list_return',
                'message': 'Return to results?',
                'default': False
            },
        ]

        repeat_list = prompt(back_confirmation)

        if(repeat_list['list_return'] == False):
            sys.exit()

main()