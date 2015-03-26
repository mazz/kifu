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

        <!-- getting jquery-latest AFTER bootstrap above seems to fix topbar menu from disappearing -->
    <script src="http://code.jquery.com/jquery-latest.js"></script>

    <link rel="stylesheet" href="/static/css/login.css">

    <!-- Latest compiled and minified JavaScript -->
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>

    <!-- (End Bootstrap)-->



##        <!-- Bootstrap Core CSS -->
##    <link href="../static/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
##
##    <!-- MetisMenu CSS -->
##    <link href="../static/metisMenu/dist/metisMenu.min.css" rel="stylesheet">
##
##    <!-- Timeline CSS -->
##    <link href="../static/dist/css/timeline.css" rel="stylesheet">
##
##    <!-- Custom CSS -->
##    <link href="../static/dist/css/sb-admin-2.css" rel="stylesheet">
##
##    <!-- Morris Charts CSS -->
##    <link href="../static/morrisjs/morris.css" rel="stylesheet">

    <!-- Custom Fonts -->
    <link href="/foo/static/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->


##    <!-- Bootstrap Core CSS -->
##    <link href="/bootstrap.min.css">
##
##    <!-- MetisMenu CSS -->
##    <link href="/static/metisMenu/dist/metisMenu.min.css" rel="stylesheet">
##
##    <!-- Custom CSS -->
##    <link href="/static/dist/css/sb-admin-2.css" rel="stylesheet">
##
##    <!-- Custom Fonts -->
##    <link href="/static/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">
##
##    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
##    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
##    <!--[if lt IE 9]>
##        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
##        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
##    <![endif]-->



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
            <a href="#" class="navbar-brand">foo</a>
        </div>
        <!-- Collection of nav links, forms, and other content for toggling -->
        <div id="navbarCollapse" class="collapse navbar-collapse">
            <ul class="nav navbar-nav">
##                <li class="active"><a href="#">Home</a></li>
##                <li><a href="#">Profile</a></li>
##                <li class="dropdown">
##                    <a data-toggle="dropdown" class="dropdown-toggle" href="#">Messages <b class="caret"></b></a>
##                    <ul role="menu" class="dropdown-menu">
##                        <li><a href="#">Inbox</a></li>
##                        <li><a href="#">Drafts</a></li>
##                        <li><a href="#">Sent Items</a></li>
##                        <li class="divider"></li>
##                        <li><a href="#">Trash</a></li>
##                    </ul>
##                </li>
            </ul>
##            <form role="search" class="navbar-form navbar-left">
##                <div class="form-group">
##                    <input type="text" placeholder="Search" class="form-control">
##                </div>
##            </form>
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




##  <div id="page">
##
##              <!-- Navigation -->
##        <nav class="navbar navbar-default navbar-static-top" role="navigation" style="margin-bottom: 0">
##            <div class="navbar-header">
##                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
##                    <span class="sr-only">Toggle navigation</span>
##                    <span class="icon-bar"></span>
##                    <span class="icon-bar"></span>
##                    <span class="icon-bar"></span>
##                </button>
####                <a class="navbar-brand" href="index.html">SB Admin v2.0</a>
##            </div>
##            <!-- /.navbar-header -->
##
##            <ul class="nav navbar-top-links navbar-right">


                ##        % if request.user and request.user.username:
##            <li class="active"><a href="${request.route_url('user_account', username=request.user.username)}">Account</a></li>
##        % else:
##            <li class="active"><a href="${request.route_url('login')}">Sign In</a></li>
##        % endif

##                <!-- /.dropdown -->
##                % if request.user and request.user.username:
##                <li class="dropdown">
##                    <a class="dropdown-toggle" data-toggle="dropdown" href="#">
##                        <i class="fa fa-user fa-fw"></i>  <i class="fa fa-caret-down"></i>
##                    </a>
##                    <ul class="dropdown-menu dropdown-user">
##                        <li><a href="#"><i class="fa fa-user fa-fw"></i> User Profile</a>
##                        </li>
####                        <li><a href="#"><i class="fa fa-gear fa-fw"></i> Settings</a>
####                        </li>
##                        <li class="divider"></li>
##                        <li><a href="${request.route_url('logout')}"><i class="fa fa-sign-out fa-fw"></i> Logout</a>
##                        </li>
##                    </ul>
##                    <!-- /.dropdown-user -->
##                </li>
##                <!-- /.dropdown -->
##                % endif
##
##
##            </ul>
##            <!-- /.navbar-top-links -->
##
##
##                <!-- /.sidebar-collapse -->
##            </div>
##            <!-- /.navbar-static-side -->
##        </nav>


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
