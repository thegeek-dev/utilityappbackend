from flask_restful import Resource
from flask import request
from config import db
from passlib.hash import sha256_crypt
import math
import random
import jwt
from config import mailjet


class AddUser(Resource):
    def post(self):
        if self.check_user(request.json['username']) != None:
            return {'message': "username already exists"}, 409
        if self.check_user(request.json['email']) != None:
            return {'message': "email already exists"}, 409
        reqEmail = request.json['email']
        reqOtp = request.json['otp']
        actualOtp = db.otps.find_one({'email': reqEmail})['otp']
        if reqOtp != actualOtp:
            return {'message': 'otp is wrong'}, 401
        db.users.insert_one(
            {
                'email': reqEmail,
                'username': request.json['username'],
                'password': sha256_crypt.encrypt(request.json['password'])
            }
        )
        return {"message": "success"}, 201

    def check_user(self, username):
        return db.users.find_one({'username': username})


class LoginUser(Resource):
    def post(self):
        user = db.users.find_one({'email': request.json['email']})
        if user == None:
            return {"message": "user does not exist"}, 404
        verified = sha256_crypt.verify(
            request.json['password'], user['password'])
        if verified:
            token = jwt.encode(
                payload={"email": request.json['email']}, key='jwtsecret', algorithm='HS256')
            return {
                "message": "correct password",
                "token": token
            }, 200
        else:
            return {"message": "wrong password"}, 401


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


class SendOtp(Resource):

    def post(self):
        print(request.json['email'])
        user = db.users.find_one({'email': request.json['email']})
        if user:
            return {'message': 'user already exists'}, 409
        user = db.users.find_one({'username': request.json['username']})
        if user:
            return {'message': 'user already exists'}, 409
        otp = generateOTP()
        db.otps.delete_one({'email': request.json['email']})
        db.otps.insert_one({'email': request.json['email'], 'otp': otp})

        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "noreply@utility.my.to",
                        "Name": "Utility Server"
                    },
                    "To": [
                        {
                            "Email": request.json['email'],
                        }
                    ],
                    "Subject": "OTP Verification for Utility Server",
                    "TextPart": "Your OTP for Utility Server is " + otp,
                }
            ]
        }
        result = mailjet.send.create(data=data)
        print(result.json())
        return {"message": "Otp Sent"}, 200
