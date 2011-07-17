<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <base href="${cherrypy.request.base}/"/>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <title>Live Browser</title>
    </head>
    <body>
        <h1>Hello World !</h1>
        <p>Login:</p>
        <form action="/login">
           <input type="text" id="login" name="login"/>
        </form>
        <p>${content}</p>
        <a href="https://oauth.live.com/authorize?client_id=000000004C05390D&scope=wl.signin%20wl.basic&response_type=code&redirect_uri=${cherrypy.request.base}/callback">Login with your Windows Live account</a>
    </body>
</html>
