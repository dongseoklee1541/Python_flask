# CH.01 Hello, World!

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
