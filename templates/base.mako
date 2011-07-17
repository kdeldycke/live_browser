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
        %if me:
           <div>
              Logged in as: ${me['name']} |
              <a href="${me['link']}" target="_blank">Windows Live profile</a>
           </div>
        %endif
        ${next.body()}
        <div>
                <p>Debug info:</p>
                <ul>
                    <li>Number of active session: ${len(cherrypy.session)}</li>
                </ul>
                <p>Session info:</p>
                <ul>
                    <li>Session ID: ${cherrypy.session.id}</li>
                    %for (k, v) in cherrypy.session.items():
                        <li>${k}: ${v}</li>
                    %endfor
                </ul>
        </div>
    </body>
</html>
