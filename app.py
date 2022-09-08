from config import app, api, PORT
from controllers import auth

api.add_resource(auth.AddUser, '/auth/add-user')
api.add_resource(auth.LoginUser, '/auth/login-user')
api.add_resource(auth.SendOtp, '/auth/send-otp')


if __name__ == '__main__':
    app.run(port=PORT, host='0.0.0.0')
