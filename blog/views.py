from blog import app
from models import Post
from decorators import login_required
from flask import render_template, flash, url_for, redirect,request
from google.appengine.api import users
from wtforms import Form, BooleanField, StringField, TextField, PasswordField, TextAreaField, validators
import logging
from markdown2 import Markdown

class PostForm(Form):
    title = StringField('Title', [validators.Required()])
    content = TextAreaField('Content', [validators.Required()])

class PostData:
    def __init__(self, url, title, content):
        self.url = url
        self.title = title
        self.content = content

@app.route('/')
def redirect_to_home():
    return redirect(url_for('list_posts'))

@app.route('/me')
def show_profile():
    return render_template('srt-resume.html')

@app.route('/posts/<posttitle>')
def show_posts(posttitle):
    posts = Post.all()
    posts.filter("url =", posttitle)
    return render_template('list_posts.html', posts=posts)

@app.route('/posts')
def list_posts():
    posts = Post.all()
    posts.order('-when')
    post_data = []
    for q in posts:
        if len(q.content) > 2000:
            content = q.content[:2000]
            content = content + "....<p>" + "<a href=/posts/" + q.url + ">read more </a>"
        else:
            content = q.content
        curr = PostData(q.url, q.title,content)
        post_data.append(curr)
    return render_template('list_posts.html', posts=post_data)

@app.route('/posts/new', methods = ['GET'])
@login_required
def new_post():
    if not users.is_current_user_admin():
        return redirect(url_for('list_posts'))
    form = PostForm(request.form)
    logging.info('/posts/new/GET')
    return render_template('markdownEditor.html', form=form)

@app.route('/posts/new', methods = ['POST'])
def addNewPosts():
    if not users.is_current_user_admin():
        return redirect(url_for('list_posts'))
    form = PostForm(request.form)
    if form.validate():
        mdConverter = Markdown()
        pt = form.title.data
        p_url = pt.replace(" ","-")
        post = Post(title = pt,
                    content = mdConverter.convert(form.content.data),
                    author = users.get_current_user(),
                    url = p_url)

        logging.info( "%s %s %s %s" %(post.title, post.content, post.author, post.url )) 
          
        post.put()
        return redirect(url_for('list_posts'))
    else:
        return render_template('new_post.html', form=form)