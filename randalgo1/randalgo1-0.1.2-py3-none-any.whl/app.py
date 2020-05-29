import html
import json
import urllib.request


def generate_answers(quest, QuestionType):
    answers = []
    if QuestionType == "multiple":
        answers = [
            quest["correct_answer"],
            quest["incorrect_answers"][0],
            quest["incorrect_answers"][1],
            quest["incorrect_answers"][2]
        ]
        answers.sort()
    elif QuestionType == "boolean":
        answers = ["True", "False"]
    else:
        print("Unrecognized question type: " + QuestionType)
    return answers


def generate_questions(n, TOKEN, TOPIC, DIFFICULTY):
    QuestionURL = "https://opentdb.com/api.php?amount=" + \
        str(n) + "&token=" + TOKEN + TOPIC + DIFFICULTY

    with urllib.request.urlopen(QuestionURL) as url:
        data = json.loads(url.read().decode())
    return data


n = 10
TokenURL = "https://opentdb.com/api_token.php?command=request"

with urllib.request.urlopen(TokenURL) as url:
    data = json.loads(url.read().decode())
    TOKEN = data["token"]

TopicURL = "https://opentdb.com/api_category.php"

with urllib.request.urlopen(TopicURL) as url:
    data = json.loads(url.read().decode())
    cat = data["trivia_categories"]

loopMenu = True

while loopMenu:
    players = input("How many players? ")
    if players == "":
        players = "1"
    if (players.isalpha() == True or int(players) < 0):
        print("Not valid answer")
    else:
        players = int(players)
        print("0. All")
        for i in range(1, len(cat) + 1):
            print(str(i) + ". " + cat[i-1]["name"])

        TOPIC = ""
        DIFFICULTY = ""
        loop = True
        while loop:
            sel = input("Choose category: ")
            if sel == "":
                sel = "0"
            if (sel.isalpha() == True or int(sel) not in range(len(cat) + 1)):
                print("Not valid answer")
            else:
                if (sel != "0" and sel != ""):
                    TOPIC = "&category=" + str(cat[int(sel) - 1]["id"])
                loop = False

        print("1. Easy\n2. Medium\n3. Hard\n4. All")
        loop = True
        while loop:
            sel = input("Choose difficulty: ")
            if sel == "":
                sel = "0"
            if (sel.isalpha() == True or int(sel) not in range(5)):
                print("Not valid answer")
            else:
                if (sel == "1"):
                    DIFFICULTY = "&difficulty=easy"
                elif (sel == "2"):
                    DIFFICULTY = "&difficulty=medium"
                elif (sel == "3"):
                    DIFFICULTY = "&difficulty=hard"
                loop = False

        questions = []
        points = []

        for pl in range(players):
            questions.append(generate_questions(n, TOKEN, TOPIC, DIFFICULTY))
            points.append(0)

        for i in range(n):
            for pl in range(players):
                if players == 1:
                    x = input("It's your turn")
                else:
                    x = input("Player " + str(pl + 1) + ", it's your turn")
                loop = True
                quest = questions[pl]["results"][i]
                QuestionType = quest["type"]
                print("Question number " + str(i + 1))
                if (TOPIC == ""):
                    print("Category: " + quest["category"])
                if (DIFFICULTY == ""):
                    print("Difficulty: " + quest["difficulty"])
                print(html.unescape(quest["question"]))

                answers = generate_answers(quest, QuestionType)
                for k in range(len(answers)):
                    print(str(k + 1) + ". " + html.unescape(answers[k]))
                while (loop):
                    answer = input("Choice: ")
                    if (answer == ""):
                        answer = "0"
                    if (answer.isalpha() == True or int(answer) not in range(len(answers) + 1)):
                        print("Not valid answer")
                    elif (answers[int(answer) - 1] == quest["correct_answer"]):
                        print("Correct!")
                        points[pl] += 1
                        loop = False
                    else:
                        if (answer != "0"):
                            print("Wrong!")
                        print("The correct answer is " +
                              html.unescape(quest["correct_answer"]))
                        loop = False

        for pl in range(players):
            print("Points player " + str(pl + 1) + ": " + str(points[pl]))
        loopMenu = False

