# -*- coding: utf-8 -*-

import math

from flask import request, jsonify, Blueprint, Response
from flask.views import MethodView
from app import db, app
from app.models.author import Author
from app.models.book import AuthorBook
from app.serializers.AuthorSerializer import AuthorSerializer



author = Blueprint('Author', __name__)


class AuthorView(MethodView):


    def get_author_detail(pk):
        author = []
        for author_book in AuthorBook.query.filter_by(book_id=pk).all():
            author.append({'id': author_book.author_id, 'name': author_book.author.name})
        response = author
        return jsonify(response)
   

    @author.route('/v1/author/<int:pk>/',  methods=['GET', 'PUT', 'DELETE'])
    @author.route('/v1/author/<int:pk>',  methods=['GET', 'PUT', 'DELETE'])
    @author.route('/v1/author/', methods=['GET', 'POST'])
    @author.route('/v1/author', methods=['GET', 'POST'])
    def index(pk=None):
        if request.method == 'GET': #OK
            if not pk:
                if request.args.get('name') is not None:
                    authors = Author.query.filter(Author.name.ilike("%"+request.args.get('name')+"%")).order_by(Author.name).all()
                else:
                    authors = Author.query.order_by(Author.name).all()
                response = AuthorView().paginate()

            else:
                response = AuthorSerializer().get_by_id(Author.query.filter_by(id=pk).first())
            return jsonify(response)


        elif request.method == 'POST':
            try:
                AuthorView().post()
                return Response('Created', 201)
            except Exception as exc:
                return Response(exc, 500)


        elif request.method == 'DELETE': #OK
            try:
                AuthorView().delete(pk)
                return Response(' Delete Successfully!', 200)
            except Exception as exc:
                return Response(exc, 500)

        elif request.method == 'PUT':
            try:
                AuthorView().update(pk)
                return Response(' Update Successfully!', 200)
            except Exception as exc:
                return Response(exc, 500)

    @staticmethod
    def post():
        data = request.form
        db.session.add(Author(name=data['name']))
        db.session.commit()
        
    @staticmethod
    def delete(pk=None):
        for relationship in AuthorBook.query.filter(AuthorBook.author_id == pk).all():
            AuthorBook.query.filter(AuthorBook.id == relationship.id).delete()
        Author.query.filter(Author.id == pk).delete()
        db.session.commit()


    @staticmethod
    def update(pk):
        data = request.form
        name = request.values.get('name')
        Author.query.filter(Author.id == pk).update({'name': data['name']})
        db.session.commit()


    @staticmethod
    def paginate():
        previous = None
        next = None
        total = len(Author.query.order_by(Author.name).all())
        count_pages = math.ceil(total / 5)
        if request.args.get('page') is None:
            page = 1
        else:
            page = int(request.args.get('page'))

        if 1 <= page < int(count_pages):
            next = 'http://0.0.0.0:8000/v1/author/?page='+str(page+1)
        if page == 1:
            previous = None
        else:
            previous = 'http://0.0.0.0:8000/v1/author/?page='+str(page-1)

        authors = Author.query.paginate(page, 5).items

        response = {'count': total, 'next': next, 'previous': previous}
        results = []
        for detail_author in authors:
            results.append({
                'id': detail_author.id,
                'name': detail_author.name
            })
            response['results'] = results
        return response