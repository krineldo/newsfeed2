import json

from flask import Flask, render_template, request, url_for, redirect, session
from pymongo import MongoClient
import bcrypt
from bson.json_util import dumps
from datetime import datetime
from geopy.geocoders import Nominatim

app = Flask(__name__)
app.secret_key = "testing"


def MongoDB():
    myclient = MongoClient('localhost', 27017)
    mydb = myclient["newdb"]
    return mydb


client = MongoDB()


def users(mydb):
    users_coll = mydb["users"]
    # world_cup = mydb["world_cup"]
    # covid = mydb["covid"]
    # bitcoin = mydb["bitcoin"]
    # war = mydb["war"]
    # nba = mydb["nba"]
    # python = mydb["python"]
    # ps5 = mydb["ps5"]
    # f1 = mydb["f1"]
    # sources = mydb["sources"]
    pwd = 'admin1234'
    has = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
    user_found = users_coll.find_one({'name': 'admin'})
    if user_found is None:
        ad = {'name': 'admin', 'email': 'admin@admin.com', 'password': has}
        x = users_coll.insert_one(ad)
    # ad = {'name': 'admin', 'email': 'admin@admin.com', 'password': has}
    # x = users_coll.insert_one(ad)
    print("i have created everything")
    for coll in mydb.list_collection_names():
        print(coll)
    return users_coll


users_coll = users(client)
# routes

@app.route("/", methods=['post', 'get'])
def index():
    print("i am inside the routing")
    message = ''
    # if method post in index
    if request.method == 'POST':
        if request.form.get('sign_up') == "push1":
            # return render_template('register.html')
            return redirect(url_for("register"))
        elif request.form.get('login') == "push2":
            return redirect(url_for("login"))
        else:
            return redirect(url_for("logout"))
    elif request.method == 'GET':
        return render_template('index.html')
    return render_template('index.html')


@app.route("/admin", methods=['post', 'get'])
def admin():
    try:
        mydoc = users_coll.find({"name": {"$ne": "admin"}}, {"_id": False, "email": 1, "name": 1, "keywords": 1,
                                                             "location": 1})
        return render_template("admin.html", tasks=mydoc)
    except Exception as e:
        return dumps({'error': str(e)})


@app.route("/admin/<string:user_name>", methods=['post', 'get'])
def delete(user_name):
    print(users_coll.find_one({"name": user_name}))
    users_coll.delete_one({"name": user_name})
    mydoc = users_coll.find({"name": {"$ne": "admin"}}, {"_id": False, "email": 1, "name": 1,
                                                         "keywords": 1, "location": 1})
    return render_template("admin.html", tasks=mydoc)


@app.route("/register", methods=['post', 'get'])
def register():
    if "email" in session:
        return redirect(url_for("home", email=session["email"]))

    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        loc = Nominatim(user_agent="GetLoc")
        getloc = loc.geocode(request.form.getlist('location'))
        # getloc = json.dumps(loc.geocode(request.form.getlist('location')).address)
        keywords = request.form.getlist('keyword')
        # if found in database showcase that it's found
        user_found = users_coll.find_one({"name": user})
        email_found = users_coll.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('register.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('register.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('register.html', message=message)
        else:
            # hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            time_stamp = datetime.now().timestamp()
            date_time = datetime.fromtimestamp(time_stamp)
            #str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")
            # assing them in a dictionary in key value pairs
            user_input = {'name': user, 'email': email, 'password': hashed, 'keywords': keywords,
                          'location': getloc.address, 'timestamp': date_time}
            # insert it in the record collection
            users_coll.insert_one(user_input)

            # find the new created account and its email
            user_data = users_coll.find_one({"email": email})
            new_email = user_data['email']
            new_keywords = user_data['keywords']
            # if registered redirect to logged in as the registered user
            return render_template('home.html', email=new_email, keywords=new_keywords)
    return render_template('register.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("home", email=session["email"]))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # check if email exists in database
        email_found = users_coll.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            # encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                if session["email"] == "admin@admin.com" and password == "admin1234":
                    return redirect(url_for("admin"))
                return redirect(url_for('home', email=session["email"]))
            else:
                if "email" in session:
                    return redirect(url_for("home", email=session["email"]))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)


@app.route('/home/<string:email>')
def home(email):
    email_found = users_coll.find_one({"email": email})
    if email_found:
        keywords = email_found.get("keywords")
        print(keywords)
        return render_template('home.html', email=email, keywords=keywords)
    return render_template('home.html', email=email)
    # if "email" in session:
    #     email = session["email"]
    #     return render_template('home.html', email=email)
    # else:
    #     return redirect(url_for("login"))


@app.route('/home/<string:email>/update', methods=["POST", "GET", "UPDATE"])
def update(email):
    email_found = users_coll.find_one({"email": email})
    if email_found:
        keywords = request.form.getlist('keyword')
        users_coll.update_one({"email": email}, {"$set": {"keywords": keywords}})
    return render_template('update.html')

@app.route('/home/<string:email>/<string:keyword>', methods=["POST", "GET"])
def view(email, keyword):
    articles_coll = client[keyword]
    
    try:
        articles_doc = articles_coll.find({},{"title":1, "description":1,"url":1, "source":1}).sort("source", 1)
        #articles_doc = articles_coll.find({},{"title":1, "description":1,"url":1, {$group: {"source":1}}}).sort({"name":1})
        # articles_doc = articles_coll.group({
        #     key: {"title":1, "description":1,"url":1, "source":1},
            
        # })
        #print(articles_coll[0])
        #
        # for article in articles_doc:
        #     # print(article, "\n\n")
        #     print(type(article))
        #     var = article.get(['_id'])
        #     print(len(var))
        return render_template("articles.html", tasks=articles_doc, email=email, keyword=keyword)
    except Exception as e:
        return dumps({'error': str(e)})

@app.route('/home/<string:email>/<string:keyword>/<string:wiki>', methods=["POST", "GET"])
def wiki(email,keyword,wiki):
    sources_coll = client["sources"]
    
    sources_doc = sources_coll.find_one({ "title.title": wiki},{"_id":False, 'title.extract':1}) #where title == wiki
    # for x in sources_doc:
    #     print(x)
    return render_template("wiki.html", tasks=sources_doc)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')


# main
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)