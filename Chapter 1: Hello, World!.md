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

