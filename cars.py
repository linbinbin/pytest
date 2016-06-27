#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a Flask web app controller for the cars with rasberrypi.
"""

from flask import Flask, request, redirect, current_app 
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from flask_sslify import SSLify
from functools import wraps
from OpenSSL import SSL
from mock import Mock, patch
import unittest

context = ('cert.pem', 'privkey.pem')

users = {
    "john": "hello",
    "susan": "bye"
    }
 
app = Flask(__name__)
sslify = SSLify(app)
api = Api(app)

def ssl_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if current_app.config.get("SSL"):
            print("@ssl_required!")
            if request.is_secure:
                print("@ssl_required is secure!")
                return fn(*args, **kwargs)
            else:
                print("@ssl_required is nosecure!")
                return redirect(request.url.replace("http://", "https://"))
        
        return fn(*args, **kwargs)
            
    return decorated_view
    
class HelloWord(Resource):
    auth = HTTPBasicAuth()
    @staticmethod
    @auth.verify_password
    def verify_passord(username, password):
        if username:
            return password == users[username]
        else:
            return False
          
    @auth.login_required 
    @ssl_required  
    def get(self):
        return {'Hello':'world'}


    
api.add_resource(HelloWord,'/')

if __name__=='__main__':
    app.run(debug=True, ssl_context=context, threaded=True)