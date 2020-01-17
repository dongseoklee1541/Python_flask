# 웹 개발 이해 및 용어 정리
하나의 웹서버가 여러개의 앱을 서비스하는건 문제가 없다.(포트 번호만 다르게 만든다면 큰 문제 없음)

* web application : 서비스하는 모든 앱들을 총칭

* web application context : 앱들의 각각의 공간, 영역(HELLO FLASK, MICROBLOG) 즉 app에 접근한 사람들이 모두 사용하는 공용 공간

* session : app에 접근하는 한명의 유저(나만을)를 위한 영역(다만 같은 유저여도 다른 웹브라우저를 통해서 접근하면 다른 세션을 할당 받는다. 즉
웹브라우저 기준으로 나누는 것)

* MVR : Model, View, Route

* route : URI 를 정의하는 녀석

* lazy_loading : 모든 것을 메모리에 올리지 않겠다. 필요할때 실행해 메모리에 올리겠다는 것

* endpoint : 내 route의 URI를 뜻함

* WSGI : Web Server Gateway(특정 포트를 붙들고 있는 것) Interface(대면 하고 있는 것, 플라스크의 기본 포트인 5000번 포트를 계속 처다본다)

* Redirect : a.html로 접속했을때 b.html로 날려주는 것, 특정 url에 접근하면 목적지로 날려준다. 

* forward : Redirect와 동일한 역할을 하지만, 주소는 바뀌지 않는다.
## flask 이해
플라스크는 app, static, templates 등 정해진 양식의 폴더가 있다.

### folder & file

모든 웹앱은 request가 들어오면 그에 대한 response를 취하게 된다.
* applciation : py 파일과 같이 특정한 연산을 한 후 response 하는 경우

* static : img , css, javascript 등 연산없이 그대로 response하는 정적인 언어들을 static 이라고 한다.

* templates(view) : html 파일들이 모여 있는 폴더

* __init__.py : app의 모듈들의 시작지점, 모듈이 실행될때 자동으로 실행되는 파일이다.

* microblog.py(앱의 이름) : 앱을 메모리와 프로세서에게 할당하는 녀석

```python
from app import create_app, db, cli 
# 여기서 결국 app 폴더 안에 있는 __init__.py 을 실행시키는 거지만, 
# 여기선 생략해서 사용할 수 있다. 앱이 실행될때 함께 실행되어 그렇다
app = app.run() # 메모리에 올리는 과정
```

### flask global object : g

```python
from flask import g
```
여기서 **g** 는 전역변수이다. 또한 이 값들은 application_context에 저장되어 app에 접근하는 모든 사람들이 공유하는 자원이 된다.

### Request Parameter
Request는 기본이 string 형으로 되어있다. 다른 형태(int, list, etc...)로 사용하기 위해선 변환을 해줘야 한다.
```python

# MultiDict Type
...get('<param name>', <default-value>, <type>)
methods: get, getlist(리스트로 변환되어 반환), clear, etc
<type> : 기본값은 string 이지만, 여기에 int를 넣는다면 intger 형태로 반환한다.
# GET
request.args.get('q')

# 예시
@app.route('/rp')
def rp():
 q = request.args.get('q')
 return "q= %s" % str(q) # 이것의 결과값은 q = str(q) 의 값으로 response 된다.

# POST
request.form.get('p', 123) # 입력값이 있으면 'p'를 반환하지만 없다면 기본값으로 123을 반환하겠다.
                           # python 에서는 request.body 대신에 form으로 바꿔서 사용한다.
                           
# GET or POST : 원하는 정보가 편지봉투에 있는지('GET') 편지지('BODY','form')에 있는지 모를 때 values는 둘다 찾아본다.
request.values.get('v')

# Parameters
request.args.getlist('qs')
```

### Request Parameter Custom Function Type
```python
from datetime import datetime, date
# request 처리 용 함수
def ymd(fmt):
    def trans(date_str):
        return datetime.strptime(date_str, fmt)
    return trans
"""
request.values.get이 실행되어 ymd 함수가 실행되면, return 값이 메서드인 trans이므로 trans 함수가 실행되어 연산을 시작한다.
여기서 date_str의 값은 request.values.get의 인수인 'date'가 들어가게 된다. 이렇게 복잡하게 짜는 이유는 웹은 똑같은 함수를 여러 사용자가
여러번 사용하는데 이런 상황에서 메모리 낭비를 방지하기 위한 목적이다.
"""

@app.route('/dt')
def dt():
    datestr = request.values.get('date', date.today(), type=ymd('%Y-%m-%d'))
    return "우리나라 시간 형식: " + str(datestr)
```

### request.environ
환경 변수를 request 해보자.
```python
return ('REQUEST_METHOD: %(REQUEST_METHOD) s <br>' # %가 여기서는 request.environ['REQUEST_METHOD']로 호출된다.
        'SCRIPT_NAME: %(SCRIPT_NAME) s <br>'
        'PATH_INFO: %(PATH_INFO) s <br>'
        'QUERY_STRING: %(QUERY_STRING) s <br>'
        'SERVER_NAME: %(SERVER_NAME) s <br>'
        'SERVER_PORT: %(SERVER_PORT) s <br>'  
        'SERVER_PROTOCOL: %(SERVER_PROTOCOL) s <br>'
        'wsgi.version: %(wsgi.version) s <br>'
        'wsgi.url_scheme: %(wsgi.url_scheme) s <br>'
        'wsgi.input: %(wsgi.input) s <br>'
        'wsgi.errors: %(wsgi.errors) s <br>'
        'wsgi.multithread: %(wsgi.multithread) s <br>'
        'wsgi.multiprocess: %(wsgi.multiprocess) s <br>'
        'wsgi.run_once: %(wsgi.run_once) s') % request.environ
```

### request
```
request.is_xhr : xhr 이나 아니냐
request.url
request.path
request.endpoint : URI를 가져옴
request.get_json() : json의 data 부분을 가져온다
app.config.update(MAX_CONTENT_LENGTH=1024*1024) : 최대로 가져올 수 있는 문자열의 길이는 1024*1024이다.
request.max_content_length
```

### Templates(flask 에선 Jinja)
템플릿 엔진이란 ? 특정 언어(파이썬, JAVA, JS)등을 html(string, xml, json, image, video, etc..)로 변환시켜주는 녀석들

#### trim_blocks(공백 제거)
파이썬 코드로 인해 생기는 공백을 없애고 싶다면 양 사이드에 '-'을 붙여준다. %와 떨어져선 안되고 붙여줘야한다.

```
# ./templates/index.html
<pre>
ttt 한글
{%- if True -%}
    TTT
{%- endif -%}qqq
</pre>


# invalid, '-'을 %와 붙여줘라.
{% - if True - %}
# Tip: nodemon watching the html
nodemon start_helloflask.py -w helloflask/__init__.py -w helloflask/templates/index.html
```

#### escape
single quotation(따옴표), double quotation(쌍따옴표) 에 관계 없이 사용하면 코드가 실행되지 않고 그대로 html로 표기된다.
```
# quotation escape
{{ abc {ef} ghi }}  ⇒ {{ "abc {ef} ghi" }}
{{ "}}>> <strong>Strong</strong>"}}    or   {{ '}}>> <strong>Strong</strong>' | escape }} # escpae 사용하기

# cf. safe string & striptags  
{{ "<strong>Strong1</strong>" | safe}} : 쌍따옴표 있어도 무시하고 코드로 내
{{ "<strong>Strong2</strong>" | striptags}} : 

# {% raw %} ~ {% endraw %} : display source code , Jinja와 Handlebars를 함께 사용할때 유용
{% raw %}
	{% if True  %}
    		TTT
	{% endif %}
{% endraw %}
```

#### Markup

코드 단에서 render_template을 통해서 보낼때, html코드를 통해 강조하고 싶은 경우 사용한다.

```python
# from flask import Markup
return render_template("index.html", markup=Markup("<b>B</b>")) # 이때 markup은 Markup 객체로 전송한다.
# Example: Markup()
mu = Markup("<h1>iii = <i>%s</i></h1>")
h = mu % "Italic"
print("h=", h)
"""
 mu는 '%s'가 들어가 있어서 % 연산이 가능하다. 그래서 h에서 % "Italic"을 사용해 %s자리에 Italic를 넣을 수 있다.
"""
return render_template("index.html", markup=Markup(h))

# Markup.escape() & unescape()
bold = Markup("<b>Bold</b>")
bold2 = Markup.escape("<b>Bold</b>")
bold3 = bold2.unescape()

print(bold, bold2, bold3)
⇒ <b>Bold</b> &lt;b&gt;Bold&lt;/b&gt; <b>Bold</b>
```

#### FOR loop

```
# {% for var in iter %}  …  {% endfor %}
{% for item in items %}
	...item 처리..
{% endfor %}
# Example
lst = [ ("만남1", "김건모"), ("만남2", "노사연") ]
return render_template("index.html", lst=lst)

<ul>
    {% for item in lst %}
        <li>{{item[0]}}: {{item[1]}}</li>
    {% endfor %}
</ul>

{% for title, name in lst %} 
    <li>{{title}}: {{name}}</li> => 더 직관성이 있는(친절한) 코드, 하지만 튜플의 경우 받아야 하는 변수가 2개 이상으로 늘어날 경우 오류 발생
{% endfor %}
```

#### loop object
```
# for loop 속에서 기본으로 제공되는 object : `현재 for loop 의 self`
- loop.index: 1부터 시작하는 index 값  (cf. loop.index0 : 0부터 시작하는 index)
- loop.revindex: n~1 내림차순 index값  (cf. loop.revindex0 : 0 부터 시작하는 내림차순 index)
- loop.first: boolean(isThisFirstItem), loop의 첫번째인지의 여부, 첫번째이면 True 반환
- loop.last: boolean(isThisLastItem), loop의 마지막인지의 여부, 마지막이면 True 반환
- loop.length: size, 리스트의 길이
- loop.depth : loop 깊이 

# loop.cycle (특정 주기로 수행)
<ul>
    {% for item in lst %}
        <li class="{{loop.cycle('aaa', 'bbb')}}">{{item[0]}}: {{item[1]}}</li>
    {% endfor %}
</ul>
```

#### URL & Link
```
# url_for('folder', filename='filename.ext')
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" >

# url_for('router-link') : "/tmpl" 와 같은 방법을 사용해도 똑같다.
Copyright <a href="/tmpl">IndiFlex Senior Coding</a>
Copyright <a href="{{ url_for('tmpl') }}">IndiFlex Senior Coding</a>
```
----
## 참고 자료

참고자료 : [시니어 코딩 유튜브](https://docs.google.com/presentation/d/1S9mMlAYCulzAO8j5x9uCZbMUif8cAJHSHt1avztqeVg/edit#slide=id.g4ec498ce8e_0_5)
