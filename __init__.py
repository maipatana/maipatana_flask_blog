import os
from flask import Flask, render_template, render_template_string, Markup, request, redirect, url_for, session, make_response
from flask_flatpages import FlatPages
from flask_flatpages.utils import pygmented_markdown
from contactform import ContactForm
from flask_wtf.csrf import CsrfProtect
from flask_mail import Message, Mail
#from werkzeug.contrib.atom import AtomFeed

app = Flask(__name__)

app.secret_key = os.urandom(36)

app.config.from_object(__name__)

CsrfProtect(app)

# email server
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.environ.get('MAIL_USERNAME')
app.config["MAIL_PASSWORD"] = os.environ.get('MAIL_PASSWORD')

mail=Mail(app)

HOSTING_DOMAIN = "https://maipatana.me"

#  ------------------------ Markdown Content System Management ------------------------ #
                                                                                        #
                                                                                        #
#DEBUG = True
#FLATPAGES_AUTO_RELOAD = DEBUG
per_page = 5
POSTS_DIR = 'blogs'


def pagenum(totalposts, postperpage):
    pages = [1]
    num = 2
    while totalposts > postperpage:
        pages.append(num)
        totalposts -= postperpage
        num += 1
    return pages

# # Take Jinja
# def prerender_jinja(text):
#     return pygmented_markdown(render_template_string(Markup(text)))

def my_renderer(text):
    prerendered_body = render_template_string(text)
    return pygmented_markdown(prerendered_body)

app.config['FLATPAGES_ROOT'] = 'content'
app.config['FLATPAGES_EXTENSION'] = '.md'
app.config['FLATPAGES_HTML_RENDERER'] = my_renderer

flatpages = FlatPages(app)
#  ------------------------ Markdown Content System Management ------------------------ #

#  -------------------------------------- Blogs ----------------------------------------#
                                                                                        #
                                                                                        #
@app.route('/blogs/', defaults={'page': 1})
@app.route("/blogs/page/<int:page>/")
def posts(page):
    cat = 'blogs'
    posts = [p for p in flatpages if p.path.startswith(POSTS_DIR) and cat in p.meta.get('cats', [])]
    posts.sort(key=lambda item:item['date'], reverse=True)
    total = len(posts)
    pages = pagenum(total, per_page)
    posts = posts[(page*per_page)-per_page:page*per_page]
    return render_template('posts.html', posts=posts, page=page, pages=pages, cat=cat)


@app.route('/blogs/<name>/')
def post(name):
    path = u'{}/{}'.format(POSTS_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)


@app.route('/tags/<string:tag>/', defaults={'page': 1})
@app.route('/tags/<string:tag>/page/<int:page>/')
def tags(tag, page):
    posts = [p for p in flatpages if tag in p.meta.get('tags', [])]
    posts.sort(key=lambda item:item['date'], reverse=True)
    total = len(posts)
    pages = pagenum(total, per_page)
    posts = posts[(page*per_page)-per_page:page*per_page]
    return render_template('posts.html', posts=posts, tag=tag, page=page, pages=pages)



#  ------------------------------------ Tutorials --------------------------------------#
                                                                                        #
                                                                                        #
@app.route('/tutorials/', defaults={'page': 1})
@app.route("/tutorials/page/<int:page>/")
def tutorials(page):
    cat = 'tutorials'
    posts = [p for p in flatpages if p.path.startswith(POSTS_DIR) and cat in p.meta.get('cats', [])]
    posts.sort(key=lambda item:item['date'], reverse=True)
    total = len(posts)
    pages = pagenum(total, per_page)
    posts = posts[(page*per_page)-per_page:page*per_page]
    return render_template('tutorials.html', posts=posts, page=page, pages=pages, cat=cat)


@app.route('/tutorials/<name>/')
def tutorial(name):
    path = u'{}/{}'.format(POSTS_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)


#  ------------------------------------ Projects ---------------------------------------#
                                                                                        #
                                                                                        #
@app.route('/projects/', defaults={'page': 1})
@app.route("/projects/page/<int:page>/")
def projects(page):
    cat = 'projects'
    posts = [p for p in flatpages if p.path.startswith(POSTS_DIR) and cat in p.meta.get('cats', [])]
    posts.sort(key=lambda item:item['date'], reverse=True)
    total = len(posts)
    pages = pagenum(total, per_page)
    posts = posts[(page*per_page)-per_page:page*per_page]
    return render_template('projects.html', posts=posts, page=page, pages=pages, cat=cat)


@app.route(u'/projects/<name>/')
def project(name):
    path = u'{}/{}'.format(POSTS_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)


#  ---------------------------- Redirect from old urls----------------------------------#
                                                                                        #
                                                                                        #
@app.route(u'/<name>/')
def redirectfromoldurls(name):
    path = u'{}/{}'.format(POSTS_DIR, name)
    post = flatpages.get_or_404(path)
    if "tutorials" in post.meta.get('cats',[]):
        return redirect(url_for('tutorial',name=name), code=301)
    return redirect(url_for('post', name=name), code=301)


#  ------------------------------------ About Me ---------------------------------------#
                                                                                        #
                                                                                        #
@app.route('/aboutme/')
def aboutme():
    # Contact Message
    form = ContactForm(request.form)
    if 'name' in session:
        name = session['name']
    else:
        name = []
    if request.method == 'POST' and form.validate():
        email = form.email.data.lower()
        name = form.name.data
        message = form.message.data
        subject = form.subject.data
        msg = Message('[maipatana]'+subject,
                      sender=emai, recipients= ['maipatana@gmail.com'])
        msg.body = """
        From: %s Email: %s
        %s
        """ % (name, email, message)
        mail.send(msg)
        session['name'] = name
        return redirect(url_for('home'))
    return render_template('aboutme.html', form=form, name=name)


#  -------------------------------------- Home -----------------------------------------#
                                                                                        #
                                                                                        #
@app.route('/', methods=['GET', 'POST'])
def home():
    # Recent Posts
    tags = [tag for p in flatpages if p.path.startswith(POSTS_DIR) for tag in p.meta.get('tags', []) ]
    blogs = [p for p in flatpages if p.path.startswith(POSTS_DIR) and 'blogs' in p.meta.get('cats', [])]
    blogs.sort(key=lambda item:item['date'], reverse=True)
    projects = [p for p in flatpages if p.path.startswith(POSTS_DIR) and 'projects' in p.meta.get('cats', [])]
    projects.sort(key=lambda item:item['date'], reverse=True)
    energy = [p for p in flatpages if p.path.startswith(POSTS_DIR) and 'tutorials' in p.meta.get('cats', [])
              and 'energy' in p.meta.get('tags', [])]
    energy.sort(key=lambda item:item['date'], reverse=True)
    ottv = [p for p in flatpages if p.path.startswith(POSTS_DIR) and 'tutorials' in p.meta.get('cats', [])
              and 'ottv' in p.meta.get('tags', [])]
    ottv.sort(key=lambda item:item['date'], reverse=False)
    simulation = [p for p in flatpages if p.path.startswith(POSTS_DIR) and 'tutorials' in p.meta.get('cats', [])
              and 'simulation' in p.meta.get('tags', [])]
    simulation.sort(key=lambda item:item['date'], reverse=False)
    grasshopper = [p for p in flatpages if p.path.startswith(POSTS_DIR) and 'tutorials' in p.meta.get('cats', [])
                   and 'grasshopper' in p.meta.get('tags', [])]
    grasshopper.sort(key=lambda item:item['date'], reverse=True)
    python = [p for p in flatpages if p.path.startswith(POSTS_DIR) and 'tutorials' in p.meta.get('cats', [])
              and 'python' in p.meta.get('tags', [])]
    python.sort(key=lambda item:item['date'], reverse=True)
    basicpy = [p for p in flatpages if p.path.startswith(POSTS_DIR) and 'tutorials' in p.meta.get('cats', [])
              and 'basic python' in p.meta.get('tags', [])]
    basicpy.sort(key=lambda item:item['date'], reverse=False)

    # Contact Message
    form = ContactForm(request.form)
    if 'name' in session:
        name = session['name']
    else:
        name = []
    if request.method == 'POST' and form.validate():
        email = form.email.data.lower()
        name = form.name.data
        message = form.message.data
        subject = form.subject.data
        msg = Message('[maipatana]'+subject,
                      sender=emai, recipients= ['maipatana@gmail.com'])
        msg.body = """
        From: %s Email: %s
        %s
        """ % (name, email, message)
        mail.send(msg)
        session['name'] = name
        return redirect(url_for('home'))
    # Render
    return render_template('home.html', blogs=blogs[:5], ottv=ottv[:5], projects=projects[:5], simulation=simulation[:5], basicpy=basicpy[:10],
                           energy=energy[:5], grasshopper=grasshopper[:5], python=python[:5], form=form, name=name, tags=set(tags))
#  ----------------------------------- End Home ----------------------------------------#

# Logout
@app.route('/logout/')
def logout():
    # remove the username from the session if it's there
    session.pop('name', None)
    return redirect(url_for('home'))

#  -------------------------------- Error Handling -------------------------------------#
@app.errorhandler(404)
def page_not_found(e):
    tags = [tag for p in flatpages if p.path.startswith(POSTS_DIR) for tag in p.meta.get('tags', []) ]
    return render_template("404.html", tags=set(tags))


@app.errorhandler(405)
def methodnotfound(e):
    return render_template("405.html", error='')


@app.errorhandler(500)
def internalerror(e):
    return render_template("500.html", error='')

#  ---------------------------- Sitemap Robot -------------------------------------#
@app.route('/sitemap.xml')
def generate_sitemap():
    posts = [p for p in flatpages if p.path.startswith(POSTS_DIR)]
    sitemap =  render_template("sitemap.xml", posts=posts)
    response= make_response(sitemap)
    response.headers["Content-Type"] = "application/xml"
    return response


@app.route('/robot.txt')
def robot():
    return ("""
    User-agent: *
    Disallow: /logout/
    Allow: /
    Sitemap: https://maipatana.me/sitemap.xml
    """)

# Run App
if __name__ == "__main__":
    app.run()
