from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    content_html = db.Column(db.Text)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
