from flask import Flask,request,render_template,redirect,flash
from flask_debugtoolbar import DebugToolbarExtension
from flask import session
from surveys import Survey,satisfaction_survey,personality_quiz,surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "this-is-my-key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug=DebugToolbarExtension(app)

# responses = session["responses"] can't be difine outside of route

@app.route('/')
def select_survey():
    """ home page """
    return render_template("surveys.html",surveys=surveys)

@app.route('/pick_a_survey')
def pick_a_survey():
    survey_key = request.args['survey']
    session['survey_key']=survey_key
    current_survey = surveys[survey_key]
    
    return render_template("homepage.html",title=current_survey.title, instructions=current_survey.instructions)

@app.route("/sessionPage",methods=['POST'])
def set_session():
    session['responses'] = []
    print("####################################")
    print(session["responses"])
    return redirect("/begin")

@app.route("/begin")
def start_survey():
    return redirect("/questions/0")

@app.route("/questions/<int:idx>")
def question(idx):
    survey_key=session['survey_key']
    current_survey=surveys[survey_key]
    responses = session['responses']
    if (len(responses) != idx):  
        flash("you are trying to access an invalid question")
        return redirect(f"/questions/{len(responses)}")

    if (len(responses) < idx):
        flash("you are trying to access an invalid question")
        return redirect(f"/questions/{len(responses)}")

    if (len(responses) == len(current_survey.questions)):
        return redirect("/complete")

    
    question = current_survey.questions[idx]
    return render_template("questions.html",question=question.question,choices=question.choices,allow_text=question.allow_text)

@app.route("/answer",methods=['POST'])
def answer():
    survey_key=session['survey_key']
    current_survey=surveys[survey_key]
    # answer=request.form['answer']
    
    responses = session["responses"]
    if len(request.form.keys())== 1:
        responses.append(request.form['answer'])
    else:
        ans=[]
        for key in request.form.keys():
            ans.append(request.form[key])
        responses.append(ans)
 
    # responses.append(answer)
    session["responses"] = responses
  
    if(len(responses) == len(current_survey.questions)):
        print(session["responses"])
        return redirect("/complete")
    else:
        print(session["responses"])
        return redirect(f"/questions/{len(responses)}")


@app.route("/complete")
def complete():
    survey_key=session['survey_key']
    current_survey=surveys[survey_key]
    responses = session["responses"]
    question_list=[]
    for question in current_survey.questions:
        question_list.append(question.question)
    new_list = list(zip(question_list,responses))
    final_list=[]
    for pair in new_list:
        str=""
        for i in pair:
            str1=""
            for x in i:
                str1+=x
            str=str+str1+" " 
        final_list.append(str);
    return render_template("complete.html",final_list=final_list)
    