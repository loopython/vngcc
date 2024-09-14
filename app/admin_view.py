from flask_admin.contrib.sqla import ModelView
from app import admin_view, db
from app.models import User, Post, Category
from flask_login import current_user
from flask import redirect, url_for

def setup_admin():
    admin_view.add_view(ModelView(Post, db.session))
    admin_view.add_view(ModelView(User, db.session))
    admin_view.add_view(ModelView(Category, db.session))
