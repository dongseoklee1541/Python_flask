from flask import render_template
from app import db
from app.errors import bp

@bp.app_errorhandler(404) # errorhandler : 에러 페이지를 변경하기 위한 데코레이터
def not_found_error(error):
	return render_template('404.html'), 400

@bp.app_errorhandler(500)
def internal_error(error):
	db.session.rollback() # rollback 처리를 통해 오류를 일으킨 db를 되돌린다.
	return render_template('500.html'), 500
