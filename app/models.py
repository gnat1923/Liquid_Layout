from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    id : so.Mapped[int] = so.mapped_column(primary_key=True)
    username : so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email : so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash : so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    
    posts : so.WriteOnlyMapped["Post"] = so.relationship(back_populates="author")

    def __repr__(self):
        return "<User {}>".format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Post(db.Model):
    id : so.Mapped[int] = so.mapped_column(primary_key=True)
    title : so.Mapped[str] = so.mapped_column(sa.String(64))
    body : so.Mapped[str] = so.mapped_column(sa.Text)
    map_embed : so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    transit : so.Mapped[str] = so.mapped_column(sa.String(64))
    neighbourhood : so.Mapped[str] = so.mapped_column(sa.String(64))
    beer_rating : so.Mapped[str] = so.mapped_column(sa.Integer)
    guinness : so.Mapped[bool] = so.mapped_column(sa.Boolean)
    smoking : so.Mapped[bool] = so.mapped_column(sa.Boolean)
    music : so.Mapped[str] = so.mapped_column(sa.String(128))
    visible : so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True, nullable=True)
    image_data: so.Mapped[bytes] = so.mapped_column(sa.LargeBinary, nullable=True)  # Store image data
    image_filename: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)  # Store image filename
    timestamp : so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id : so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author : so.Mapped[User] = so.relationship(back_populates="posts")

    def __repr__(self):
        return "<Post {}>".format(self.body)