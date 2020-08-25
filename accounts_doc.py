""" API 1.

Name: SignUpAPIView

URL: localhost:8000/api/accounts/signup

Method: POST

Description: Signup as a new user


  Request json example:
"""

Json_1 = {
    "username": "yektanet",
    "email": "yek@te.net",
    "password": "123456",
    "repeat_password": '123456'
}

""" API 2.

Name: LoginAPIView

URL: localhost:8000/api/accounts/login

Method: POST

Description: Login with provided credentials


  Request json example: 
"""

Json_2 = {

    "username": "yektanet",  # (or "yek@te.net") login with username or email
    # but the "key" must be "username" for both of them

    "password": "123456"

}

""" API 3.

Name: LogoutAPIView

URL: localhost:8000/api/accounts/logout

Method: POST

Description: Logout user

    Header : {Authorization: Token [Token Returned from login]}

  Request json example: 
"""

Json_3 = {

    # Leave Emtpy if not needed

}
