from flask import Flask, render_template, g, request, session, redirect, url_for,make_response
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import os
# from flask_uploads import UploadSet,configure_uploads,IMAGES
import uuid
import os.path
import uuid
import pandas as pd
from flask import Flask, render_template,request,url_for
import numpy as np 
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import re
import pickle
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import json
import base64
import email, smtplib, ssl
from random import randint 
import googletrans
from googletrans import Translator
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pdfkit
from werkzeug import secure_filename


app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'admin_security'

#photos
# photos = UploadSet('photos',IMAGES)
# app.config['UPLOADED_PHOTOS_DEST'] = 'pictures'
# app.config['UPLOADED_PHOTOS_ALLOW'] = ['png','jpg']
# configure_uploads(app,photos)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def get_current_user():
    user_result = None

    if 'user' in session:
        user = session['user']
        db = get_db()
        user_cur = db.execute('select id, email, password from users where email = ?', [user])
        user_result = user_cur.fetchone()

    return user_result

def get_current_doctor():
    doctor_result = None

    if 'doctor' in session:
        doctor = session['doctor']
        db = get_db()
        doctor_cur = db.execute('select id, email, password from doctor where email = ?', [doctor])
        doctor_result = doctor_cur.fetchone()

    return doctor_result

@app.route('/')
def index():

    return render_template('home.html')

@app.route('/user_register', methods=['GET', 'POST'])
def user_register():
    user = get_current_user()
    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(request.form['password'], method='sha256')
        db = get_db()
        db.execute('insert into users (email,password) values (?,?)', [email, password])
        db.commit()
        session['user'] = request.form['email']
        return redirect(url_for('user_login'))

    return render_template('user_register.html')


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    user = get_current_user()

    if request.method == 'POST':
        db  = get_db()

        email = request.form['email']
        password = request.form['password']
        user_all_cur = db.execute('select id,email,password from users')
        user_all_res = user_all_cur.fetchall()
        flag=0
        for i in range(len(user_all_res)):
            if  user_all_res[i][1]==  email:
                flag=1
                break
            else:
                continue
        if flag==1:
            user_cur = db.execute('select id,email,password from users where email = ?',[email])
            user_result = user_cur.fetchone()
        else:
            return "<h2>Email does not exist</h2>"

        if check_password_hash(user_result['password'],password):
            session['user'] = user_result['email']
            session['username']=email

            return redirect(url_for('ask'))
        else:
            return '<h2>Login Failed</h2>'
    return render_template('user_login.html')

@app.route('/doctor_register', methods=['GET', 'POST'])
def doctor_register():
    doctor = get_current_doctor()
    department_list=[]
    import json
    with open('result.json', 'r') as fp:
        department_json=json.load(fp)
    arr=[department_json]
    # for key,item in department_json:
    #     department_list.append([department_json.key,department_json.item])
    for i in range(len(arr)):
        for j,k in arr[i].items():
            print(str(j)+" "+str(k))
            department_list.append([j,k])

    print(department_list)
    # for i in range(38):
    #     department_list.append(data)
    if request.method == 'POST' and 'imagefile' in request.files:
        try:
            db = get_db()
            email = request.form['email']
            image =  request.files['imagefile']
            speciality = request.form['speciality']
            # save file
            filename = uuid.uuid4().hex+'.png'
            image.save(os.path.join("static/pictures", filename))
            print(image)
            password = generate_password_hash(request.form['password'], method='sha256')
            db = get_db()
            db.execute('insert into doctor (email,password,expert,speciality,image,admin) values (?,?,?,?,?,?)', [email, password,0,speciality,filename,0])
            db.commit()
            session['doctor'] = request.form['email']

            return redirect(url_for('doctor_login'))
        except Exception as e:
            print(e.__class__.__name__, e)
            return '<h1>Uplaod Failed</h1>'

    return render_template('doctor_register.html',department_list=department_list)



@app.route('/doctor_login', methods=['GET', 'POST'])
def doctor_login():
    doctor = get_current_doctor()
    if request.method == 'POST':
        db = get_db()
        email = request.form['email']
        password = request.form['password']

        doctor_all_cur = db.execute('select id,email,password,expert,admin from doctor')
        doctor_all_res = doctor_all_cur.fetchall()
        flag=0

        for i in range(len(doctor_all_res)):
            if  doctor_all_res[i][1]==  email:
                flag=1
                break
            else:
                continue
        if flag==1:
            doctor_cur = db.execute('select id,email,password,expert,admin from doctor where email = ?',[email])
            doctor_res = doctor_cur.fetchone()
        else:
            return "<h2>Email does not exist</h2>"
        
        if check_password_hash(doctor_res['password'],password) and doctor_res['email']== email and doctor_res['expert']==1:
            session['doctor'] = doctor_res['email']
            
            return redirect(url_for('unanswered'))
        else:
            return '<h2>Login Failed</h2>'

    return render_template('doctor_login.html',doctor=doctor)


@app.route('/ask',methods=['POST','GET'])
def ask():
    user = get_current_user()
    if request.method == 'POST':
        question = request.form['sym']
        translator = Translator()
        question = translator.translate(question,dest = 'en').text
        print(question)
        lis = []
        json_file_dict = pickle.load(open("department_dict.pkl","rb"))
        for department,code in json_file_dict.items():
            lis.append([code,department])

        # print(lis)
        vectorizer = pickle.load(open("vectorizer.pickle",'rb'))
        model = pickle.load(open("classifier.pickle",'rb'))
        my_prediction = -1
        final_prediction = -1
        import spacy
        nlp4=spacy.load("Department_recommend")
        doc=nlp4(question)
        li =[]
        for entity in doc.ents:
            li.append(entity.text)

        string_symptoms = ""
        for i in range(len(li)):
            string_symptoms+=li[i]
            string_symptoms+=","

        symptoms = [string_symptoms]
        vect = vectorizer.transform(symptoms).toarray()
        my_prediction = model.predict(vect)
        for i in range(len(lis)):
            if lis[i][0] == my_prediction:
                final_prediction = lis[i][1]
                break

        email = user['email']
        db = get_db()
        db.execute('insert into problem(email,problem_specification) values(?,?)',[email,question])
        db.execute('insert into consult_doctor(problem_specification) values(?)',[question])
        db.commit()
        doctors_cur = db.execute('select email,speciality,image from doctor')
        doctors_res = doctors_cur.fetchall()
        return render_template('ask.html',doctors_res=doctors_res,final_prediction=final_prediction, random=randint(1,12234234234))
    return render_template('ask.html', random=randint(1,12234234234))



@app.route('/translate',methods=['GET','POST'])
def translate():
    changed_lang = None
    if request.method == 'POST':
        translator = Translator()
        print(request.form)
        lang = request.form['code']
        print(lang)
        print(str(lang))
        #translations = translator.translate(english_entry, dest=lang)
        #changed_lang = translations.text
        #print(changed_lang)
        message = request.form['message']
        d ={
            'hello' : "Hi !! What is your age?",
            'years' : 'Let me know how are you feeling?And What are your symptoms like?',
            'suffering' : 'Do you have any Previous Prescription?',
            'symptoms' : 'Do you have any Previous Prescription?',
            'yes' : 'Then,Please upload it'

        }

        for key,pair in d.items():
            key_translations = translator.translate(key, dest=lang)

            if key_translations.text in message:
                return translator.translate(pair,dest = lang).text

        return translator.translate("Sorry!! Please Repeat", dest = lang).text

    return render_template('ask.html')

@app.route('/back_translate',methods=['GET','POST'])
def back_translate():
    user = get_current_user()
    if request.method == 'POST':
        years = request.form['years']
        symptoms = request.form['symptoms']
        translator = Translator()
        if translator.translate(years,dest='en').text == 'years':
            return translator.translate(years,dest='en').textfile
        if translator.translate(symptoms,dest = 'en').text == 'symptoms':
            return translator.translate(symptoms,dest='en').text


@app.route('/unanswered',methods=['GET','POST'])
def unanswered():
    doctor = get_current_doctor()
    db = get_db()
    query_cur = db.execute('select doc_email,user_email,problem_specification,problem_department from consult_doctor')
    query_all = query_cur.fetchall()
    unanswered_cur = db.execute('select id,email,problem_specification, problem_department from problem')
    unanswered_result = unanswered_cur.fetchall()

    return render_template('unanswered.html',unanswered_questions= unanswered_result,doctor=doctor,query_all = query_all)

@app.route('/answer',methods=['GET','POST'])
def answer():
    doctor=get_current_doctor()
    if request.method == 'POST':
        answer = request.form['javascript_content']
        print('answer='+answer)
        with open("doc_pres.txt","w") as fp:
            for x in answer:
                fp.write(x)
        print(answer)
        try:
            with open("/textfile.txt","w") as file:
                file.write(answer)
        except:
            print("not able to write")
    return render_template('answer.html',doctor=doctor,email=request.args.get('email'))

def convertImage(imgData1):
	imgstr = re.search(r'base64,(.*)', str(imgData1)).group(1)
	with open('static/output.png', 'wb') as output:
		output.write(base64.b64decode(imgstr))

@app.route('/sign', methods=['GET', 'POST'])
def sign():
  #get the image
  if request.method == 'POST':
	  imgData = request.get_data()
	  #convert the image
	  convertImage(imgData)
	 
	  return "Signature Saved"


  return render_template('sign.html')
@app.route('/nlp',methods=['GET','POST'])
def nlp():
	string_nlp=""
	with open("doc_pres.txt","r") as test_file:
		for x in test_file:
			string_nlp+=(x)

	with open("pres_file.txt","w") as fp:
		for x in string_nlp:
			fp.write(x)


	d={"Name":[],"Age":[],"Symptoms":[],"Disease":[],"Medicines":[],"Advices":[]}

	input_file=open("pres_file.txt").read()

	
	# with open('whitelist.pkl', 'rb') as f:
	#     data = pickle.load(f)

	# # %%capture cap --no-stderr
	# import spacy
	# nlp2=spacy.load('en_core_web_sm')
	# doc=nlp2(input_file)
	# string="NAME: "
	# for token in doc:
	#     if((token.tag_=="NN" or token.tag_=='NNP') and str(token).lower() not in data):
	#         d["Name"].append(token.text)
	#         break

	# import spacy
	# nlp=spacy.load("en_core_web_sm")
	# doc=nlp(input_file)
	# from spacy.matcher import PhraseMatcher
	# import random
	# age_list=[]
	# matcher = PhraseMatcher(nlp.vocab, attr="SHAPE")
	# age_indicator=['YEAR', 'YEARS', 'Y/O', 'AGES', 'AGE', 'Y.O', 'Y.O.','AGED','AGE IS']
	# matcher.add("age", None, nlp("76 year old"),nlp("aged 58"),nlp('aged 123'),nlp("54 y/o"),nlp("age is 59"),nlp("123 y/o"), nlp("ages 35"),nlp("age 45"),nlp("ages 123"),nlp("age 123"),nlp("54 years old"),nlp("124 years old"),nlp("41 y.o."),nlp("123 y.o."),nlp('113 year old'))

	# for match_id, start, end in matcher(doc):
	#     t=doc[start:end]
	#     break
	# string=""
	# for i in t.text:
	#     if((i).isdigit()):
	#         string+=str(i)
	# d["Age"].append(string)


	# nlp4=spacy.load("new_model_3")
	# doc=nlp4(input_file)
	# for entity in doc.ents:
	#     d["Symptoms"].append(entity.text)


	# nlp5=spacy.load("new_model_2")
	# doc=nlp5(input_file)
	# for entity in doc.ents:
	#     print(entity.text)


	# nlp4=spacy.load("new_model_4")
	# doc=nlp4(input_file)
	# for entity in doc.ents:
	#     d["Medicines"].append(entity.text)


	# nlp6=spacy.load("medical_Advice_model")
	# doc=nlp6(input_file)
	# for entity in doc.ents:
	#     d["Advices"].append(entity.text)


	# # for i,j in d.items():
	# #     print(i," :",j)
	# # d.clear()

	import spacy
	nlp5=spacy.load("new_model_5")
	doc=nlp5(input_file)
	for entity in doc.ents:
	    d["Name"].append(entity.text)


	import spacy
	nlp=spacy.load("en_core_web_sm")
	doc=nlp(input_file)
	print(doc)


	from spacy.matcher import PhraseMatcher
	import random
	age_list=[]
	matcher = PhraseMatcher(nlp.vocab, attr="SHAPE")
	age_indicator=['YEAR', 'YEARS', 'Y/O', 'AGES', 'AGE', 'Y.O', 'Y.O.','AGED','AGE IS']
	matcher.add("age", None, nlp("76 year old"),nlp("aged 58"),nlp('aged 123'),nlp("54 y/o"),nlp("age is 59"),nlp("123 y/o"), nlp("ages 35"),nlp("age 45"),nlp("ages 123"),nlp("age 123"),nlp("54 years old"),nlp("124 years old"),nlp("41 y.o."),nlp("123 y.o."),nlp('113 year old'))


	for match_id, start, end in matcher(doc):
	    t=doc[start:end]
	    break
	string=""
	for i in t.text:
	    if((i).isdigit()):
	        string+=str(i)
	d["Age"].append(string)

	nlp4=spacy.load("new_model_3")
	doc=nlp4(input_file)
	for entity in doc.ents:
	    d["Symptoms"].append(entity.text)


	nlp5=spacy.load("new_model_2")
	doc=nlp5(input_file)
	for entity in doc.ents:
	    d["Disease"].append(entity.text)

	nlp4=spacy.load("new_model_4")
	doc=nlp4(input_file)
	for entity in doc.ents:
	    d["Medicines"].append(entity.text)

	nlp6=spacy.load("medical_Advice_model")
	doc=nlp6(input_file)
	for entity in doc.ents:
	    d["Advices"].append(entity.text)


	for i,j in d.items():
	    print(i," :",j)


	app_json = json.dumps(d)
	print(type(d))
	print(app_json)
	# return "working"
	l=d["Symptoms"]
	str1=""
	for i in l:
		str1+=i+" "
	n=d["Name"]
	strName=""
	for i in n:
		strName+=i+" "
	age=d["Age"]
	strAge=""
	for i in age:
		strAge+=i+" "
	Disease=d["Disease"]
	strDisease=""
	for i in Disease:
		strDisease+=i+" "
	Medicine=d["Medicines"]
	strMedicine=""
	for i in Medicine:
		strMedicine+=i+" "
	Advice=d["Advices"]
	strAdvice=""
	for i in Advice:
		strAdvice+=i+" "
	

	return render_template('answer.html',tabledata=(str1),name=(strName),age=(strAge),disease=(strDisease),medicine=(strMedicine),advice=(strAdvice))

@app.route('/doctors',methods=['GET','POST'])
def doctors():
    doctor = get_current_doctor()
    if request.method == 'GET':
        db =  get_db()
        doctor_cur = db.execute('select id, email,password,expert,admin from doctor')
        doctor_results = doctor_cur.fetchall()

    return render_template('doctors.html',doctor_results=doctor_results,doctor=doctor)

@app.route('/promote/<doctor_id>')
def promote(doctor_id):
    db = get_db()
    db.execute('update doctor set expert =1 where id = ?',[doctor_id])
    db.commit()
    return redirect(url_for('doctors'))

@app.route('/consult',methods = ['GET','POST'])
def consult():
    user = get_current_user()
    if request.method == 'POST':
        print(request.form)
        doc_email = request.form['doc_email']
        symptoms = request.form['symptoms']
        print('Symptoms==='+symptoms)
        problem_department = request.form['department']
        print('doc_email:'+doc_email)
        # print('department:'+department)
        db = get_db()
        user_email = user['email']
        id_cur = db.execute(' SELECT id FROM consult_doctor ORDER BY ID DESC LIMIT 1')
        id_result = id_cur.fetchone()
        id_result_1 = int(id_result['id'])
        print(type(id_result_1) )
        stmt = f"update consult_doctor set doc_email='{doc_email}',user_email = '{user_email}',problem_department = '{problem_department}'  where id={id_result_1}"
        print(stmt)
        db.execute(stmt)
        db.commit()

        return render_template('ask.html')
    return render_template('ask.html')

@app.route('/pay',methods=['GET','POST'])
def pay():
    return  render_template('pay.html')
    

# @app.route('/recommend',methods=['GET','POST'])
# def recommend():
#     user = get_current_user()
#     if request.method == 'POST':
#         symptoms=request.form['javascript_content']
#         print(symptoms)
#         return render_template('ask')


@app.route('/genPDF')
def genPDF():
    rendered=render_template('answer.html') 
    pdf=pdfkit.from_string(rendered,False)#keep the generated pdf in the memory first
    response=make_response(pdf)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition']='attachment;filename=pres.pdf'
    return response      

@app.route('/mail',methods=['GET','POST'])
def mail():
    user = get_current_user()
    if request.method == 'POST' and 'prescription' in request.files:
        try:
            file = request.files['prescription']
            print(file)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            subject = "An email with attachment from Python"
            body = "This is an email with attachment sent from Python"
            sender_email = "sih20error404@gmail.com"
            receiver_email = request.args.get('email','')
            # password = input("Type your password and press enter:")
            password="118209@error"
            # Create a multipart message and set headers
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            message["Bcc"] = receiver_email
            # Recommended for mass emails
            # Add body to email
            message.attach(MIMEText(body, "plain"))
            filename = 'pres.pdf'
            # In same directory as script
            # Open PDF file in binary mode
            with open(filename, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                # Encode file in ASCII characters to send by email    
            encoders.encode_base64(part)
            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
                )
            # Add attachment to message and convert message to string
            message.attach(part)
            text = message.as_string()
            # Log in to server using secure context and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, text)
        except:
            "upload failed"
    return render_template('answer.html')

@app.route('/logout')
def logout():
    
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)