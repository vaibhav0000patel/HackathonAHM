import sqlite_data as sd

while(True):
    print "Bot: Hey, do you want to start the game?"
    ans = raw_input("You: ")
    if(ans.lower()=="yes"):
        score = 0
        print "Bot: Cool, Here we go."
        print "Here is your first question."
        print ""
        
        
        while(ans!="end"):
            sq_data = sd.main_def()
            #print sq_data
            _,question, opt1, opt2, opt3, opt4, correct_answer = [i for i in sq_data[0]]
            print "Question :",question
            print "A :",opt1
            print "B :",opt2
            print "C :",opt3
            print "D :",opt4
            print ""
            ans = raw_input("Your answer : ")
            if(ans.lower()==correct_answer.lower()):
                score = score + 1
                print "CORRECT! Your score:",score
                print ""
                print "**Next Question**"
                print ""
            else:
                print "WRONG! \""+correct_answer+"\" is the correct answer."
                print "your score:",score
                print ""
                print "**Next Question**"
                print ""
    elif(ans.lower()=="no"):
        print "bye!"
        exit(0)
    else:
        print "YES or NO"
