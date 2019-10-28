# -*- coding: utf-8 -*-

import math

from app.models.book import Book, AuthorBook
from flask.views import MethodView
from flask import request, jsonify, Blueprint, Response
from app import db, app
from app.serializers.BookSerializer import BookSerializer

book = Blueprint('Book', __name__)

class BookView(MethodView):
    @book.route('/v1/book/<int:pk>/author/')
    def get_author_detail(pk):
        author = []
        for author_book in AuthorBook.query.filter_by(book_id=pk).all():
            author.append({
                'id': author_book.author_id, 
                'name': author_book.author.name
            })
        res = author
        return jsonify(res)

    @book.route('/v1/book/<int:pk>/',  methods=['GET', 'PUT', 'DELETE'])
    @book.route('/v1/book/<int:pk>',  methods=['GET', 'PUT', 'DELETE'])
    @book.route('/v1/book/', methods=['GET', 'POST'])
    @book.route('/v1/book', methods=['GET', 'POST'])
    def home(pk=None):
        if request.method == 'GET':
            if not pk:
                if request.args.get('name') is not None:
                    books = Book.query.filter(Book.name.ilike("%"+data['name']+"%")).order_by(Book.name).all()
                else:
                    books = Book.query.order_by(Book.name).all()
                res = BookView().pagination()
            else:
                res = BookSerializer.get_by_id(Book.query.filter_by(id=pk).all(), AuthorBook)
            return jsonify(res)

        elif request.method == 'POST':
            try:
                BookView().post()
                return Response('Created', 201)
            except Exception as exc:
                return Response(exc, 500)

        elif request.method == 'DELETE':
            try:
                BookView().delete(pk)
                return Response('Delete Successfully', 200)
            except Exception as exc:
                return Response(exc, 500)

        elif request.method == 'PUT':
            try:
                BookView.update(pk)
                return Response(' Update Successfully!', 200)
            except Exception as exc:
                return Response(exc, 500)

    @staticmethod
    def post():
        data = request.form
        book = Book(name=data['name'],summary=data['summary'])
        db.session.add(book)
        db.session.commit()
        for authors in data['author']:
            if authors is not '':
                details = Book.query.order_by(Book.id.desc()).first()
                db.session.add(AuthorBook(author_id=authors, book_id=details.id))
                db.session.commit()

    @staticmethod
    def delete(pk):
        for relationship in AuthorBook.query.filter(AuthorBook.book_id == pk).all():
            AuthorBook.query.filter(AuthorBook.id == relationship.id).delete()
        Book.query.filter(Book.id == pk).delete()
        db.session.commit()

    @staticmethod
    def update(pk):
        data = request.form
     
        if data['name'] not in '':
            Book.query.filter(Book.id == pk).update({'name': data['name']})
            db.session.commit()
        if data['summary'] not in '':
            Book.query.filter(Book.id == pk).update({'summary': data['summary']})
            db.session.commit()
        if data['author'] not in '':
            for relationship in AuthorBook.query.filter(AuthorBook.book_id == pk).all():
                AuthorBook.query.filter(AuthorBook.id == relationship.id).delete()
            for authors in data['author']:
                if authors not in '':
                    details = Book.query.order_by(Book.id.desc()).first()
                    db.session.add(AuthorBook(author_id=authors, book_id=details.id))
                    db.session.commit()


    @staticmethod
    def pagination():
        previous = None
        next = None
        total = len(Book.query.order_by(Book.name).all())
        count_pages = math.ceil(total / 5)
        if request.args.get('page') is None:
            page = 1
        else:
            page = int(request.args.get('page'))

        if 1 <= page < int(count_pages):
            next = 'http://0.0.0.0:8000/v1/book/?page='+str(page+1)
        if page == 1:
            previous = None
        else:
            previous = 'http://0.0.0.0:8000/v1/book/?page='+str(page-1)

        books = Book.query.paginate(page, 5).items
        res = {'count': total, 'next': next, 'previous': previous}
        lista = []
        for detail_book in books:
            author = []
            for author_book in AuthorBook.query.filter_by(book_id=detail_book.id).all():
                author.append(author_book.author_id)
            lista.append({
                'name': detail_book.name,
                'summary': detail_book.summary,
                'author': author,
                'id': detail_book.id
            })
            res['results'] = lista
        return res