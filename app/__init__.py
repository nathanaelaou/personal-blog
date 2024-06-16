from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'banana'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/site.db'
    db.init_app(app)

    from .routes import views
    app.register_blueprint(views, url_prefix='/')

    with app.app_context():
        #db.drop_all()
        print("db created!")
        db.create_all()

    return app