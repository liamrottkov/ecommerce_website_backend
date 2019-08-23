from app import app, db
from flask import request, jsonify
from app.models import Product, Contact, User
import time
import jwt


# set index route to return nothing, just so no error occurs
@app.route('/')
@app.route('/index')
def index():
    return ''



@app.route('/api/save', methods=['POST'])
def save():
    try:
        # get headers first
        # NOTE: nothing to do with html headers
        title = request.headers.get('title')
        price = request.headers.get('price')
        description = request.headers.get('description')
        image_url = request.headers.get('image_url')

        # if any info is missing, give back an error jsonified message
        if not title or not price or not description or not image_url:
            return jsonify({ 'error' : 'Invalid parameters' })

        # all info is included, save the event
        product = Product(title=title, price=price, description=description, image_url=image_url)

        # add to db
        db.session.add(product)
        db.session.commit()

        return jsonify({ 'success' : 'Saved Product' })
    except:
        return jsonify({ 'error' : 'Error #002: Could not save Product' })



@app.route('/api/retrieve', methods=['GET'])
def retrieve():
    try:
        title = request.headers.get('title')
        price = request.headers.get('price')
        description = request.headers.get('description')
        image_url = request.headers.get('image_url')


        if not title:
            return jsonify({ 'error' : 'Error #003: Title is required' })
        # get results by price
        elif price and not title and not description:
            results = Product.query.filter_by( price=price).all()
        # get products by title
        elif title and not price and not description:
            results = Product.query.filter_by(title=title).all()
        # get products for the title and price
        elif title and price and not description:
            results = Product.query.filter_by(title=title, price=price).all()
        else:
            # get the specific products
            results = Product.query.filter_by(title=title, price=price, description=description, image_url=image_url).all()

        # if results is empty, there are no products, return response
        if results == []:
            return jsonify({ 'success' : 'No products to show' })

        # loop over results because it is an instance of Product, save information into new list and return
        products = []

        for result in results:
            product = {
                'title': result.title,
                'price': result.price,
                'description': result.description,
                'image_url': result.image_url
            }

            products.append(product)

        return jsonify({
            'success' : 'Retrieved Products',
            'products': products
        })
    except:
        return jsonify({ 'error': 'Error #007: Something went wrong' })



@app.route('/api/delete', methods=['DELETE'])
def delete():
    try:
        product_id = request.headers.get('product_id')

        product = Product.query.filter_by(product_id=product_id).first()

        if not product:
            return jsonify({ 'error': 'Error #005: Product does not exist' })

        title = product.title

        db.session.delete(product)
        db.session.commit()

        return jsonify({ 'success' : f'Product {title} deleted.' })
    except:
        return jsonify({ 'error': 'Error #006: Invalid parameters' })



@app.route('/api/save/contact', methods=['POST'])
def savePost():

        # get headers first
        # NOTE: nothing to do with html headers
        name = request.headers.get('name')
        email = request.headers.get('email')
        message = request.headers.get('message')
        print(name, email, message)
        # if any info is missing, give back an error jsonified message
        if not name or not email or not message:
            return jsonify({ 'error' : 'Invalid parameters' })

        # all info is included, save the event
        contact = Contact(name=name, email=email, message=message)

        # add to db
        db.session.add(contact)
        db.session.commit()

        return jsonify({ 'success' : 'Message recieved! We will get back to you as soon as we can!' })

        return jsonify({ 'error' : 'Error #002: Could not save Message' })



@app.route('/api/retrieve', methods=['GET'])
def checkout():
    try:
        title = request.headers.get('title')
        price = request.headers.get('price')
        description = request.headers.get('description')

        if not title:
            return jsonify({ 'error' : 'Error #003: Title is required' })
        # get results by price
        elif price and not title and not description:
            results = Product.query.filter_by( price=price).all()
        # get products by title
        elif title and not price and not description:
            results = Product.query.filter_by(title=title).all()
        # get products for the title and price
        elif title and price and not description:
            results = Product.query.filter_by(title=title, price=price).all()
        else:
            # get the specific products
            results = Product.query.filter_by(title=title, price=price, description=description).all()

        # if results is empty, there are no products, return response
        if results == []:
            return jsonify({ 'success' : 'No products to show' })

        # loop over results because it is an instance of Product, save information into new list and return
        products = []

        for result in results:
            product = {
                'title': result.title,
                'price': result.price,
                'description': result.description,
                'product_id': result.product_id,
                'image_url': result.image_url
            }

            products.append(product)

        return jsonify({
            'success' : 'Retrieved Products',
            'products': products
        })
    except:
        return jsonify({ 'error': 'Error #007: Something went wrong' })




@app.route('/api/retrieve/products', methods=['GET'])
def showProds():
    try:
        product = Product.query.all()


        products = []

        print('this should print')
        for p in product:
            new_product = {
                'title': p.title,
                'price': p.price,
                'description': p.description,
                'product_id': p.product_id,
                'image_url': p.image_url
            }

            products.append(new_product)

        return jsonify({ 'success': 'Worked', 'products': products })

        print('this should print after')
    except:
        return jsonify({ 'Error': 'Error: Failed'})



@app.route('/authentication/register', methods=['POST'])
def register():
    try:
        token = request.headers.get('token')

        print(token)

        # decode the token back to a dictionary
        data = jwt.decode(
            token,
            app.config['SECRET_KEY'],
            algorithm=['HS256']
        )

        print(data)

        # create the user and save
        user = User(email=data['email'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()

        return jsonify({ 'message' : 'success' })
    except:
        return jsonify({ 'message' : 'Error #001: User not created' })




@app.route('/authentication/login', methods=['GET'])
def login():
    try:
        token = request.headers.get('token')

        print(token)

        # decode the token back to a dictionary
        data = jwt.decode(
            token,
            app.config['SECRET_KEY'],
            algorithm=['HS256']
        )

        print(data)

        # query db to get user and check password
        user = User.query.filter_by(email=data['email']).first()

        # if user doesn't exist or password incorrect, send fail msg
        if user is None or not user.check_password(data['password']):
            return jsonify({ 'message' :  'Error #002: Invalid Credentials' })

        # create a token for that user and return it
        return jsonify({ 'message' : 'success', 'token': user.get_token() })
    except:
        return jsonify({ 'message' : 'Error #003: Failure to Login' })



@app.route('/api/data', methods=['GET'])
def data():
    try:
        token = request.headers.get('token')

        # get user id or none
        user = User.verify_token(token)

        if not user:
            return jsonify({ 'message' : 'Error #004: Invalid User' })

        # query database with user id that we got back from the verify token method, and create a new token to be passed back with encrypted information

        data = {
            'name': 'John Smith',
            'age': 27,
        }

        return jsonify({ 'info' : data })
    except:
        return jsonify({ 'message' : 'Error #005: Invalid token'})
