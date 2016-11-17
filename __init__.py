import sys
from flask import Flask, render_template, render_template_string, Markup
from flask_flatpages import FlatPages, pygmented_markdown, pygments_style_defs
from flask_frozen import Freezer
from werkzeug.contrib.atom import AtomFeed

DEBUG = True

app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)

app.config.from_object(__name__)

#  ------------------------ Markdown Content System Management ------------------------ #
FLATPAGES_AUTO_RELOAD = DEBUG                                                           #
per_page = 5                                                                            #
POST_DIR = 'blogs'                                                                      #
                                                                                        #
                                                                                        #
def pagenum(totalposts, postperpage):                                                   #
    pages = [1]                                                                         #
    num = 2                                                                             #
    while totalposts > postperpage:                                                     #
        pages.append(num)                                                               #
        totalposts -= postperpage                                                       #
        num += 1                                                                        #
    return pages

# Take Jinja
def prerender_jinja(text):
    return pygmented_markdown(render_template_string(Markup(text)))

app.config['FLATPAGES_ROOT'] = 'content'
app.config['FLATPAGES_EXTENSION'] = '.md'
app.config['FLATPAGES_HTML_RENDERER'] = prerender_jinja


@app.route('/blogs/', defaults={'page': 1})
@app.route("/blogs/page/<int:page>/")
def posts(page):
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item:item['date'], reverse=True)
    total = len(posts)
    pages = pagenum(total, per_page)
    posts = posts[(page*per_page)-per_page:page*per_page]
    return render_template('posts.html', posts=posts, page=page, pages=pages)


@app.route('/blogs/<name>/')
def post(name):
    path = '{}/{}'.format(POST_DIR, name)
    post = flatpages.get_or_404(path)
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item:item['date'], reverse=True)
    return render_template('post.html', post=post, posts=posts[:5])

                                                                                        #
@app.route('/tags/<string:tag>/', defaults={'page': 1})                                 #
@app.route('/tags/<string:tag>/page/<int:page>/')                                       #
def tags(tag, page):                                                                    #
    posts = [p for p in flatpages if tag in p.meta.get('tags', [])]                     #
    posts.sort(key=lambda item:item['date'], reverse=True)                              #
    total = len(posts)                                                                  #
    pages = pagenum(total, per_page)                                                    #
    posts = posts[(page*per_page)-per_page:page*per_page]                               #
    return render_template('posts.html', posts=posts, tag=tag, page=page, pages=pages)  #
#  ------------------------ Markdown Content System Management ------------------------ #


@app.route('/')  # Home DashBoard
def home():
    return render_template('maipatana.html')


@app.route('/tutorials/')  # Tutorial
def tutorials():
    return render_template('tutorials.html')


@app.route('/projects/')  # miniProject
def projects():
    return render_template('projects.html')


@app.route('/aboutme/')  # about me
def aboutme():
    return render_template('aboutme.html')




# Run App
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run(debug=True)
