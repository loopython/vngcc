from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import admin_view, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.Mapped[so.WriteOnlyMapped['Post']] = so.relationship('Post', back_populates='author')

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(140), nullable=False)
    slug: so.Mapped[str] = so.mapped_column(sa.String(255), unique=True, nullable=False)
    body: so.Mapped[str] = so.mapped_column(sa.Text(), nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))

    admin_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('user.id', name='fk_post_user_id'), 
        index=True, 
        nullable=False
    )

    category_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('category.id', name='fk_post_category_id'), 
        index=True, 
        nullable=False
    )

    author: so.Mapped['User'] = so.relationship('User', back_populates='posts')
    category: so.Mapped['Category'] = so.relationship('Category', back_populates='posts')

    def __repr__(self):
        return f'<Post {self.title}>'


class Category(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50), unique=True, nullable=False)

    posts: so.Mapped[list['Post']] = so.relationship('Post', back_populates='category')

    def __repr__(self):
        return f'<Category {self.name}>'

# Custom admin view for Post
class PostView(ModelView):
    form_columns = ["title", "slug", "body", "author", "category"]  # Specify fields you want in the admin form

# Admin views
admin_view.add_view(PostView(Post, db.session))  # Use custom view for Post
admin_view.add_view(ModelView(User, db.session))  # Use default ModelView for User
admin_view.add_view(ModelView(Category, db.session))  # Use default ModelView for Category
