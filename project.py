
#================================
# Imports for the project
#================================
from flask import (
    Flask, 
    render_template,
    request, redirect,
    url_for, flash,
    jsonify
)
from sqlalchemy.orm.exc import NoResultFound
from flask import session as login_session
import random, string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database_set_FinalProject import Base, Category, CategoryItem, User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from functools import wraps
from flask import make_response
import requests


#===============================
# Client_ID for GConnect
#================================
CLIENT_ID = json.loads(
    open('/var/www/Item_catalog-/Item_catalog-/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog_S"


app = Flask (__name__)
#================================
# Database - CategoryUsers
#================================
engine = create_engine ('sqlite:///CategoryUsers.db')
Base.metadata.bind= engine

DBsession = sessionmaker (bind=engine)
session=DBsession()

#Function- decorator for making sure users are logged if __name__ == '__main__':
def login_required(parm):
    @wraps(parm)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in login_session:
            return redirect(url_for('showLogin'))
        return parm(*args, **kwargs)
    return decorated_function

# Login route, create anit-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(
            string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


#================================
# Login using gmail
#================================
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    #login_session['access_token'] = credentials.to_json()
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    #see if user exists, if not create new user
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, to Item Categories '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 100px; \
                    height: 100px;border-radius:\
                    150px;-webkit-border-radius: \
                    150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'], 'success')
    print "done!"
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except NoResultFound:
        return None


#=====================================
# Logout if you logged in using gmail
#=====================================
@app.route('/gdisconnect')
def gdisconnect():
    credentials = login_session.get('credentials')
    if credentials is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not logged in.'), 401)
        response.headers['Content-type'] = 'application/json'
        return response

    print 'In gdisconnect access token is %s', credentials
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % credentials
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        #del login_session['access_token']
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


#================================
# facebook logout
#================================
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)  # noqa
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"

@app.route('/categories/Catalog.Jason')
def categoryItemsJason():
    category= session.query(Category).all()
    items = session.query(CategoryItem).all()
    return jsonify(cat=[j.serialize for j in category], 
                   category_Items=[i.serialize for i in items] )



# Show all categories
@app.route('/')
@app.route('/categories/')
def cate():
    category= session.query(Category).all()
    return render_template ('category_c.html', category=category)
    

#================================
# Show categories items
#================================
@app.route('/categories/<int:category_id>')
@login_required
def category_Items(category_id):
    category= session.query(Category).filter_by(id=category_id).one()
    items = session.query(CategoryItem).filter_by(category_id=category.id)
    return render_template ('catItems.html',category=category, items=items)



## Add a new item to the category
@app.route('/categories/<int:category_id>/item/new', methods=['GET','POST'])
@login_required
def newCategoryItem(category_id):
    if request.method == 'POST':
        print login_session
        if 'user_id' not in login_session and 'email' in login_session:
            login_session['user_id'] = getUserID(login_session['email'])

        newItem = CategoryItem(
                    name=request.form['name'],
                    user_id=login_session['user_id'],
                    category_id=category_id)
        session.add(newItem)
        session.commit()
        flash ("New Item Is Just Created")
        #return redirect(url_for('category_Items', category_id=category_id))
        return redirect(url_for('category_Items',category_id=category_id))
    else:
        return render_template('newcategoryitem.html', category_id=category_id)

 # For cleanning sessions , in case it keeps you logged in.
@app.route('/clearsession')
def clearSession():
    login_session.clear()
    return "Session cleared"
   
 
#Edit existing category 
@app.route('/categories/<int:category_id>/<int:categoryItem>/edit/',methods=['GET','POST'])
@login_required
def EditCategoryItem(category_id,categoryItem):
    editedItem = session.query(CategoryItem).filter_by(id=categoryItem).one()
    if editedItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('Ooops! You are not authorized to edit!')} \
                        </script><body onload='myFunction()'>" 
    if request.method=='POST':
        if request.form['name']:
            editedItem.name=request.form['name']
        session.add(editedItem)
        session.commit()
        flash ("Item successfully edited")
        return redirect(url_for('category_Items', category_id=category_id))
    else:
        return render_template('editCategroyItem.html', category_id=category_id, 
                               CategoryItem=categoryItem, i=editedItem)


# Delete existing category 
@app.route('/categories/<int:category_id>/<int:categoryItem>/delete/',methods=['GET','POST'])
@login_required
def DeleteCategoryItem(category_id,categoryItem):
    deleteItem= session.query(CategoryItem).filter_by(id=categoryItem).one()
    if deleteItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('Ooops! You are not authorized to delete!')} \
                    </script><body onload='myFunction()'>" 
    if request.method=='POST':
        session.delete(deleteItem)
        session.commit()
        flash ("Item successfully deleted")
        return redirect(url_for('category_Items', category_id=category_id))
    else:
        return render_template('deleteCategoryItem.html', i=deleteItem)

    
 
if __name__ == '__main__':
    app.secret_key='super_secret_Key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=False)

