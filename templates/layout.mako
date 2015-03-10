# -*- coding: utf-8 -*- 
<!DOCTYPE html>  
<!--[if IE 9]><html class="lt-ie10" lang="en" > <![endif]-->
<html class="no-js" lang="en" >
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>app</title>

    <!-- Latest compiled and minified CSS (Bootstrap)-->
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">

    <!-- Optional theme -->
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap-theme.min.css">

    <!-- Latest compiled and minified JavaScript -->
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>

    <!-- (End Bootstrap)-->

    <link rel="stylesheet" href="/static/css/login.css">

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

  <div id="page">

##    <nav class="top-bar" data-topbar>
##  <ul class="title-area">
##    <li class="name">
##      <h1><a href="#">testboot</a></h1>
##    </li>
##    <li class="toggle-topbar menu-icon"><a href="#"><span>Menu</span></a></li>
##  </ul>
##
##  <section class="top-bar-section">
##    <!-- Right Nav Section -->
##    <ul class="right">
##        % if request.user and request.user.username:
##            <li class="active"><a href="${request.route_url('user_account', username=request.user.username)}">Account</a></li>
##        % else:
##            <li class="active"><a href="${request.route_url('login')}">Sign In</a></li>
##        % endif
##
##    </ul>
##
##    <!-- Left Nav Section -->
##    <ul class="left">
##      <!--li><a href="#">Left Nav Button</a></li-->
##    </ul>
##  </section>
##</nav>

    ${next.body()}

  </div>
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
