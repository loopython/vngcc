from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/about')
def about():
    return render_template('about.html', title='About')
@app.route('/intro')
def intro():
    return render_template('About Us/intro.html', title='Introduction to Vietnam House in GCC')
@app.route('/mission')
def mission():
    return render_template('About Us/mission.html', title='Mission Statement')
@app.route('/profile')
def profile():
    return render_template('About Us/profile.html', title='Our Profile')
@app.route('/partners')
def partners():
    return render_template('About Us/partners.html', title='Our Partners')


@app.route('/services')
def services():
    return render_template('services.html', title='Services')
@app.route('/tradepromo')
def tradepromo():
    return render_template('Services/tradepromo.html', title='Trade Promotion')
@app.route('/consulting')
def consulting():
    return render_template('Services/consulting.html', title='Consulting')
@app.route('/mice')
def mice():
    return render_template('Services/mice.html', title='MICE')

@app.route('/b2b')
def b2b():
    return render_template('b2b.html', title='B2B')
@app.route('/sbe')
def sbe():
    return render_template('B2B/sbe.html', title='Sucessful Business Events')
@app.route('/uaebe')
def uaebe():
    return render_template('B2B/uaebe.html', title='UAE Business Events')
@app.route('/sabe')
def sabe():
    return render_template('B2B/sabe.html', title='Saudi Arabia Business Events')


@app.route('/news')
def news():
    return render_template('news.html', title='News & Events')
@app.route('/latestnews')
def latestnews():
    return render_template('News & Events/latestnews.html', title='Latest news press release media coverage related to Vietnam House in GCC.')
@app.route('/upcoming')
def upcoming():
    return render_template('News & Events/upcoming.html', title='Upcoming events, seminars, and workshops.')
@app.route('/gallery')
def gallery():
    return render_template('News & Events/gallery.html', title='Gallery')


@app.route('/marketprofile')
def marketprofile():
    return render_template('marketprofile.html', title='Market Profile')
@app.route('/uae')
def uae():
    return render_template('Market Profile/uae.html', title='United Arab Emirates')
@app.route('/saudi')
def saudi():
    return render_template('Market Profile/saudi.html', title='Kingdom of Saudi Arabia')
@app.route('/oman')
def oman():
    return render_template('Market Profile/oman.html', title='Sultanate of Oman')
@app.route('/qatar')
def qatar():
    return render_template('Market Profile/qatar.html', title='State of Qatar')
@app.route('/kuwait')
def kuwait():
    return render_template('Market Profile/kuwait.html', title='State of Kuwait')
@app.route('/bahrain')
def bahrain():
    return render_template('Market Profile/bahrain.html', title='Kingdom of Bahrain')