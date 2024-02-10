from flask import Flask,request,render_template,redirect,flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "this-is-my-key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug=DebugToolbarExtension(app)


responses=[]
survey = satisfaction_survey
que_len=len(survey.questions)

@app.route("/")
def home_page():
    """ home page """
    print(f"this is {responses}")
    return render_template("homepage.html",title=survey.title, instructions=survey.instructions)

@app.route("/begin",methods=['POST'])
def start_survey():
    responses.clear();
    return redirect("/questions/0")

@app.route("/questions/<int:idx>")
def question(idx):
    if (len(responses) != idx):  
        return redirect(f"/questions/{len(responses)}")
    if(len(responses) == que_len):
        return redirect("/complete")
    if(idx > que_len or idx < 0 ):
        flash(f"no such question")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[idx]
    return render_template("questions.html",question=question.question,choices=question.choices)

@app.route("/answer",methods=['POST'])
def answer():
    answer=request.form['answer']
    responses.append(answer)
    if(len(responses) == que_len):
        # print(f"this is {responses}")
        return redirect('/complete')
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/complete")
def complete():
    return render_template("thankyou.html")




# @app.route("/question/0", methods=["POST"])
# def question0():
    
#     que0=satisfaction_survey.questions[0]
#     return render_template("question0.html",que0=que0)


# @app.route("/answer",methods=["POST"])
# def question1():
#     ans=request.form['ans']
#     responses.append(ans)

#     que1=satisfaction_survey.questions[1]
#     return render_template("question1.html",que1=que1)
    
# @app.route("/answer1",methods=["POST"])
# def question2():
#     ans=request.form['ans']
#     responses.append(ans)

#     que2=satisfaction_survey.questions[2]
#     return render_template("question2.html",que2=que2)

# @app.route("/answer2",methods=["POST"])
# def question3():
#     ans=request.form['ans']
#     responses.append(ans)

#     que3=satisfaction_survey.questions[3]
#     return render_template("question3.html",que3=que3)

# @app.route("/answer3",methods=["POST"])
# def question4():
#     ans=request.form['ans']
#     responses.append(ans)
#     print(responses)
#     # flash("Thank you")
#     return render_template("thankyou.html")
    


