from flask import Blueprint, render_template, redirect, url_for, request, flash, request, jsonify, send_from_directory, session
from .models import Post, db
from .forms import PostForm
from werkzeug.utils import secure_filename
import os

views = Blueprint('views', __name__)

@views.route('/static/images/<path:filename>')
def get_image(filename):
    #return send_from_directory(os.path.join(os.getcwd(), 'static/app/static/images'), filename)
    return send_from_directory(os.path.join(os.getcwd(), 'app/static/images'), filename)

@views.route('/')
def home():
    posts = Post.query.all()
    posts.reverse()
    return render_template('index.html', posts=posts)

@views.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        code = request.form['code']
        print(code)
        if code == '1234':
            session['admin_logged_in'] = True
            return redirect(url_for('views.admin_dashboard'))
        else:
            flash('Incorrect code. Please try again.', 'danger')
            print("WRONG")
            return redirect(url_for('views.admin_login'))
    return render_template('admin_login.html')

@views.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.home'))

@views.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        flash('Please log in as admin first.', 'danger')
        return redirect(url_for('views.admin_login'))
    
    return render_template('admin_dashboard.html')

@views.route('/delete_post')
def delete_post():
    if not session.get('admin_logged_in'):
        flash('Please log in as admin first.', 'danger')
        return redirect(url_for('views.admin_login'))
    
    posts = Post.query.all()
    posts.reverse()
    return render_template('delete_post.html', posts=posts)

@views.route('handle_delete_post/<int:post_id>', methods=['POST'])
def handle_delete_post(post_id):
    if not session.get('admin_logged_in'):
        flash('Please log in as admin first.', 'danger')
        return redirect(url_for('views.admin_login'))
    
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f'Post "{post.title}" deleted successfully!', 'success')
    return redirect(url_for('views.home'))

@views.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if not session.get('admin_logged_in'):
        flash('Please log in as admin first.', 'danger')
        return redirect(url_for('views.admin_login'))
    
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        date = form.date.data
        content_html = request.form['content']
        content_html = content_html.replace('src="static/images/', 'src="/static/images/')
        image_file = form.image_file.data
        
        if image_file:
            filename = secure_filename(image_file.filename)
            #file_path = os.path.join(os.getcwd(), 'static/app/static/images', filename)
            file_path = os.path.join(os.getcwd(), 'app/static/images', filename)
            image_file.save(file_path)
        else:
            filename = 'default.jpg' #default image if none uploaded
        
        post = Post(title=title, date=date, content_html=content_html, image_file=filename)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created.', 'success')
        return redirect(url_for('views.home'))
    return render_template('new_post.html', title='New Post', form=form)

@views.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        #WHEN DEPLOYED USE THIS INSTEAD !!!
        #filepath = os.path.join('/home/nathanaelaou/mysite/app/static/images', filename)
        filepath = os.path.join(os.getcwd(), 'app/static/images', filename)
        file.save(filepath)
        # Return the URL of the uploaded image
        print(url_for('static', filename='images/' + filename, _external=False))
        return jsonify({'location': url_for('static', filename='images/' + filename)}), 201
    return jsonify({'error': 'Failed to upload image'}), 500