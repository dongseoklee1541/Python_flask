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

* $flask db init : 마이그레이션 저장소 생성

* $flask db migrate : 데이터베이스를 변경하지 않고 마이그레이션 스크립트만 생성

* $flask db upgrade : 변경 사항을 데이터베이스에 적용, MYSQL, Postgre 와 같이 DB server 작업시 실행하기 전에 데이터베이스를 DB server에 생성해야 함

* $flas db downgrade : 변경 사항을 되돌리고 싶을때 사용, upgrade를 undo 한다.


# CH.05 Login

* werkzeug.security : 비밀번호를 특정 알고리즘을 통해 해쉬로 바꾸어 보안성을 높일 수 있는 패키지
  * generate_password_hash(args) : 를 통해 args을 해쉬값으로 바꾸어 반환해준다. 해쉬값은 매번 바뀌므로 해쉬값을 통해서 원래의 값을 알 수는 없다.
  
* filter_by


# CH.07 Error Handling

* $ set FLASK_DEBUG=1 : 플라스크의 디버그 모드를 실행하는 코드, 디버그 모드가 실행되면 소스코드가 수정될때 자동으로 서버를 재시작해준다. 이 모드는
상용서버에서 사용하면 안된다. 해킹을 하고자 하는 유저들에게는 내부 소스코드를 보여주는 결과가 되어 뜻하지 않는 선물을 주게 되기 때문이다.
디버그 모드를 해제하고 싶다면, 1을 0으로 바꾸어 실행해주자.

# CH.09 

* user.followed_posts().paginate(1, 20, False).items : 1페이지부터~ 20페이지까지, 지정된 페이지를 넘어간다면
True인 경우 404에러를 보내지만 False 인 경우 빈 화면을 내보낸다.

# CH.12 I18n(국제화) and L10n(지역화)

* from flask_babel import lazy_gettext as _l : 번역을 위해 텍스트를 추출(gettext)를 사용할때는 '_'을 사용하는 것이 convenction이다. 여기서는 lazy_gettext 를 사용하여 '_l'로 사용한다.

```python
from flask_babel import lazy_gettext as _l
login.login_message = _l('Please log in to accesss this page.')
```

* pybabel extract -F babel.cfg -k _l -o messages.pot . : pybabel extract는 명령에서 지정된 구성 파일을 읽는다. -F 옵션을 선택한 다음,
명령에 지정된 디렉토리에서 시작해 소스와 일치하는 디렉토리의 모든 코드 및 템플릿 파일을 검색한다. 

기본적으로 pybabel은 '_' 를 텍스트 마크로 읽지만 여기서는 lazy_gettxet를 사용했기에 '_l'로 찾으라고 해야 한다. (-k _l)

-o meesages.pot 은 출력파일을 messages.pot 으로 출력하라는 의미이다.
