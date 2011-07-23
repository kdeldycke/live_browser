<!doctype html>
<!--[if lt IE 7 ]> <html lang="en" class="no-js ie6"> <![endif]-->
<!--[if IE 7 ]>    <html lang="en" class="no-js ie7"> <![endif]-->
<!--[if IE 8 ]>    <html lang="en" class="no-js ie8"> <![endif]-->
<!--[if IE 9 ]>    <html lang="en" class="no-js ie9"> <![endif]-->
<!--[if (gt IE 9)|!(IE)]><!--> <html lang="en" class="no-js"> <!--<![endif]-->
<head>
    <%block name="head"/>
    <base href="${cherrypy.request.base}/"/>

    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

    <title>
        Live Browser &mdash;
        <%block name="title"/>
    </title>
    <meta name="description" content="Windows Live API Browser">
    <meta name="author" content="Kevin Deldcyke">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link rel="shortcut icon" href="/favicon.ico">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <link rel="stylesheet" href="css/style.css?v=1">
    <link rel="stylesheet" media="handheld" href="css/handheld.css?v=1">
    <script src="js/libs/modernizr-1.7.min.js"></script>
</head>
<body>

    <div id="container">

        <header>
            %if me:
                <div>
                    Logged in as: ${me['name']} |
                    <a href="${me['link']}" target="_blank">Windows Live profile</a> |
                    <a href="/logout">log out</a>
                </div>
            %endif
        </header>

        <div id="main" role="main">
            ${next.body()}
        </div>

        <footer>
            <p>Debug info:</p>
            <ul>
                <li>Number of active session: ${len(cherrypy.session)}</li>
            </ul>
            <p>Session data:</p>
            <ul>
                <li>Session ID: ${cherrypy.session.id}</li>
                %for (k, v) in cherrypy.session.items():
                    <li>${k}: ${v}</li>
                %endfor
            </ul>
        </footer>

    </div>

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js"></script>
    <script>!window.jQuery && document.write(unescape('%3Cscript src="js/libs/jquery-1.5.1.min.js"%3E%3C/script%3E'))</script>
    <script src="js/plugins.js"></script>
    <script src="js/script.js"></script>

    <!--[if lt IE 7 ]>
    <script src="js/libs/dd_belatedpng.js"></script>
    <script> DD_belatedPNG.fix('img, .png_bg');</script>
    <![endif]-->

    <script>
        var _gaq=[['_setAccount','UA-XXXXX-X'],['_trackPageview']]; // Change UA-XXXXX-X to be your site's ID
        (function(d,t){var g=d.createElement(t),s=d.getElementsByTagName(t)[0];g.async=1;
        g.src=('https:'==location.protocol?'//ssl':'//www')+'.google-analytics.com/ga.js';
        s.parentNode.insertBefore(g,s)}(document,'script'));
    </script>

</body>
</html>