from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # global fask object
#connect to database
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://sahar:sahar@localhost/weblog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.String(600),nullable=False)
    created_at = db.Column(db.String(120), nullable=False ,default="4,july,2017")
    keywords = db.Column(db.String(120), nullable=True)
    category = db.Column(db.String(120), nullable=True)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(120), nullable=False)
    lastName = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120),nullable=False)
    posts = db.relationship('News', backref='author', lazy='dynamic')


# db.drop_all()
# db.create_all()


@app.route('/')
def index():
    # return 'home page'
    return render_template('index.html',news=News.query.order_by(News.created_at.desc()).limit(5))
@app.route('/readMore/<id>') 
def news(id):
    return render_template('news.html',single_news = News.query.get(id))
@app.route('/signinpage') 
def signin():
    # return 'signin page'
    return render_template('signin.html')
@app.route('/signuppage') 
def signup():
    # return 'signup page'
    return render_template('signup.html')
@app.route('/aboutpage') 
def about():
    # return 'about page'
    return render_template('about.html')
@app.route('/addpostpage',methods=["GET","POST"]) 
def addpost():
    if request.method == "GET":
        # return 'get'
        return render_template('addpost.html')
    else:
        title = request.form['title-post']
        category = request.form['category']
        author_id = request.form['author-post']
        created_at = request.form['created_at']
        body = request.form['post-body']
        keywords = request.form['keywords']
        db.session.add(News(title=title,body=body,created_at=created_at,category=category,keywords=keywords,author_id=author_id))
        db.session.commit();
      #  return 'post saved'
        return redirect("http://127.0.0.1:8080/", code=302)

if __name__ == '__main__':
    app.run(port=8080)


