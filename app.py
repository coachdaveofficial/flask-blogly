"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, PostTag, Tag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)




with app.app_context():
    connect_db(app)

    db.create_all()

@app.route('/')
def list_users():
    """List users"""

    users = User.query.all()
    
    return render_template("user_list.html", users=users)

@app.route('/users/<int:user_id>/details/')
def user_details(user_id):
    '''Show user details'''
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id = user.id).all()

    return render_template('user_details.html', user=user, posts=posts)

@app.route('/users/new/', methods=['POST', 'GET'])
def create_user():
    """Show form to create user"""
    if request.method == 'GET':
        return render_template('create_user.html')
    elif request.method == 'POST':

        first_name = request.form['first_name']
        last_name= request.form['last_name']
        image_source = request.form['image_source']


        user = User(first_name=first_name, last_name=last_name, image_url=image_source)
        db.session.add(user)
        db.session.commit()

        return redirect('/')

@app.route('/users/<int:user_id>/post/', methods=['POST', 'GET'])
def add_post(user_id):
    """Add post for specific user"""

    user = User.query.get_or_404(user_id)
    tag_options = Tag.query.all()

    if request.method == 'GET':
        return render_template('add_post.html', user=user, tags=tag_options)
    elif request.method == 'POST':

        title = request.form['title']
        content = request.form['content']
        tags = request.form.getlist('tag')


        post = Post(title=title, content=content, user_id=user_id)
        
        for tagname in tags:
            tag = Tag.query.filter_by(name=tagname).one()
            post.tags.append(tag)

        db.session.add(post)
        db.session.commit()

        return redirect(f'/users/{user_id}/details')

@app.route('/users/<int:user_id>/delete/')
def delete_user(user_id):
    '''Delete user from database then return to home page'''


    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')

@app.route('/users/<int:user_id>/edit/')
def edit_user(user_id):


    user = User.query.get_or_404(user_id)


    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit/submit/')
def submit_user_changes(user_id):

    user = User.query.get_or_404(user_id)

    user.first_name = request.args['first_name'] if request.args['first_name'] != '' else user.first_name
    user.last_name = request.args['last_name'] if request.args['last_name'] != '' else user.last_name
    user.image_url = request.args['image_source'] if request.args['image_source'] != '' else user.image_url

    db.session.add(user)
    db.session.commit()

    
    return redirect(f'/users/{user.id}/details')
    

@app.route('/post/<int:post_id>/')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.filter_by(id=post.user_id).first()

    return render_template('show_post.html', post=post, user=user)

@app.route('/post/<int:post_id>/delete/')
def delete_post(post_id):
    '''Delete post from database then return to user details page'''


    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}/details')

@app.route('/post/<int:post_id>/edit/', methods=['GET', 'POST'])
def edit_post(post_id):

    if request.method == 'GET':

        post = Post.query.get_or_404(post_id)
        tags = Tag.query.all()

        return render_template('edit_post.html', post=post, tags=tags)
    
    elif request.method == 'POST':

        post = Post.query.get_or_404(post_id)
        for tag in post.tags:
            print(tag.name)


        post.title = request.form['title'] if request.form['title'] != '' else post.title
        post.content = request.form['content'] if request.form['content'] != '' else post.content
        tag_ids = [int(num) for num in request.form.getlist("tags")]
        post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

        db.session.add(post)
        db.session.commit()

        
        return redirect(f'/post/{post.id}')


@app.route('/post/<int:post_id>/edit/submit/')
def submit_post_changes(post_id):

    post = Post.query.get_or_404(post_id)
    for tag in post.tags:
        print(tag.name)
    post.title = request.args['title'] if request.args['title'] != '' else post.title
    post.content = request.args['content'] if request.args['content'] != '' else post.content
    post.tags = request.form.getlist('tag') if request.form.getlist('tag') != [] else post.tags


    db.session.add(post)
    db.session.commit()

    
    return redirect(f'/post/{post.id}')

@app.route('/tags/')
def show_tags():
    tags = Tag.query.all()

    return render_template('show_tags.html', tags=tags)

@app.route('/tags/<int:tag_id>/')
def tag_details(tag_id):
    tag = Tag.query.get_or_404(tag_id)



    return render_template('tag_details.html', tag=tag)

@app.route('/tags/new/', methods=['POST', 'GET'])
def add_tag():
    if request.method == 'GET':
        return render_template('add_tag.html')
    elif request.method == 'POST':
        name = request.form['name']
        
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()

        return redirect(f'/tags/')

@app.route('/tags/<int:tag_id>/edit/', methods=['POST', 'GET'])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    if request.method == 'GET':
        return render_template('edit_tag.html', tag=tag)
    elif request.method == 'POST':
        name = request.form['name']
        
        tag.name = name
        db.session.add(tag)
        db.session.commit()

        return redirect(f'/tags/')

@app.route('/tags/<int:tag_id>/delete/')
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect(f'/tags/')