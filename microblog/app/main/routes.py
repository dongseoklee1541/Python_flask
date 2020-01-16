from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_babel import _, get_locale
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, PostForm, SearchForm
from app.models import User, Post
from app.translate import translate
from guess_language import guess_language
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
        """
        flask.g : provided by Flask is a place where the application
        can store data that needs to persist through the life of a request.
        """
    g.locale = str(get_locale())

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user,
                    language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Home'), form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/explore')
@login_required
def explore():
	page = request.args.get('page',1,type=int)
	posts = Post.query.order_by(Post.timestamp.desc()).paginate(
	page,current_app.config['POSTS_PER_PAGE'],False)
	next_url = url_for('main.explore',page=posts.next_num)\
		if posts.has_next else None
	prev_url = url_for('main.explore',page=posts.prev_num)\
		if posts.has_prev else None
	# references index page, 그러나 form을 사용하지 않음
	return render_template('index.html', title = _('Explore'), posts=posts.items,
	next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>') # <and> : dynamic component
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	# first_or_404 : 결과가 없을 경우 404 오류를 반환
	page = request.args.get('page',1,type=int)
	posts = user.posts.order_by(Post.timestamp.desc()).paginate(
		page, current_app.config['POSTS_PER_PAGE'],False)
	next_url = url_for('main.user',username=user.username, page=posts.next_num)\
		if posts.has_next else None
	prev_url = url_for('main.user',username=user.username, page=posts.prev_num)\
		if posts.has_prev else None
	return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
	# submit을 post로 요청했을 경우
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
	# GET 요청했을 경우
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash(_('User %(username)s not found.', username=username))
		return redirect(url_for('main.index'))

	if user == current_user:
		flash(_('You cannot follow yourself!'))
		return redirect(url_for('main.user',username=username))

	current_user.follow(user)
	db.session.commit()
	flash(_('You are following %(username)s!',username=username))
	return redirect(url_for('main.user',username=username))

@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash(_('User %(username)s not found.', username=username))
		return redirect(url_for('main.index'))
	if user == current_user:
		flash(_('You cannot unfollow yourself!'))
		return redirect(url_for('main.user', username=username))
	current_user.unfollow(user)
	db.session.commit()
	flash(_('You are not following %(username)s.', username=username))
	return redirect(url_for('main.user', username=username))

@bp.route('/translate', methods=['POST'])
@login_required
def translate_text(): #jsonify : converts the dict to a JSON
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})


"""
form.validate_on_submit(): to check if the form submission was valid.
그러나 위의 방식은 POST 일때만 가능하다. 그래서 데이터 submit 방식을 확인하지 않는 메서드인
form.validate() 를 사용한다. if the validation fails, it is because the user
submitted an empty search form, that case I just redirect to the explore page.
"""
@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                                current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts,
                            next_url=next_url, prev_url=prev_url)