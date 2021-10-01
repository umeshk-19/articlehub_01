from flask import request, jsonify, render_template, redirect, url_for, make_response
from slugify import slugify
from datetime import datetime
from sqlalchemy import desc
from app import app, db
from app.models import Article
import dateutil.parser


@app.route("/", methods=["GET"])
def index():
    articlesdata = {}
    articledata = []
    articlesCount = 0
    articles = Article.query.order_by(Article.updatedAt.desc()).all()
    if request.args.get("error"):
        if request.args.get("error") == "article":
            error = "Article not found !"
        else:
            error = "Profile not found !"
    else:
        error = None
    for article in articles:
        data = {
            "slug": article.slug,
            "title": article.title.capitalize(),
            "description": article.description,
            "body": article.body,
            "image": article.image,
            "createdAt": article.createdAt.astimezone().isoformat(),
            "updatedAt": article.updatedAt.astimezone().isoformat(),
            "author": article.author,
        }
        articledata.append(data)
        articlesCount += 1
    articlesdata["articles"] = articledata
    articlesdata["articlesCount"] = articlesCount
    return render_template("feed.html", articles=articlesdata, error=error)


@app.route("/article/<slug>", methods=["GET"])
def get_articledata(slug):
    article = Article.query.filter(Article.slug == slug).first()
    if article:
        articledata = {
            "article": {
                "slug": article.slug,
                "title": article.title.capitalize(),
                "description": article.description,
                "body": article.body,
                "image": article.image,
                "createdAt": article.createdAt.astimezone().isoformat(),
                "updatedAt": article.updatedAt.astimezone().isoformat(),
                "author": article.author,
            }
        }
        return render_template("article.html", article=articledata["article"],)
    else:
        return redirect(url_for("index", error="article"))


@app.route("/articles/add", methods=["GET"])
def add_article():
    error = request.args.get("error") if request.args.get("error") else None
    return render_template("post.html", error=error)


@app.route("/article/edit/<slug>", methods=["GET"])
def edit_article_details(slug):
    article = Article.query.filter(Article.slug == slug).first()
    return render_template(
        "post.html",
        slug=slug,
        title=article.title,
        image=article.image,
        description=article.description,
        body=article.body,
        author=article.author,
        error=None,
    )


@app.route("/api/articles", methods=["POST"])
def article():
    data = request.get_json()
    title = data["article"]["title"].lower()
    articles = Article.query.filter(Article.title == title).count()
    if articles:
        slug = slugify(data["article"]["title"]) + "-" + str(articles + 1)
    else:
        slug = slugify(data["article"]["title"])
    description = data["article"]["description"]
    body = data["article"]["body"]
    if "image" in data["article"]:
        image = data["article"]["image"]
    else:
        image = None
    author = data["article"]["author"]
    createdAt = datetime.now()
    updatedAt = datetime.now()
    article = Article(
        slug, title, description, body, image, author, createdAt, updatedAt
    )
    db.session.add(article)
    db.session.commit()
    articledata = {
        "article": {
            "slug": article.slug,
            "title": article.title.capitalize(),
            "description": article.description,
            "body": article.body,
            "image": article.image,
            "author": article.author,
            "createdAt": article.createdAt.astimezone().isoformat(),
            "updatedAt": article.updatedAt.astimezone().isoformat(),
        }
    }
    return jsonify(articledata), 200


@app.route("/api/articles", methods=["GET"])
def all_articles():
    articlesdata = {}
    articledata = []
    articlesCount = 0
    articles = Article.query.order_by(Article.updatedAt.desc()).all()
    for article in articles:
        data = {
            "slug": article.slug,
            "title": article.title.capitalize(),
            "description": article.description,
            "body": article.body,
            "image": article.image,
            "author": article.author,
            "createdAt": article.createdAt.astimezone().isoformat(),
            "updatedAt": article.updatedAt.astimezone().isoformat(),
        }
        articledata.append(data)
        articlesCount += 1
    articlesdata["articles"] = articledata
    articlesdata["articlesCount"] = articlesCount
    return jsonify(articlesdata), 200


@app.route("/api/articles/<slug>", methods=["GET"])
def get_article(slug):
    article = Article.query.filter(Article.slug == slug).first()
    if article:
        articledata = {
            "article": {
                "slug": article.slug,
                "title": article.title.capitalize(),
                "description": article.description,
                "body": article.body,
                "image": article.image,
                "author": article.author,
                "createdAt": article.createdAt.astimezone().isoformat(),
                "updatedAt": article.updatedAt.astimezone().isoformat(),
            }
        }
        return jsonify(articledata), 200
    else:
        return ("No article found with this slug"), 404


@app.route("/api/articles/<slug>", methods=["PUT", "DELETE"])
def edit_article(slug):
    article = Article.query.filter(Article.slug == slug).first()
    if article:
        if request.method == "PUT":
            data = request.get_json()
            if "title" in data["article"]:
                article.title = data["article"]["title"].lower()
                title = data["article"]["title"].lower()
                articles = Article.query.filter(Article.title == title).count()
                if articles > 1:
                    slug = slugify(data["article"]["title"]) + "-" + str(articles)
                else:
                    slug = slugify(data["article"]["title"])
                article.slug = slug
            if "description" in data["article"]:
                article.description = data["article"]["description"]
            if "body" in data["article"]:
                article.body = data["article"]["body"]
            if "image" in data["article"]:
                article.image = data["article"]["image"]
            if "author" in data["article"]:
                article.author = data["article"]["author"]
            article.updatedAt = datetime.now()
            db.session.commit()
            article = Article.query.filter(Article.slug == slug).first()
        elif request.method == "DELETE":
            db.session.delete(article)
            db.session.commit()
        articledata = {
            "article": {
                "slug": article.slug,
                "title": article.title.capitalize(),
                "description": article.description,
                "body": article.body,
                "image": article.image,
                "author": article.author,
                "createdAt": article.createdAt.astimezone().isoformat(),
                "updatedAt": article.updatedAt.astimezone().isoformat(),
            }
        }
        return jsonify(articledata), 200
    else:
        return ("No article found with this slug"), 404


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("404.html"), 404


@app.template_filter("datetime")
def _jinja2_filter_datetime(date):
    date = dateutil.parser.parse(date)
    return date.strftime("%b %d, %Y")
