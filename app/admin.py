from flask_admin.contrib.sqla import ModelView
from app import db, admin
from app.models import User, Post
from flask_login import current_user
from flask import redirect, url_for

# Customize the ModelViews if needed
class UserAdmin(ModelView):
    column_list = ('id', 'username', 'email')  # Customize the fields shown in the admin panel

class PostAdmin(ModelView):
    column_list = ('id', 'title', 'timestamp', 'user_id')

# Add views to the admin panel
admin.add_view(UserAdmin(User, db.session))
admin.add_view(PostAdmin(Post, db.session))
