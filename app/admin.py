from app import db, admin
from app.models import Post
from flask_admin.contrib.sqla import ModelView


admin.add_view(ModelView(Post, db.session))