# CH.01 Hello, World!

* FLASK_APP="app.py" : FLASK_APP은 서버를 실행할때 실행할 어플리케이션을 지정해주는 역할을 한다. 

Rendering: template(탬플릿)을 완전히 HTML로 변환하는 작업

* render_template() : 템플릿 파일 이름과 템플릿 인수의 변수 목록을 가져와 동일한 템플릿을 반환하지만 표시되는 내용은 실제 내용으로 표시

플라스크에서 템플릿을 사용할때 Jinja2 라는 엔진을 활용한다

### Jinja2의 문법

* {{ ... }} : 변수나 표현식
* {% ... %} : if나 for같은 제어문
* {# ... #} : 주석문 


# CH.03 Web Forms

* form.validate_on_submit() : GET으로 전송시 False, POST 방식으로 전송시 True로 반환된다.

* flash() : 사용자에게 메세지를 보여줄 수 있는 메서드

* get_flashed_messages() : from Flask, flash에 등록된 모든 메세지들을 반환함

* redirect() : 클라이언트 웹 브라우저에게 인수로 지정된 페이지로 자동으로 이동하게 함

```
redirect('/index') : /index 로 이동해라.
```

* url_for() : URL을 동적으로 생성하는 메서드

# CH.04 DataBase

* $flask db init : 마이그레이션 저장소(repository) 생성

* $flask db migrate : 데이터베이스를 변경하지 않고 마이그레이션 스크립트만 생성한다.(The flask db migrate command does not make any changes to the database, it just generates the migration script.) 저장소를 생성 하거나 데이터 베이스 스키마의 구조가 변경된
경우 migrate를 통해서 변경 사항을 작성해야 한다.

* $flask db upgrade : migrate를 통해 변경된 사항을 데이터베이스에 적용, MYSQL, Postgre 와 같이 DB server 작업시 실행하기 전에 데이터베이스를 DB server에 생성해야 한다. 

* $flas db downgrade : 변경 사항을 되돌리고 싶을때 사용, upgrade를 undo 한다.


# CH.05 Login

* werkzeug.security : 비밀번호를 특정 알고리즘을 통해 해쉬로 바꾸어 보안성을 높일 수 있는 패키지
  * generate_password_hash(args) : 를 통해 args을 해쉬값으로 바꾸어 반환해준다. 해쉬값은 매번 바뀌므로 해쉬값을 통해서 원래의 값을 알 수는 없다.
  * check_password_hash : 해쉬값과 비밀번호를 입력받아 같으면 True, 다르면 False 를 출력하는 메소드
```
>>> from werkzeug.security import generate_password_hash
>>> hash = generate_password_hash('foobar')
>>> hash
'pbkdf2:sha256:50000$vT9fkZM8$04dfa35c6476acf7e788a1b5b3c35e217c78dc04539d295f011f01f18cd2175f'
```
```
>>> from werkzeug.security import check_password_hash
>>> check_password_hash(hash, 'foobar')
True
>>> check_password_hash(hash, 'barfoo')
False
```

* flask-login : 로그인을 위한 플라스크 확장 라이브라리

* filter_by : 결과는 일치하는 사용자 이름을 가진 객체 만을 포함하는 쿼리다.

# CH.06 Profile Page and Avatars

#### validate_on_submit()

* True 인 경우 : browser가 POST 방식으로 request 했을때.

* False 인 경우 : 두가지 상황이 존재한다. 첫째 browser가 GET 방식으로 request 한 경우와 둘째 browser가 POST 로 requset했지만, 해당 데이터의 내용이 잘못 됐을 경우다.

# CH.07 Error Handling

* $ set FLASK_DEBUG=1 : 플라스크의 디버그 모드를 실행하는 코드, 디버그 모드가 실행되면 소스코드가 수정될때 자동으로 서버를 재시작해준다. 이 모드는
상용서버에서 사용하면 안된다. 해킹을 하고자 하는 유저들에게는 내부 소스코드를 보여주는 결과가 되어 뜻하지 않는 선물을 주게 되기 때문이다.
디버그 모드를 해제하고 싶다면, 1을 0으로 바꾸어 실행해주자.

# CH.08 Followers
* backref=db.backref('followers', lazy='dynamic'), lazy='dynamic') : db.brackref(...)은 user 테이블이 followers 테이블을 역참조 할 때
쓰인다. lazy='dynamic'의 경우 request가 있기 전에는 쿼리문을 작동하지 않는다는 의미이다. one-to-many 관계를 만드는 방법이다.

# CH.09 Pagination

* Post/Redirect/Get : 사용자가 POST 요청을 보낸 상태에서 새로고침을 누르게 된다면, 다시 POST 요청을 하여 데이터가 중복될 수 있다.(쇼핑몰 중복 구매) 이를 방지하기 위해서, POST를 보낸 순간에 Redirect로 다른 경로를 보내고 GET 방식을 통해서 URL만 새로고침하여 POST를 중복으로 보내는 것을 방지
하는 방법이다.

* followed_posts() : User 클래스의 메소드로  유저가 db에서 관심이는 게시물을 가져올 수 있음 

* user.followed_posts().paginate(1, 20, False).items : 1페이지부터~ 20페이지까지, 지정된 페이지를 넘어간다면
True인 경우 404에러를 보내지만 False 인 경우 빈 화면을 내보낸다.
  * paginate(a,b,c) a : starting page number / b : number of items per page / c: an error flag

* Pagination class : item, has_next, has_prev, next_num, prev_num

* url_for(url, query args...)

# CH.12 Dates and Times
* datetime.utcnow() : utc기준 시간
  * datetime.now() : 내 지역 기준 시간
  
  
# CH.13 I18n(국제화) and L10n(지역화)

* from flask_babel import lazy_gettext as _l : 번역을 위해 텍스트를 추출(gettext)를 사용할때는 '_'을 사용하는 것이 convenction이다. 여기서는 lazy_gettext 를 사용하여 '_l'로 사용한다.

```python
from flask_babel import lazy_gettext as _l
login.login_message = _l('Please log in to accesss this page.')
```

*$ pybabel extract -F babel.cfg -k _l -o messages.pot . : pybabel extract는 명령에서 지정된 구성 파일을 읽는다. -F 옵션을 선택한 다음,
명령에 지정된 디렉토리에서 시작해 소스와 일치하는 디렉토리의 모든 코드 및 템플릿 파일을 검색한다. 

기본적으로 pybabel은 '_' 를 텍스트 마크로 읽지만 여기서는 lazy_gettxet를 사용했기에 '_l'로 찾으라고 해야 한다. (-k _l)

-o meesages.pot 은 출력파일을 messages.pot 으로 출력하라는 의미이다.


*$ pybabel init -i messages.pot -d app/translations -l es : pybabel을 통해서 번역해야 할 파일을 선택하고(-i message.pot)

위치는 app/translations(기본 폴더)에 저장한다.(-d app/translations)

번역하고 싶은 언어는 스페인어다.(-l es)


