# maipatana_flask_blog

This is the code of my website that I am working on.<br>
The are three major parts; blogs, tutorials and projects.<br>
I am migrating from WordPress (maipatana.me) to flask.<br>
Hopefully I can launch this blog within this year.<br>

--------2016/11/26----------

The website is up on 26/11/2016. There are some minor additions that I didn't put it up on GitHub.<br>
For example, Google Analytic tracking code. However, the overall structure is the same.<br>
<br>
It is important to note that in order for Flask-Flatpages to ready non-ascii Markdown filenames, <br>
You should go to `/usr/local/lib/python2.7/dist-packages/flask_flatpages` or whereever your package is.<br>
Then open the file `flatpages.py`. At around line 191, I changed os.walk("My full path to Markdown files folder.")<br>
`for cur_path, _, filenames in os.walk("/var/www/FlaskApp/FlaskApp/content/blogs"):`<br>
Also at a few lines below, `I added .decode('utf-8')`.<br>
Like this `path = u'/'.join(path_prefix + (name_without_extension.decode('utf-8'), ))`.<br>
<br>
This will make reading non-ascii filename with no problem.<br>

--------2016/11/23----------

The site is ready to be used.<br>
The rest is to add more contents in /content/blogs/ folder.<br>
Category of the post is determinded by cats tag.<br>
There are three categories at the moment: blogs, tutorials and projects.<br>

--------2016/11/17----------

I have done the skeleton of the website.<br>
Tutorials and projects aren't yet concluded how it's going to be.<br>
I will soon start transfer my contents from my old site to here.<br>
Also will work on home-page as well.

