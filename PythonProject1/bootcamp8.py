class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(250), nullable=False)
# SQLAlchemy در بسیاری از موارد می‌تواند خودش نام جدول را از نام کلاس بسازد، اما با:
__tablename__ = "blog_posts"
# خودمان صریحاً نام جدول را تعیین می‌کنیم.
#########################################################################################
# وقتی یک دکوراتور خودمان میسازیم و آن را روی چند route میگذاریم معمولا خطا میگیریم مثلا در زیر خطا خواهیم داشت
#چونکه admin_only را خودمان ساخته ایم
@app.route("/new-post")
@login_required
@admin_only
def add_new_post():
    pass

@app.route("/edit-post/<int:post_id>")
@login_required
@admin_only
def edit_post(post_id):
    pass
#برای رفع این مشکل به این پکیج نیاز داریم
from functools import wraps
# سپس دکوراتور خود را از حالت زیر
def admin_only(function):
    def wrapper(*args, **kwargs):
        if current_user.id == 1:
            return function(*args, **kwargs)
        else:
            return abort(403)
    return wrapper
#به حالت زیر تغییر خواهیم داد یعنی wraps@ را اضافه میکنیم
def admin_only(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.id == 1:
            return function(*args, **kwargs)
        else:
            return abort(403)
    return wrapper
#حالا یک نکته این abort چیست؟
#وقتی دسترسی به یک صفحه را میبندیم بهتر است که از این متد استفاده کنیم.
#
# این متد کد خطای مورد نظر را از ما میگیرد و در صفحه اطلاعات خطای لازم را به کاربر میدهد
# مثلا بجای کد زیر
if current_user.id == 1:
    return function(*args, **kwargs)
else:
    # return "Forbidden", 403
#مینویسیم
if current_user.id == 1:
    return function(*args, **kwargs)
else:
    return abort(403)

#باید این متد را به صورت زیر load کنیم
from flask import abort
# سپس بدون استفاده از return هم میتوانیم از آن استفاده کنیم مانند flash با این تفاوت که نیازی به کد در html ندارد
#########################################################################################
from sqlalchemy.orm import relationship
# کد بالا چیست و چه کاربردی دارد؟
# فرض کن دو جدول داریم:
# User
# BlogPost
# هر کاربر می‌تواند چند پست داشته باشد.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#author_id
# می‌گوید:
# این پست متعلق به کدام User است؟
# پس ForeignKey ارتباط را در سطح دیتابیس برقرار می‌کند.
# پس relationship برای چیست؟
# حالا می‌خواهیم در پایتون بتوانیم این کار را انجام دهیم:
# post.author
# و مستقیماً User مربوط به پست را بگیریم.
# یا برعکس:
# user.posts و تمام پست‌های آن کاربر را بگیریم.
# اینجاست که:
# relationship()
# وارد می‌شود.
# مدل کامل
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    # This will act like a List of BlogPost objects attached to each User.
    # The "author" refers to the author property in the BlogPost class.
    posts = db.relationship("BlogPost", back_populates="author")

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    # Create Foreign Key, "user.id" the users refers to the tablename of User.
    author_id = db.Column( db.Integer, db.ForeignKey("user.id"))
    # Create reference to the User object, the "posts" refers to the posts protperty in the User class.
    author = db.relationship("User", back_populates="posts")
# حالا دو چیز داریم:
# 1.ForeignKey
author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
# ارتباط واقعی بین رکوردهای دیتابیس را مشخص می‌کند.
# 2.relationship
posts = db.relationship("BlogPost", back_populates="author")
author = db.relationship("User", back_populates="posts")
# وقتی با یک User کار می‌کنم، بتوانم به BlogPostهای مرتبطش از طریق user.posts دسترسی داشته باشم.
# و back_populates هم باعث می‌شود از سمت BlogPost بتوانیم بنویسیم:
# post.author
#فرض کن
user = User.query.get(1)
# نتیجه چیزی شبیه این است
[
    <BlogPost 1>,
    <BlogPost 2>
]
# پس
for post in user.posts:
    print(post.title)
 # از طرف دیگر:
post = BlogPost.query.get(1)
post.author
#  نتیجه میشود<User 1>
# بعد
post.author.name
#این بحث ارتباط مدلها 4 حالت دارد
# 1. One-to-Many
# یک User
#    ↓
# چند BlogPost
# 2. Many-to-One
# چند BlogPost
#       ↓
#    یک User
# 3. Many-to-Many
# 4. One-to-One
# از کجا باید بدانیم این foreignkey در کدام کلاس باشد
# قاعده‌ی اصلی:
# Foreign Key در کلاسی قرار می‌گیرد که «چندتا» است.
#الان در مثال های بالا در BlogPost هست چرا
# چون BlogPost سمت MANY است و هر پست باید مشخص کند متعلق به کدام User است
#دقت شود که posts  و author ستون های دیتابیس نیستند بلکه آبجکتی از هر کلاس در کلاس دیگری هستند تا بین این دو کلاس رابطه برقرار کنند
#########################################################################################
#اگر در یک فایل html همزمان از extends  و include استفاده کنیم باید
# در Jinja وقتی از extends استفاده می‌کنی، باید اولین دستور template باشد:
# {% extends 'bootstrap/base.html' %}
# {% import 'bootstrap/wtf.html' as wtf %}
# بعد اگر می‌خواهی header.html را وارد کنی، باید آن را داخل یک block قرار بدهی:
# {% extends 'bootstrap/base.html' %}
# {% import 'bootstrap/wtf.html' as wtf %}
# {% block content %}
#     {% include "header.html" %}
#     <!-- Page Header -->
#     <header class="masthead" style="background-image: url('{{post.img_url}}')">
#         ...
#     </header>
#     <!-- Post Content -->
#     <article>
#         ...
#     </article>
#     {% include "footer.html" %}
# {% endblock %}
#########################################################################################
# Gravatar چیست؟
# Gravatar سرویسی است که برای هر ایمیل، یک تصویر پروفایل (Avatar) مرتبط دارد.
# در Flask معمولاً این‌طور استفاده می‌شود:
from flask_gravatar import Gravatar
gravatar = Gravatar(
    app, size=100, rating='g', default='retro', force_default=False, force_lower=False,
    use_ssl=False, base_url=None)

# بعد در قالب Jinja می‌توانی مثلاً:
< img src = "{{email | gravatar }}"/>
# خودش عکس را داخل دیتابیس ذخیره نمی‌کند. بر اساس ایمیل کاربر، یک URL برای Avatar می‌سازد
# و مرورگر آن تصویر را از Gravatar دریافت می‌کند.
#########################################################################################
# TODO PROJECT 69 ساختن وبسایت با لاگین و آواتار و سه نوع دیتابیس از
#########################################################################################
# Git
#version control
# در ابتدا برنامه git-bash را باز میکنیم سپس در این برنامه برای اینکه به root direction دسترسی داشته باشیم باید از ~ cd  استفاده کنیم
#سپس برای اینکه بفهمیم در موقعیت درست قرار گرفتیم از ls استفاده میکنیم تا لیست فایل و فولدرها را بر گرداند
#سپس وارد terminal یا همان powershell میشویم و در آنجا در دسکتاپ فولدر جدید به نام مثلا Story میسازیم
#سپس در ادامه یک فایل متنی مثلا با نام Chapter1.txt میسازیم برای باز کردن این فایل از دستور start Chapter1.txt استفاده میکنیم
#که هم در git_bash و هم در powershell این دستور قابل استفاده است سپس کمی متن داخل آن فایل مینویسیم. در این مرحله باید
# ما یک git local repository بسازیم تا تغییرات را برای ما رصد کند برای این کار ابتدا باید git را در پوشه مورد نظر نصب کنیم از
#طریق git init این دستور را در powershell  وارد میکنیم وقتی از ls عادی استفاده کنیم فایل های نصب شده نشان داده نمیشوند چونکه پنهان هستند
#برای اینکار از دستور ls -force استفاده میکنیم خب برای اینکه ما تغییرات را در فایل ها رصد کنیم باید ابتدا آنها را در قسمتی که
#به نام staging area نامدارد وارد کنیم این بخش جایی است که تعیین میکنیم کدام فایل های موجود در پوشه مورد نظر باید وارد git شوند و تغییراتشان رصد شود
# برای اینکه بدانیم کدام فایل ها در این staging area هشتند باید از دستور git status استفاده کنیم داخل powershell فایل هایی که با رنگ قرمز هستند یعنی
#هنوز وارد این مرحله یا staging area نشده اند. برای وارد کردن آنها به این مرحله از باید از دستور git add  chapter1.txt استفاده کنیم
# سپس دوباره برای فایل های منتقل شده به این بخش از git status استفاده میکنیم و میبینیم که فایل قرمز الان به بخش مورد نظر برای رصد کردن اضافه شده و رنگش سبز شده است
#برای اینکه توضیح دهیم در آن مرحله از تغییراتی که بر سر فایل آوردیم چه تغییراتی صورت گرفته تا وقتی که دوباره تاریخچه تغییرات را نگاه کردیم ببینیم چه کرده ایم
#باید از دستور "git commit -m "complete chapter1 of story در powershell استفاده کینم. نکته ی مهم این هست که باید تغییرات به
#زبان حال باشد نه گذشته.  حالا برای مشاهده تغییرات انجام شده روی فایل و مشاهده تاریخچه میتوان از دستور git log استفاده کرد
#نکته ی مهم اینکه گاها ممکنه سیستم هشدار دهد که کاربری که دستور میدهد مشخص نیست. برای رفع این مشکل باید یا نام کاربر یا ایمیل را مشخص کرد از طریق زیر
#  git config--global user.email "you@example.com"
#  git config--global user.name "your name"
#حالا برای ثبت تغییرات بیشتر در git دو فایل جدید میسازیم و باید همان کارهای ابلا را برای اضافه کردن آنها به staging area انجام بدیم
#سپس یکسری مطالب داخل آنها مینویسیم. دوباره git status را میزنیم تا ببینیم چه فایل هایی وارد staging area نشده اند
# سپس باید آنها را به staging area اضافه کنیم. اما نکته ی اینجا این است که ما نمیتوانیم برای تعداد زیادی فایل از
#دستور git add filename استفاده کنیم. در عوض از دستور . git add space برای اضافه کردن گروهی استفاده میکنیم دقت شود سپیس همان جای خالی
#هست و نه بخشی از دستور نوشتاری. با این کار همه فایل های داخل آن دایرکتوری به گیت اضافه میشوند
# سپس دوباره از "git commit -m "complete chapter 2 and 3 استفاده میکنیم تا این بخش از توضیحات مربوط به تغییرات را هم ذخیره کنیم
# سپس با زدن git log تغییرات را میبینیم
#working directory -> staging area -> local repositry
#اولی همان پوشه است دومی همان مرکز رصد تغییرات فایل است و سومی جایی است که نسخه قبلی فایل ها وجود دارد تا در صورت نیاز نسخه قبلی فایل ها را برگردانیم
#خب الان مثلا فایل سوم chapter3.txt را باز میکنیم و متن آنرا عوض میکنیم. سپس دوباره با زدن git status میبینیم کدام فایل را تغییر داده ایم
# سپس با زدن دستور git diff chapter3.txt تغییرات داده شده را نگاه میکنیم و اگر مورد قبول نباشد و بخواهیم فایل نسخه قبلی را برگردانیم
#باید از دستور git checkout chapter3.txt استفاده کنیم که فورا فایل را به نسخه قبلی برمیگرداند.
#و اگر بخواهیم آنرا ذخیره کنیم ابتدا دوباره git add chapter3.txt را میزنیم سپس برای توضیح تاریخچه "git commit -m "explain
#########################################################################################
#Remote repository By GitHub
#برای اینکه بتوانیم فایل هایی را که در git local داریم به github منتقل کنیم ابتدا وارد گیت هاب میشویم
#سپس در آنجا وارد قسمت new repository میشویم و نام مناسبی براش مینویسیم همراه توضیحات مختصر و یک repository جدید میسازیم در صفحه بعد یک لینک داریم
#و دو روش برای ایجاد repository روش اول ساختن مستقیم از گیت هاب و دومی مانند ما انتقال از محلی به ریموت
#سپس در powershell از کد های زیر استفاده میکنیم
# git remote add origin https://github.com/momenfortest1-bit/Story.git
# git push -u origin master
#در بالا origin  نام  ریموت ما هست و میتواند هر چیزی باشد اسمش اما پیشنهاد این است همان origin بماند
#در بالا master هم نام branch اصلی در گیت هاب هست
#سپس در گیت هاب با رفتن به بخش insights سپس network میتوانیم مراحل ساختی را که از طریق git commit m ساختیم را ببینیم
#یا با زدن commit زیر بخش code در گیت هاب میتوان همان مراحل ساخت را دید سپس با زدن روی هر بخش میتوان تغییرات را دید
# نکته اینکه برای این که همه repository ها را ببینیم روی آیکون پروفایل کلیک میکنیم سپس روی all repositories سپس روی my repositories
#########################################################################################
# Local Version Control with PyCharm
# we can do this in PyCharm by simply going to VCS -> Enable Version Control Integration.
# This is the same as what we did before with git init
# در ابتدا میبینیم که  همه فایل ها به رنگ نارنجی یا قرمز هستند چونکه هنوز مرحله ی git add انجام نشده است برای اینکار
#ابتدا فایل پروژه اصلی را از منوی سمت چپ انتخاب نموده سپس با رفتن به git-> selected directory/ file -> add
#فایل را به گیت اضافه میکنیم حالا رنگشان سبز میشود حالا برای اضافه کردن اولین commit  به  git-> commit  میرویم
#اگر اولین commit را زدیم میتوانیم با رفتن به git-> show git log نتایج را ببینیم
#########################################################################################
# حالا فرستادن به remote  یا همان گیت هاب از طریق pycharm