# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Blueprint, redirect, render_template, request, url_for


crud = Blueprint('crud', __name__)


# [START list]
@crud.route("/")
def list():
    return render_template("list.html")
# def list():
#     token = request.args.get('page_token', None)
#     if token:
#         token = token.encode('utf-8')

#     books, next_page_token = get_model().list(cursor=token)

#     return render_template(
#         "list.html",
#         books=books,
#         next_page_token=next_page_token)

# [END list]

# [START list]
@crud.route("/search", methods=['GET', 'POST'])
def search():
    key = ""

    if request.method == 'POST':
        key = request.form['searchKey']
        if key=="":
            return redirect(url_for('.list'))
    key = key.lower()

    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().list(cursor=token)
    matching_books = []
    
    for book in books:
        if key in book['title'].lower():
            matching_books.append(book)
        elif key in book['author'].lower():
            matching_books.append(book)

    return render_template(
        "search.html",
        books=matching_books,
        next_page_token=next_page_token,
        search_key = key)
# [END list]


@crud.route('/<id>')
def view(id):
    book = get_model().read(id)
    avgRating = get_model().readRatings(id)
    ratingReviews = get_model().readReviews(id)
    print(ratingReviews)
    return render_template("view.html", book=book, avgRating = avgRating, ratingReviews=ratingReviews)


# [START add]
@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        #data['rating'] = 0

        book = get_model().create(data)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Add", book={})
# [END add]


@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    book = get_model().read(id)
    
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        book = get_model().update(data, id)

        return redirect(url_for('.view', id=book['id']))
    
    return render_template("form.html", action="Edit", book=book)

@crud.route('/<id>/rate', methods=['GET', 'POST'])
def rate(id):
    book = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        data['bookId'] = id
        data['rating'] = request.form['rating']

        review = get_model().createReview(data, id)


        return redirect(url_for('.view', id=book['id']))

    return render_template("rating.html", action="Rate", review={})


@crud.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
