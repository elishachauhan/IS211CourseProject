#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A small docstring for IS 211 Course Project."""

from flask import Flask
from flask import session
from flask import redirect
from flask import request
from flask import render_template
import sqlite3
import time
import re


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
DATABASE = 'musicblog.db'


class Post:
    def __init__(self, title, date, author, post, id, last_update,
                 is_published, category):
        self.title = title
        self.date = date
        self.author = author
        self.post = post
        self.id = id
        self.last_update = last_update
        self.is_published = is_published
        self.category = category


def logged_in():
    if 'username' in session:
        return True
    else:
        return False


def generate_list_of_posts(selection=""):

    list_of_posts = []
    conn = sqlite3.connect(DATABASE)

    if selection == "":
        post_list = conn.execute("SELECT * FROM Posts WHERE is_published"
                                 " = 'YES' ORDER BY id DESC").fetchall()
    else:
        post_list = conn.execute("SELECT * FROM Posts WHERE username = '%s'"
                                 " ORDER BY id DESC" % selection).fetchall()

    for post in post_list:
        input_id = post[0]
        input_title = post[1]
        input_username = post[2]
        input_date = post[3]
        input_last_update = post[4]
        input_post = post[5]
        input_is_published = post[6]
        input_category = post[7]

        list_of_posts.append(Post(input_title, input_date, input_username,
                                  input_post, input_id, input_last_update,
                                  input_is_published, input_category))
    conn.commit()
    conn.close()

    return list_of_posts


def rtemplate(page, message=""):
    if logged_in():
        if page == 'index.html':
            list_of_posts = generate_list_of_posts()
        else:
            list_of_posts = generate_list_of_posts(session['username'])
        username = session['username']
    else:
        list_of_posts = generate_list_of_posts()
        username = "Not Logged In"

    has_posts = True
    if len(list_of_posts) == 0:
        has_posts = False

    return render_template(page, username=username, has_posts=has_posts,
                           logged_in=logged_in(), status_message=message,
                           list_of_posts=list_of_posts)


@app.route('/')
def index():
    
    return rtemplate('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if logged_in():
        return rtemplate('dashboard.html', "ERROR: You are already logged in.")

    status_message = ""
    credentials_filled = 'username' in request.form and \
                         'password' in request.form

    if credentials_filled:
        conn = sqlite3.connect(DATABASE)

        c = conn.execute('''SELECT password
                            FROM Users
                            WHERE username = '%s' '''
                         % request.form['username'])
        correct_password_intermediate = c.fetchone()
        correct_credentials = False
        if correct_password_intermediate != None:
            correct_password = correct_password_intermediate[0]
            correct_credentials = c != None and \
                                  request.form['password'] == correct_password

    if credentials_filled and correct_credentials:
        session['username'] = request.form['username']
        return redirect('/dashboard')
    elif credentials_filled and not correct_credentials:
        status_message = "ERROR: No password matches that username."
    elif not credentials_filled:
        status_message = ""

    return rtemplate('login.html', status_message)


@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if not logged_in():
        status_message = "ERROR: You must be logged in to access the " \
                         "dashboard!"
        return rtemplate('login.html', status_message)

    return rtemplate('dashboard.html')


@app.route('/post', methods=['GET','POST'])
def post():
    if not logged_in():
        return rtemplate('login.html', "ERROR: You must be logged in to post.")

    if len(request.form) == 0:
        return rtemplate('dashboard.html', "ERROR: You must post from the "
                                           "dashboard.")

    title = request.form['title']
    username = request.form['username']
    post = request.form['post']
    category = request.form['category']

    refined_title = re.sub("[']", "''", title)
    refined_post = re.sub("[']", "''", post)
    refined_category = re.sub("[']", "''", category)

    pattern = "[^\s]+"
    
    if re.search(pattern, refined_title) and \
            re.search(pattern, refined_category) and \
            re.search(pattern, refined_post):
        conn = sqlite3.connect(DATABASE)

        now = time.strftime('%H:%M%p %Z on %b %d, %Y')
        yes_published = "YES"

        add_statement = '''INSERT INTO Posts
                           (id, title, username, date, is_published, post,
                           category)
                           VALUES
                           (NULL, '%s', '%s', '%s', '%s', '%s', '%s')''' % \
                            (refined_title, username, now, yes_published,
                             refined_post, category)

        conn.execute(add_statement)
        conn.commit()
        conn.close()

        status_message = "Successfully posted!"
    else:
        status_message = "ERROR: You must enter a valid title, category, and" \
                         " post. Entry was not posted."

    return rtemplate('dashboard.html', status_message)


@app.route('/delete', methods=['GET','POST'])
def delete():
    if not logged_in():
        return rtemplate('login.html', "ERROR: You must be logged in to delete"
                                       " posts!")

    if len(request.form) == 0:
        return rtemplate('dashboard.html', "ERROR: You must delete from the "
                                           "dashboard.")

    conn = sqlite3.connect(DATABASE)
    conn.execute('''DELETE FROM Posts WHERE id = %s''' % request.form['id'])
    conn.commit()
    conn.close()

    return rtemplate('dashboard.html', "Successfully deleted!")


@app.route('/edit', methods=['GET','POST'])
def edit():
    if not logged_in():
        return rtemplate('login.html', "ERROR: You must be logged in to edit "
                                       "posts.")

    if len(request.form) == 0:
        return rtemplate('dashboard.html', "ERROR: You must edit from the "
                                           "dashboard.")

    if 'still_needs_input' in request.form:
        conn = sqlite3.connect(DATABASE)
        c = conn.execute('''SELECT * FROM Posts WHERE id = %s'''
                         % request.form['id']).fetchone()
        conn.commit()
        conn.close()

        id = c[0]
        title = c[1]
        post = c[5]
        category = c[7]
        return render_template('edit.html', title=title, id=id, post=post,
                               category=category,
                               username=session['username'],
                               logged_in=logged_in())

    title = request.form['title']
    id = request.form['id']
    post = request.form['post']
    category = request.form['category']

    refined_title = re.sub("[']", "''", title)
    refined_post = re.sub("[']", "''", post)
    refined_category = re.sub("[']", "''", category)

    pattern = "[^\s]+"
    
    if re.search(pattern, refined_title) \
            and re.search(pattern, refined_category) \
            and re.search(pattern, refined_post):
        conn = sqlite3.connect(DATABASE)

        now = time.strftime('%H:%M%p %Z on %b %d, %Y')

        conn.execute('''UPDATE Posts
                        SET title='%s', post='%s', last_update='%s',
                        category='%s'
                        WHERE id=%s''' % (refined_title, refined_post,
                                          now, refined_category, id))
        conn.commit()
        conn.close()
        status_message = "Successfully edited!"
    else:
        status_message = "ERROR: You must enter a valid title, category, " \
                         "and post! Entry was not posted."

    return rtemplate('dashboard.html', status_message)


@app.route('/publish', methods=['GET','POST'])
def publish():
    if not logged_in():
        return rtemplate('login.html', "ERROR: Only logged in users can "
                                       "publish posts.")

    if len(request.form) == 0:
        return rtemplate('dashboard.html', "ERROR: You must publish from the "
                                           "dashboard.")

    id = request.form['id']

    conn = sqlite3.connect(DATABASE)
    conn.execute('''UPDATE Posts
                    SET is_published='YES'
                    WHERE id='%s';''' % (id))
    conn.commit()
    conn.close()

    return rtemplate('dashboard.html', "Successfully published!")


@app.route('/unpublish', methods=['GET','POST'])
def unpublish():
    if not logged_in():
        return rtemplate('login.html', "ERROR: Only logged in users can "
                                       "unpublish posts.")

    if len(request.form) == 0:
        return rtemplate('dashboard.html', "ERROR: You must unpublish from the"
                                           " dashboard.")

    id = request.form['id']

    conn = sqlite3.connect(DATABASE)
    conn.execute('''UPDATE Posts
                    SET is_published='NO'
                    WHERE id='%s';''' % (id))
    conn.commit()
    conn.close()

    return rtemplate('dashboard.html', "Successfully unpublished!")


@app.route('/blogpost/<id>', methods=['GET','POST'])
def blogpost(id):

    conn = sqlite3.connect(DATABASE)
    c = conn.execute('''SELECT * FROM Posts WHERE id = '%s';''' % id)
    post_contents = c.fetchone()

    username_current = "Not logged in"
    if logged_in():
        username_current = session['username']

    if post_contents is None:
        return render_template('no_post.html', logged_in=logged_in(),
                               username=username_current)

    id = post_contents[0]
    title = post_contents[1]
    username = post_contents[2]
    date = post_contents[3]
    last_updated = post_contents[4]
    post = post_contents[5]
    is_published = post_contents[6]
    category = post_contents[7]

    post_shown = Post(title, date, username, post, id, last_updated,
                      is_published, category)
    list_of_posts = [post_shown]

    return render_template('specific_posts.html', list_of_posts=list_of_posts,
                           logged_in=logged_in(), username=username_current,
                           purpose="blogpost")


@app.route('/category/<category>', methods=['GET','POST'])
def category(category):

    conn = sqlite3.connect(DATABASE)
    c = conn.execute('''SELECT *
                        FROM Posts
                        WHERE category='%s' AND is_published='YES'
                        ORDER BY id DESC;''' % category)
    list_of_posts = []

    username_current = "Not logged in"
    if logged_in():
        username_current = session['username']

    for post in c.fetchall():
        input_id = post[0]
        input_title = post[1]
        input_username = post[2]
        input_date = post[3]
        input_last_updated = post[4]
        input_post = post[5]
        input_is_published = post[6]
        input_category = post[7]

        list_of_posts.append(Post(input_title, input_date, input_username,
                                  input_post, input_id, input_last_updated,
                                  input_is_published, input_category))

    if len(list_of_posts) == 0:
        return render_template('no_post.html', logged_in=logged_in(),
                               username=username_current)

    return render_template('specific_posts.html', list_of_posts=list_of_posts,
                           logged_in=logged_in(), username=username_current,
                           purpose="category", category=category)


@app.route('/logout')
def logout():
    if not logged_in():
        return rtemplate('login.html', "ERROR: You are not logged in!")

    session.pop('username', None)
    return redirect('/')


if __name__ == "__main__":
    app.run()
