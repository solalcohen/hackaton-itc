import os
from bottle import (get, post, redirect, request, route, run, static_file,
                    template, jinja2_view, error)
import utils
import json
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='17011993',
                             db='new_schema',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)


# Static Routes

@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="./js")


@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="./css")


@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="./images")


@route('/')
def index():
    sectionTemplate = "./templates/home.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


@get("/how")
def how():
    sectionTemplate = "./templates/howwork.tpl"
    return template("./pages/logged.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


@get("/ourPartners")
def partners():
    sectionTemplate = "./templates/partners.tpl"
    return template("./pages/logged.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


@route('/store')
def browse():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM categories"
        cursor.execute(sql)
        result = cursor.fetchall()
    sectionTemplate = "./templates/store1.tpl"
    sectionData = result
    return template("./pages/logged.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=sectionData)


@route('/contact')
def search():
    sectionTemplate = "./templates/contact.tpl"
    return template("./pages/logged.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData={})

def requiers_login(handler_method):
    def check_login(*args):
        if not userIsLoggedIn():
            redirect('/signup')
        else:
            return handler_method(*args)
    return check_login


def userIsLoggedIn():
    emailFromCookie=request.get_cookie('mail')
    sessionFromCookie=request.get_cookie('password')
    with connection.cursor() as cursor:
        sql ="SELECT * FROM users WHERE email = '{}' AND password = '{}'".format(emailFromCookie,sessionFromCookie)
        cursor.execute(sql)
        result=cursor.fetchone()
        return result

@get
@post('/signin')
def signin():
    if request.method == 'POST':
        return handleLogin(request)
    else:
        context = {'err_msg': ''}
        sectionTemplate = "./templates/login.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,**context,
                    sectionData={})


def handleLogin(request):
    email = request.forms.get("email")
    password = request.forms.get("password")
    userVerified = verifyUser(email, password)
    if userVerified:
        redirect('/store')
    else:
        context = {"err_msg": "Wrong nickname or password"}
        return template("./pages/logged.html",version=utils.getVersion(), sectionTemplate="./templates/login.tpl", **context, sectionData={})


def verifyUser(email, password):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM users WHERE email = '{}' AND password = '{}'".format(email, password)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            return True
        return False


@route('/join')
def search():
    sectionTemplate = "./templates/form.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData={})


@post('/search')
@jinja2_view('search_result.tpl', template_lookup=['templates'])
def search_result():
    shows = []
    results = []
    query = request.forms.get('q')
    for show in utils.AVAILABE_SHOWS:
        json_show = utils.getJsonFromFile(show)
        dict_show = json.loads(json_show)
        shows.append(dict_show)
    for show in shows:
        for episode in show["_embedded"]["episodes"]:
            s = {}
            if type(episode['summary']) == str and query in episode['summary'] or type(
                    episode['name']) == str and query in episode['name']:
                s["showid"] = show['id']
                s['episodeid'] = episode['id']
                s['text'] = show["name"] + " : " + episode["name"]
                results.append(s)
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate="./templates/search_result.tpl",
                    sectionData={}, results=results, query=query)


@route('/show/<number>')
def show(number):
    with connection.cursor() as cursor:
        sql = "SELECT id_product,pr.product_name, pr.product_image, price, sup.supermarket_name, sup.supermarket_image, cat.id as category_id FROM prices  as p1 inner join supermarkets as sup on p1.id_supermarket = sup.id inner join products as pr on  p1.id_product = pr.id inner join categories as cat on pr.id_category = cat.id group by id_product,pr.product_name, pr.product_image, price, sup.supermarket_name, sup.supermarket_image having price <= (select min(p2.price) from prices as p2 where p2.id_product = p1.id_product group by p2.id_product) and category_id ={} order by price;".format(number)
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    sectionTemplate = "./templates/store2.tpl"
    return template("./pages/logged.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=result)


@route('/ajax/show/<number>')
def show(number):
    with connection.cursor() as cursor:
        sql = "SELECT id_product,pr.product_name, pr.product_image, price, sup.supermarket_name, sup.supermarket_image, cat.id as category_id FROM prices  as p1 inner join supermarkets as sup on p1.id_supermarket = sup.id inner join products as pr on  p1.id_product = pr.id inner join categories as cat on pr.id_category = cat.id group by id_product,pr.product_name, pr.product_image, price, sup.supermarket_name, sup.supermarket_image having price <= (select min(p2.price) from prices as p2 where p2.id_product = p1.id_product group by p2.id_product) and category_id ={} order by price;".format(number)
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return template("./templates/store2.tpl", result=result)


@route('/show/<number>/episode/<episode_number>')
def show(number, episode_number):
    sectionTemplate = "./templates/article.tpl"
    json_show = utils.getJsonFromFile(number)
    show = json.loads(json_show)
    episodes = show["_embedded"]["episodes"]
    for episode in episodes:
        if str(episode["id"]) == episode_number:
            result_episode = episode
    return template("./pages/logged.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=result_episode)


@route('/ajax/show/<number>/episode/<episode_number>')
def show(number, episode_number):
    json_show = utils.getJsonFromFile(number)
    show = json.loads(json_show)
    episodes = show["_embedded"]["episodes"]
    for episode in episodes:
        if str(episode["id"]) == episode_number:
            result_episode = episode
    return template("./templates/article.tpl", result=result_episode)


@error(404)
def error404(error):
    sectionTemplate = "./templates/404.tpl"
    return template("./pages/logged.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})




run(host='0.0.0.0', debug=True, port=os.environ.get('PORT', 5000))
