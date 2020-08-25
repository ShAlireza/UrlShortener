""" API 1.

Name: ShortenURLAPIView

URL: localhost:8000/r/short-url

Method: POST

Description: Add new long url to make it short

    Header : {Authorization: Token [Token Returned from login]}


  Request json example: 
"""

Json_1 = {

    "long_url": "https://google.com",
    "suggested_path": "google"  # Optional field

}

""" API 2.

Name: ShortenURLAPIView

URL: localhost:8000/r/short-url

Method: GET

Description: Get urls analytics of a user

    Header : {Authorization: Token [Token Returned from login]}


  Request json example: 
"""

Json_2 = {

    # Leave Emtpy if not needed

}

""" API 3.

Name: RedirectAPIView

URL: localhost:8000/r/<slug>

Method: GET

Description: Redirect the short to the real long url


  Request json example: 
"""

Json_3 = {

    # Leave Emtpy if not needed

}
