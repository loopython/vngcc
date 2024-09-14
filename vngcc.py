import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Post
from app.admin_view import setup_admin

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}

if __name__ == '__main__':
    app.run(debug=True)