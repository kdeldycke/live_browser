<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <%block name="head"/>
        <base href="${cherrypy.request.base}/"/>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <title>
            Live Browser &mdash;
            <%block name="title"/>
        </title>
    </head>
    <body>
        ${next.body()}
    </body>
</html>
