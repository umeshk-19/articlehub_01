from app import db


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    image = db.Column(
        db.String,
        default="https://static.wixstatic.com/media/8e9ccd_21329500d45c427f82869bc547dbe44c~mv2.jpg",
        nullable=False,
    )
    author = db.Column(db.String, nullable=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

    def __init__(
        self, slug, title, description, body, image, author, createdAt, updatedAt
    ):
        self.slug = slug
        self.title = title
        self.description = description
        self.body = body
        self.image = image
        self.author = author
        self.createdAt = createdAt
        self.updatedAt = updatedAt
