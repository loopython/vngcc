from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login, admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    # Ensure unique backref name
    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')

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

    # Ensure the backref name is unique
    author: so.Mapped[User] = so.relationship(back_populates='posts')
    category: so.Mapped['Category'] = so.relationship('Category', backref='categorized_posts')

    def __repr__(self):
        return f'<Post {self.title}>'

class Category(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50), unique=True, nullable=False)

    # Ensure unique backref name
    posts: so.Mapped[so.WriteOnlyMapped['Post']] = so.relationship('Post', backref='categorized_in_category', lazy='select')

    def __repr__(self):
        return f'<Category {self.name}>'

# Admin views
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Category, db.session))