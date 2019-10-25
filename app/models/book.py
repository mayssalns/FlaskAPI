# -*- coding: utf-8 -*-

from app import db
from sqlalchemy.orm import relationship, backref
from app.models.author import Author


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True,  index=True, autoincrement=True)
    name = db.Column(db.String(50))
    summary = db.Column(db.String(300))
    author = relationship("Author", secondary="book_author")

    def __iter__(self, name, summary, id, author):
        return [
            self.name,
            self.summary,
            self.id,
            self.author
        ]


class AuthorBook(db.Model):
    __tablename__ = 'book_author'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    book = relationship(Book, backref=backref("author_book", cascade="all, delete-orphan"))
    author = relationship(Author, backref=backref("author_book", cascade="all, delete-orphan"))
