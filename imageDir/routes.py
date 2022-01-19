import base64
from crypt import methods
from pickle import NONE
from flask import *
from imageDir import  app, db, bcrypt
from imageDir.models import User, imgDetails
from datetime import datetime
import random
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from base64 import b64encode
from PIL import Image
import io
import csv

@app.route('/', methods = ['GET','POST'])
def mainPage():
    return render_template('/main.html')


@app.route('/imageupload', methods = ['POST','GET'])
def imageUpload():
    if request.method == 'POST':
        return render_template('/imageupload.html')
    


@app.route('/uploadImage', methods = ['POST','GET'])
def uploadImage():
    if request.method == 'POST':
        name = request.form['usr']
        # ch = request.form['re'] 
        # if ch == "Click here to Upload image" or name == None:
        #     return('/imageupload.html')
        file = request.files['img']
        if file == " ":
            return render_template('/imageupload.html', msg = "Please Select a file first!!!!!")  
        name = secure_filename(file.filename)
        category = request.form['category']
        if category == " ":
            return render_template('/imageupload.html', msg = "Please Select a category first!!!!!")  
        if category == 'Jerseys':
            price = random.randrange(200,600,25)
        elif category == 'Shoes':
            price = random.randrange(100,300,50)
        elif category == 'Mobiles':
            price = random.randrange(1000,1500,100)
            
        discount = random.randrange(5,30,5)
        discountedPrice = price - ((discount/100) * price)
        userid = User.query.filter_by( username = name).first()
        img = imgDetails(file = file.read(), name = name, price = price, discount = discount, discounted_price =discountedPrice, category = category, private_user_id = userid)
        db.session.add(img)
        db.session.commit()
        
        return render_template('/public.html', msg = "Image Successfully Uploaded !!! ")  
    else:
        return render_template('/public.html', msg = "XX   ERROR   XX")


@app.route("/displayImg", methods= ['POST','GET'])
def displayImg():
    q = imgDetails.query.order_by(imgDetails.id).all()
    image_data = []
    price_data = []
    discount_data= []
    final_price = []
    for i in range(0, len(q)):
        file = q[i].file
        price = q[i].price
        dis = q[i].discount 
        final =q[i].discounted_price
        encoded_img_data = base64.b64encode(file)
        a = encoded_img_data.decode('utf-8')
        price_data.append(price)
        discount_data.append(dis)
        final_price.append(final)
        image_data.append(a)
    return render_template('/public.html', img_data=image_data, price_data = price_data, discount_data = discount_data, final_price = final_price)



@app.route("/categoryDisplay", methods= ['POST','GET'])
def categoryDisplay():
    q = imgDetails.query.order_by(imgDetails.id).all()
    image_data = []
    price_data = []
    discount_data= []
    final_price = []
    cat = request.form['category']
    for i in range(0,len(q)):
        if cat == q[i].category:
            file = q[i].file
            price = q[i].price
            dis = q[i].discount 
            final =q[i].discounted_price
            encoded_img_data = base64.b64encode(file)
            a = encoded_img_data.decode('utf-8')
            price_data.append(price)
            discount_data.append(dis)
            final_price.append(final)
            image_data.append(a)
    return render_template('/public.html', img_data=image_data, price_data = price_data, discount_data = discount_data, final_price = final_price)




@app.route("/login", methods =['GET','POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        user = User.query.filter_by(email = request.form['username']).first() 
        if user == None:
            return render_template('/signup.html', msg = "Please Sign-Up.. No user Found")
        if (user.email == request.form['username']) and (bcrypt.check_password_hash(user.password, request.form['password'])):
            q1 = imgDetails.query.order_by(imgDetails.id).all()
            image_data = []
            price_data = []
            discount_data= []
            final_price = []
            for i in range(0,len(q1)):
                if q1[i].private_user_id == user.id:
                    file = q1[i].file
                    price = q1[i].price
                    dis = q1[i].discount 
                    final =q1[i].discounted_price
                    encoded_img_data = base64.b64encode(file)
                    a = encoded_img_data.decode('utf-8')
                    price_data.append(price)
                    discount_data.append(dis)
                    final_price.append(final)
                    image_data.append(a)
            return render_template('/public.html', img_data=image_data, price_data = price_data, discount_data = discount_data, final_price = final_price)   
            #return render_template('/imageupload.html', usr = user.username) 
        else:
            return render_template('/login.html', msg = "Wrong Passsword Please try again !!!")  
    else:
        return render_template('/login.html')
    

@app.route("/signup", methods = ['GET','POST'])
def signup():
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form:
        password = request.form['password']
        hashPassword = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        
        user = User(username = request.form['username'], email = request.form['email'], password = hashPassword)
        db.session.add(user)
        db.session.commit()
        
        return render_template("/login.html", msg = "User successfully Created!!! now please login")
    else:
        return render_template("/signup.html", msg = "User NOT Created XXXX")