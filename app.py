import os
import sys
import json
import cookielib,requests
from flask import Flask, request
import sqlite_data as sd

game = 0
question = ""
opt1=""
opt2=""
opt3=""
opt4=""
correct_answer = ""
score = 0

app = Flask(__name__)
ACCESS_TOKEN = "EAAbiJpTLEZBIBAMNiAIymRolqSW8HoqMlFTGg5ptPkUKyv2GIYeVo3y82Sx58WgfK1ZCESP6SoGtD23h7Cr1aXZBCBX5T44SBjr5MigfE3IyU1ofdzZB8eCzVoEXqBZC4XNOUqhPLnRsgKTuLZBlYJxI7rcKWFAhYjEWGG4MHedwZDZD"
VERIFY_TOKEN = "app_secret"


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200



def new_question():
    global question, opt1, opt2, opt3, opt4, correct_answer
    sq_data = sd.main_def()
    _,question, opt1, opt2, opt3, opt4, correct_answer = [i for i in sq_data[0]]
    question = "Question : "+question
    opt1 = "A : "+opt1
    opt2 = "B : "+opt2
    opt3 = "C : "+opt3
    opt4 = "D : "+opt4
    
    return question +"\n"+ opt1 +"\n"+ opt2 +"\n"+ opt3 +"\n"+ opt4+"  ca : "+correct_answer

@app.route('/', methods=['POST'])

def webhook():

    global question, opt1, opt2, opt3, opt4, correct_answer,score,game
    data = request.get_json()
    log(data)  #logs

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent  a message to page

                    sender_id = messaging_event["sender"]["id"]        
                    recipient_id = messaging_event["recipient"]["id"]  
                    message_text = messaging_event["message"]["text"]
                    start_game = ["let the game begin","start the game","start game","start"]

                    if(game==1):
                        
                        if(message_text.lower()=="end"):
                            send(sender_id, "Game Over!"+"\nYour final score:"+str(score))   
                            game = 0
                            score = 0
                            correct_answer = ""
                            break
                        elif(message_text.lower()==correct_answer.lower()):  #correct_answer
                            score = score+1
                            display_question= new_question()
                            send(sender_id, "CORRECT! Your score:"+str(score)+"\n**Next Question**\n\n"+display_question)
                        else:
                            temp_str1 = "WRONG! \""+correct_answer+"\" is the correct answer."+"\nYour score:"+str(score)
                            display_question= new_question()
                            send(sender_id, temp_str1+"\n\n**Next Question**\n\n"+display_question)
                        
                    elif((message_text.lower() in start_game)and(game==0)):
                        game = 1
                        display_question = new_question()
                        send(sender_id, "Cool! Here we go!!"+"\nHere is your first question.\n\n"+display_question)
                        
                        
                    else:
                        send(sender_id,"please send \"Start\" to start the game.")


                    

                if messaging_event.get("delivery"):  
                    pass

                if messaging_event.get("optin"):  
                    pass

                if messaging_event.get("postback"):  
                    pass

    return "ok", 200


def send(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

if __name__ == '__main__':
    app.run(debug=True,port=5432)
