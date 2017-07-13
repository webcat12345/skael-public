**User registration**

In current state of affairs, we have APIs to register/verify token/login/logout a user. On a high level the APIs are (args in sub bullets):

- POST /users (Creates a new new user)
  - plaintext\_password: String (The user&#39;s plaintext password)
- POST /users (Creates a new user)
  - plaintext\_password: String (The user&#39;s plaintext password)
  - email: String (The user&#39;s email)
  - username: String (THe user&#39;s desired username)
- PUT /users/{userId} (Creates a new user)
  - See above documentation. ALl of those fields are changeable.
- DELETE /users/{userId}
  - Soft deletes the user `userId`.
- POST /auth (Logs a user in)
  - RETURN: {&quot;access\_token&quot;: &quot;...&quot;}. Set the `access_token` in the header `Authorization: Jwt ...` where elipsis are replaced with JWT.
  - username: String
  - password: String
- POST /users/verify (Verifies a user account)
  - email: String (THe email of hte user to verify
- PUT /users/verify (Regenerates and remails the new verification token)
  - email: String (The email to regenerate the verification token for
- POST /users/reset\_password (Resets a user&#39;s password).
  - token: String
  - plaintext\_password: String
- PUT /users/reset\_password (Generates a reset password token and emails it to the user).
  - email: String

Most of these endpoints return a structure similar to:


```
{

  "email": "....",

  "username": "...",

  "public_id": "...",

  "is_validated": Boolean

}
```


**How to Use Refreshing JWTs**

Whenever a request is made, if the user is authenticated, and, finally, the request was OK (HTTP: 200), a header will be added to the response. The header will be titled `new_jwt`. If the header is present, whatever the currently stored value for `new_jwt` ought to be replaced with the new value. The previous JWT will remain viable until expiration, but will not be refreshed.

How I&#39;ve handled it on frontends in the past is to add an interceptor to whatever HTTP library you&#39;re using and to commit to whatever state management system utilized in the frontend.

So, if the HTTP request library axios is being used, I&#39;ve used the following before:

[https://pastebin.com/bALXaqj7](https://pastebin.com/bALXaqj7)

This presumes that the state management system you&#39;re using is already storing the JWT.


**Persistent Logins**

I would take the following advice with a grain of salt, should you know better, but how I would personally handle long-term sessions is to store the JWT in localStorage. Then whenever a user revisits a page within the app, I would attempt to load the JWT and see if it&#39;s verified (see below). If it is verified, I would toggle the &quot;logged in&quot; and then continue to make requests with that JWT.

**How to verify the JWT:**

Send a GET request to `/users/auth`. If successful, you will get a 200 back. If not valid, you will get a 401.

**How to signal a long-term session (&quot;Keep me logged in&quot;):**

Should a &quot;Keep me logged in&quot; button be pressed in, the header &quot;KeepLoggedIn: True&quot; should be sent within the request to the /auth endpoint. This will create a token lasting a long, configurable amount. Currently 30 days.


**Verifying Tokens:**

For this implementation, the frontend will need to implement a route which handles /users/verify/{tokenId} where tokenId is a UUID. The workflow for registering account:

1. POST /users/
2. User checks email and clicks link which takes them to the frontend app
3. The frontend app parses the URI to retrieve the token
4. POST the token to /users/verify as {token: &lt;token&gt;}
  1. 200 for success
  2. 404 for invalid token

**Logging out:**

1. DELETE to /users/auth w/ the JWT

This will manually invalidate any previous valid token for the session.


**Logging in:**

1. POST to /auth
  1. {username: &lt;username&gt;, password: &lt;password&gt;}

As mentioned above, if &quot;KeepLoggedIn&quot; is passed in (as a header) with a truthy value (including a string), the duration the JWT is valid for will be automatically set to 30 days (a configurable value).
