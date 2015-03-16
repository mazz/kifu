<%inherit file="/layout.mako" />
<%def name="title()">Account Information: ${user.username}</%def>

<%namespace file="func.mako" import="account_nav, password_reset"/>
<%
    date_fmt = "%m/%d/%Y"
%>

##<div class="panel">
##    <div class="row">
##        <div class="large-4 columns">
##            <h3>Account Information</h3>
##                <h5>${user.username}</h5>
##                <h5>Member since:
##                    % if user.signup:
##                        ${user.signup.strftime(date_fmt)}
##                    % else:
##                        Unknown
##                    % endif
##                <h5>
##                <h5>Last Seen: <span>
##                    % if user.last_login:
##                        ${user.last_login.strftime(date_fmt)}
##                    % else:
##                        Not logged in
##                    % endif
##                <h5>
##            </div>
##
##            <div class="large-8 columns">
##                <form>
##                    <h5>Name</h5>
##                    <input type="text" id="name" name="name" value="${user.name}" />
##                    <h5>Email</h5>
##                    <input type="email" id="email" name="email" value="${user.email}" />
##                    <div class="row">
##                    <div class="small-3 columns">
##                        <input type="button" id="submit_account_change" value="Update" class="button" class="postfix small button expand"/>
##                    </div>
##                    </div>
##                        <div class="row">
##                            <div class="large-12 columns">
##                            <div id="account_msg" class="error"></div>
##                        </div>
##                    </div>
##                </form>
##            </div>
##    </div>
##</div>
##
##% if user.has_invites():
##<div id="invite_container">
##</div>
##% endif
##
##<div class="panel">
##    <div class="row">
##        <div class="large-4 columns">
##            <a href="#" id="view_api_key" class="heading">
##            <span aria-hidden="true" class="icon icon-lock" title="View API Key"></span>
##            <h3>View API Key</h3></a>
##        </div>
##
##        <div class="large-8 columns">
##            <div id="view_api_key_view" style="display: none; opacity: 0;">
##            </div>
##            <div class="row">
##                <div class="large-12 columns">
##                    <div data-alert class="" id="view_api_status">
##                    </div>
##                </div>
##            </div>
##
##            <div id="password_msg" class="error" style="opacity: 0;"></div>
##        </div>
##    </div>
##</div>
##
##${password_reset(user, reset=False)}
##
##<%def name="add_js()">
##    <script type="text/javascript">
##        /*
##        YUI().use('node', 'bookie-view', 'console', function (Y) {
##            Y.on('domready', function () {
##                var api_cfg = {
##                    url: APP_URL + '/api/v1',
##                    username: '${request.user.username}',
##                    api_key: '${request.user.api_key}',
##                },
##                account_view = new Y.bookie.AccountView({
##                    api_cfg: api_cfg
##                });
##
##                % if user.has_invites():
##                    var invite_view = new Y.bookie.InviteView({
##                        api_cfg: api_cfg,
##                        user: {
##                            invite_ct: ${user.invite_ct}
##                        }
##                    });
##                    invite_view.render();
##                % endif
##            });
##        });
##        */
##    </script>
##</%def>


    <div id="wrapper">

        <!-- Navigation -->
            <!-- /.navbar-top-links -->

            <div class="navbar-default sidebar" role="navigation">
                <div class="sidebar-nav navbar-collapse">
                    <ul class="nav" id="side-menu">
##                        <li class="sidebar-search">
##                            <div class="input-group custom-search-form">
##                                <input type="text" class="form-control" placeholder="Search...">
##                                <span class="input-group-btn">
##                                <button class="btn btn-default" type="button">
##                                    <i class="fa fa-search"></i>
##                                </button>
##                            </span>
##                            </div>
##                            <!-- /input-group -->
##                        </li>
                        <li>
                            <a href="#"><i class="fa fa-dashboard fa-fw"></i> User Profile</a>
                        </li>
                        <li>
                            <a href="#"><i class="fa fa-key fa-fw"></i> Change Password</a>
                        </li>
                    </ul>
                </div>
                <!-- /.sidebar-collapse -->
            </div>
            <!-- /.navbar-static-side -->
        </nav>

        <div id="page-wrapper">
            <div class="row">
                <div class="col-lg-12">
                    <h1 class="page-header">User Profile</h1>
                </div>
                <!-- /.col-lg-12 -->
            </div>
            <!-- /.row -->
            <div class="row">
                <div class="col-lg-8">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-dashboard fa-fw"></i> Account Information
##                            <div class="pull-right">
##                                <div class="btn-group">
##                                    <button type="button" class="btn btn-default btn-xs dropdown-toggle" data-toggle="dropdown">
##                                        Actions
##                                        <span class="caret"></span>
##                                    </button>
##                                    <ul class="dropdown-menu pull-right" role="menu">
##                                        <li><a href="#">Action</a>
##                                        </li>
##                                        <li><a href="#">Another action</a>
##                                        </li>
##                                        <li><a href="#">Something else here</a>
##                                        </li>
##                                        <li class="divider"></li>
##                                        <li><a href="#">Separated link</a>
##                                        </li>
##                                    </ul>
##                                </div>
##                            </div>
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">

                            ##                <h5>${user.username}</h5>
##                <h5>Member since:
##                    % if user.signup:
##                        ${user.signup.strftime(date_fmt)}
##                    % else:
##                        Unknown
##                    % endif
##                <h5>
##                <h5>Last Seen: <span>
##                    % if user.last_login:
##                        ${user.last_login.strftime(date_fmt)}
##                    % else:
##                        Not logged in
##                    % endif
##                <h5>
                               <div class="list-group">
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-clock-o fa-fw"></i> Member since
                                    <span class="pull-right text-muted small"><em>
                                        % if user.signup:
                                            ${user.signup.strftime(date_fmt)}
                                        % else:
                                            Unknown
                                        % endif
                                        </em>
                                    </span>
                                </a>

                                <a href="#" class="list-group-item">
                                    <i class="fa fa-clock-o fa-fw"></i> Last Seen
                                    <span class="pull-right text-muted small"><em>
                                        % if user.last_login:
                                            ${user.last_login.strftime(date_fmt)}
                                        % else:
                                            Not logged in
                                        % endif
                                        </em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-envelope fa-fw"></i> Email
                                    <span class="pull-right text-muted small"><em>${user.email}</em>
                                        </span>
                                </a>

                                <a href="#" class="list-group-item">
                                    <i class="fa fa-key fa-fw"></i> API Key
                                    <button type="submit" class="btn btn-default pull-right btn-xs">View API Key</button>
                                </a>
                            </div>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                    <!-- /.panel -->
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-clock-o fa-fw"></i> Settings
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">

                            <a href="#" class="list-group-item">
  <form class="form-horizontal" role="form">
    <div class="form-group">
      <label class="control-label col-sm-2" for="email">Username:</label>
      <div class="col-sm-10">
        <input type="email" class="form-control" id="new_username" placeholder="${user.name}">
      </div>
    </div>
    <div class="form-group">
      <div class="col-sm-offset-2 col-sm-10">
        <button type="submit" class="btn btn-default">Update</button>
      </div>
    </div>
  </form>
                            </a>

                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                </div>
                <!-- /.col-lg-8 -->
                <div class="col-lg-4">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-bell fa-fw"></i> Notifications Panel
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
                            <div class="list-group">
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-comment fa-fw"></i> New Comment
                                    <span class="pull-right text-muted small"><em>4 minutes ago</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-twitter fa-fw"></i> 3 New Followers
                                    <span class="pull-right text-muted small"><em>12 minutes ago</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-envelope fa-fw"></i> Message Sent
                                    <span class="pull-right text-muted small"><em>27 minutes ago</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-tasks fa-fw"></i> New Task
                                    <span class="pull-right text-muted small"><em>43 minutes ago</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-upload fa-fw"></i> Server Rebooted
                                    <span class="pull-right text-muted small"><em>11:32 AM</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-bolt fa-fw"></i> Server Crashed!
                                    <span class="pull-right text-muted small"><em>11:13 AM</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-warning fa-fw"></i> Server Not Responding
                                    <span class="pull-right text-muted small"><em>10:57 AM</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-shopping-cart fa-fw"></i> New Order Placed
                                    <span class="pull-right text-muted small"><em>9:49 AM</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-money fa-fw"></i> Payment Received
                                    <span class="pull-right text-muted small"><em>Yesterday</em>
                                    </span>
                                </a>
                            </div>
                            <!-- /.list-group -->
                            <a href="#" class="btn btn-default btn-block">View All Alerts</a>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-bar-chart-o fa-fw"></i> Donut Chart Example
                        </div>
                        <div class="panel-body">
                            <div id="morris-donut-chart"></div>
                            <a href="#" class="btn btn-default btn-block">View Details</a>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                    <div class="chat-panel panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-comments fa-fw"></i>
                            Chat
                            <div class="btn-group pull-right">
                                <button type="button" class="btn btn-default btn-xs dropdown-toggle" data-toggle="dropdown">
                                    <i class="fa fa-chevron-down"></i>
                                </button>
                                <ul class="dropdown-menu slidedown">
                                    <li>
                                        <a href="#">
                                            <i class="fa fa-refresh fa-fw"></i> Refresh
                                        </a>
                                    </li>
                                    <li>
                                        <a href="#">
                                            <i class="fa fa-check-circle fa-fw"></i> Available
                                        </a>
                                    </li>
                                    <li>
                                        <a href="#">
                                            <i class="fa fa-times fa-fw"></i> Busy
                                        </a>
                                    </li>
                                    <li>
                                        <a href="#">
                                            <i class="fa fa-clock-o fa-fw"></i> Away
                                        </a>
                                    </li>
                                    <li class="divider"></li>
                                    <li>
                                        <a href="#">
                                            <i class="fa fa-sign-out fa-fw"></i> Sign Out
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
                            <ul class="chat">
                                <li class="left clearfix">
                                    <span class="chat-img pull-left">
                                        <img src="http://placehold.it/50/55C1E7/fff" alt="User Avatar" class="img-circle" />
                                    </span>
                                    <div class="chat-body clearfix">
                                        <div class="header">
                                            <strong class="primary-font">Jack Sparrow</strong>
                                            <small class="pull-right text-muted">
                                                <i class="fa fa-clock-o fa-fw"></i> 12 mins ago
                                            </small>
                                        </div>
                                        <p>
                                            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur bibendum ornare dolor, quis ullamcorper ligula sodales.
                                        </p>
                                    </div>
                                </li>
                                <li class="right clearfix">
                                    <span class="chat-img pull-right">
                                        <img src="http://placehold.it/50/FA6F57/fff" alt="User Avatar" class="img-circle" />
                                    </span>
                                    <div class="chat-body clearfix">
                                        <div class="header">
                                            <small class=" text-muted">
                                                <i class="fa fa-clock-o fa-fw"></i> 13 mins ago</small>
                                            <strong class="pull-right primary-font">Bhaumik Patel</strong>
                                        </div>
                                        <p>
                                            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur bibendum ornare dolor, quis ullamcorper ligula sodales.
                                        </p>
                                    </div>
                                </li>
                                <li class="left clearfix">
                                    <span class="chat-img pull-left">
                                        <img src="http://placehold.it/50/55C1E7/fff" alt="User Avatar" class="img-circle" />
                                    </span>
                                    <div class="chat-body clearfix">
                                        <div class="header">
                                            <strong class="primary-font">Jack Sparrow</strong>
                                            <small class="pull-right text-muted">
                                                <i class="fa fa-clock-o fa-fw"></i> 14 mins ago</small>
                                        </div>
                                        <p>
                                            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur bibendum ornare dolor, quis ullamcorper ligula sodales.
                                        </p>
                                    </div>
                                </li>
                                <li class="right clearfix">
                                    <span class="chat-img pull-right">
                                        <img src="http://placehold.it/50/FA6F57/fff" alt="User Avatar" class="img-circle" />
                                    </span>
                                    <div class="chat-body clearfix">
                                        <div class="header">
                                            <small class=" text-muted">
                                                <i class="fa fa-clock-o fa-fw"></i> 15 mins ago</small>
                                            <strong class="pull-right primary-font">Bhaumik Patel</strong>
                                        </div>
                                        <p>
                                            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur bibendum ornare dolor, quis ullamcorper ligula sodales.
                                        </p>
                                    </div>
                                </li>
                            </ul>
                        </div>
                        <!-- /.panel-body -->
                        <div class="panel-footer">
                            <div class="input-group">
                                <input id="btn-input" type="text" class="form-control input-sm" placeholder="Type your message here..." />
                                <span class="input-group-btn">
                                    <button class="btn btn-warning btn-sm" id="btn-chat">
                                        Send
                                    </button>
                                </span>
                            </div>
                        </div>
                        <!-- /.panel-footer -->
                    </div>
                    <!-- /.panel .chat-panel -->
                </div>
                <!-- /.col-lg-4 -->
            </div>
            <!-- /.row -->
        </div>
        <!-- /#page-wrapper -->

    </div>
    <!-- /#wrapper -->


##    <!-- jQuery -->
##    <script src="../../static/jquery/dist/jquery.min.js"></script>
##
##    <!-- Bootstrap Core JavaScript -->
##    <script src="../../static/bootstrap/dist/js/bootstrap.min.js"></script>

    <!-- Metis Menu Plugin JavaScript -->
##    <script src="../../static/metisMenu/dist/metisMenu.min.js"></script>

    <!-- Morris Charts JavaScript -->
##    <script src="../../static/raphael/raphael-min.js"></script>
##    <script src="../../static/morrisjs/morris.min.js"></script>
##    <script src="../../static/js/morris-data.js"></script>

    <!-- Custom Theme JavaScript -->
##    <script src="../../static/dist/js/sb-admin-2.js"></script>


<script type="text/javascript">
            $(function() {
    $('#show_password').click(function() {
        window.console&&console.log('show_password');
        $('#password_change').slideToggle();
        $("#password_change").css({ opacity: 1. });
    });

    $('#view_api_key').click(function()
    {
        window.console&&console.log('view_api_key');
        $('#view_api_key_view').slideToggle();
        $("#view_api_key_view").css({ opacity: 1. });

        var formData = JSON.stringify({
                        username: '${user.username}',
                        api_key: '${request.user.api_key}'
                        });

        var resultString;
        $.ajax({
            type: "POST",   
            url: APP_URL + "/api/v1/" + '${user.username}' + "/api_key",
            data: formData,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data, textStatus, jqXHR)
            {
                var api_key;
                console.log("suspend success: " + data);

                for(key in data) {
                    if (key === "api_key")
                    {
                        console.log("found success");
                        api_key = data[key];
                    }

                    console.log("key: " + key);
                    console.log("value: " + data[key]);
                }

                $('#view_api_key_view').html(api_key);
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                var message;
                console.log("suspend fail");
                $('#view_api_key_view').html("There was an error obtaining your API key.");
            }
        });
    });

    $('#submit_password_change').click(function()
    {

        console.log("submit_password_change, api_key: " + '${request.user.api_key}');
        $('#changepassword-status').removeClass('alert-box').removeClass('warning').removeClass('round').removeClass('success').removeClass('radius');
        $('#changepassword-status').html("");

        var formData = JSON.stringify({
                        username: '${user.username}',
                        current_password: $("#current_password").val(),
                        new_password: $("#new_password").val(),
                        api_key: '${request.user.api_key}'
                        });

        $.ajax({
            type: "POST",   
            url: APP_URL + "/api/v1/" + '${user.username}' + "/password",
            data: formData,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data, textStatus, jqXHR)
            {
                var message;
                console.log("suspend success: " + data);

                for(key in data) {
                    if (key === "message")
                    {
                        console.log("found success");
                        message = data[key];
                    }

                    console.log("key: " + key);
                    console.log("value: " + data[key]);
                }
                $('#changepassword-status').removeClass('alert-box').removeClass('warning').removeClass('round').addClass('success').addClass('radius').addClass('alert-box');
                $('#forgotten_password_panel').slideToggle();

                $('#changepassword-status').html(message);
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                var message;
                console.log("suspend fail");
                $('#changepassword-status').removeClass('alert-box').removeClass('success').removeClass('radius').addClass('warning').addClass('round').addClass('alert-box');
                $('#forgotten_password_panel').slideToggle();

                $('#changepassword-status').html(textStatus);
            }
        });

    });

    $('#submit_account_change').click(function()
    {

        console.log("submit_account_change, api_key: " + '${request.user.api_key}');
        $('#changepassword-status').removeClass('alert-box').removeClass('warning').removeClass('round').removeClass('success').removeClass('radius');
        $('#changepassword-status').html("");

        var formData = JSON.stringify({
                        name: $("#name").val(),
                        email: $("#email").val(),
                        });

        $.ajax({
            type: "POST",   
            url: APP_URL + "/api/v1/" + '${user.username}' + "/account",
            data: formData,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data, textStatus, jqXHR)
            {
                var message;
                console.log("account change success: " + data);

                for(key in data) {
                    if (key === "message")
                    {
                        console.log("found success");
                        message = data[key];
                    }

                    console.log("key: " + key);
                    console.log("value: " + data[key]);
                }
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                var message;
                console.log("account change fail");
            }
        });

    });

});
</script>
