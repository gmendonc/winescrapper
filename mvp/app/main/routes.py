from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app, g
from flask_login import current_user, login_required
from app import db, mongo
from app.main.forms import EditProfileForm, EmptyForm, PostForm
from app.models import User, Post, Wineset
from app.main import bp
import pandas as pd
import numpy as np


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
#@login_required
def index():
    wineset = Wineset(mongo.cx)
    data = wineset.get_formatted_dataframe()
    pruned_data = data.loc[data.lowest_price <= 200.0]
    pruned_data = pruned_data[["wine_name", "link", "country", "type", "classification", "grape", "lowest_price", "vivino_link", "vivino_score", "vivino_rating"]]
    result_clean = pruned_data.loc[(pruned_data.vivino_rating>=200) & (pruned_data.lowest_price <= 80.0) & (pruned_data.vivino_score >= pruned_data.vivino_score.mean())]
    df = result_clean.sort_values(by=['lowest_price'], ascending = True, na_position = 'last')
    resumo_df = data[['lowest_price','vivino_score']].describe()
    resumo_df.columns = ['Preço', 'Avaliação']
    resumo_df.style.format({'Avaliação': "{:.2}"})
    return render_template('index.html',df=df, resumo_df=resumo_df)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page,current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/table')
def show_table():
    #df = pd.DataFrame(np.random.randn(100, 4), columns=list('ABCD'))
    winedb = Winedb()
    data = winedb.get_dataframe()
    result_clean = data.loc[(data.vivino_rating>=100) & (data.lowest_price <= 100.0) & (data.vivino_score >= 3.7)]
    df = result_clean.sort_values(by=['lowest_price', 'vivino_score'], ascending = True, na_position = 'last')
    #table = df.to_html()

    return render_template('tables.html',df=df)

