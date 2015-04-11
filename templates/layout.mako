# -*- coding: utf-8 -*- 
<!DOCTYPE html>  
<!--[if IE 9]><html class="lt-ie10" lang="en" > <![endif]-->
<html class="no-js" lang="en" >
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>app</title>

    <!-- Latest compiled and minified CSS (Bootstrap)-->
    <link rel="stylesheet" href="/static/bootstrap/3.3.4/css/bootstrap.min.css">

    <!-- Optional theme -->
    <link rel="stylesheet" href="/static/bootstrap/3.3.4/css/bootstrap-theme.min.css">

        <!-- getting jquery-latest AFTER bootstrap above seems to fix topbar menu from disappearing -->
##    <script src="http://code.jquery.com/jquery-latest.js"></script>
    <script src="/static/jquery/2.1.3/jquery.min.js"></script>

    <link rel="stylesheet" href="/static/css/login.css">

    <!-- Latest compiled and minified JavaScript -->
    <script src="/static/bootstrap/3.3.4/js/bootstrap.min.js"></script>

    <!-- (End Bootstrap)-->

    <!-- Custom Fonts -->
    <link href="/static/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

    <!-- If you are using CSS version, only link these 2 files, you may add app.css to use for your overrides if you like. -->
<!--
    <link rel="stylesheet" href="/static/css/normalize.css">
    <link rel="stylesheet" href="/static/css/foundation.css">
    <script src="/static/js/vendor/custom.modernizr.js"></script>
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="http://code.jquery.com/jquery-migrate-1.2.1.min.js"></script>
-->
    <script type="text/javascript" charset="utf-8">
        <%
            app_url = request.route_url('login').rstrip('/')
        %>
        APP_URL = '${app_url}';
    </script>
</head>

<body>

    <nav role="navigation" class="navbar navbar-inverse navbar-static-top">
        <!-- Brand and toggle get grouped for better mobile display -->
        <div class="navbar-header">
            <button type="button" data-target="#navbarCollapse" data-toggle="collapse" class="navbar-toggle">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a href="#" class="navbar-brand">~~~PROJNAME~~~</a>
        </div>
        <!-- Collection of nav links, forms, and other content for toggling -->
        <div id="navbarCollapse" class="collapse navbar-collapse">
            <ul class="nav navbar-nav">
            </ul>
            <ul class="nav navbar-nav navbar-right">
                % if request.user and request.user.username:
                    <li class="active"><a href="${request.route_url('user_account', username=request.user.username)}">Profile</a></li>
                    <li class=""><a href="${request.route_url('logout')}">Logout</a></li>
                    <li><a href="#"></a></li>
                % else:
                    <li class="active"><a href="${request.route_url('login')}">Sign In</a></li>
                    <li><a href="#"></a></li>
                % endif
            </ul>
        </div>
    </nav>

    ${next.body()}

<!--
  <script src="/static/js/vendor/jquery.js"></script>
  <script src="/static/js/foundation.min.js"></script>
  <script>
    $(document).foundation();
  </script>
-->
  % if hasattr(self, 'add_js'):
            ${self.add_js()}
  % endif

</body>
</html>
