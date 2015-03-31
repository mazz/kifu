<%inherit file="/layout.mako" />
<%def name="title()">Account Information: ${user.username}</%def>

<%namespace file="func.mako" import="account_nav, password_reset"/>
<%
    date_fmt = "%m/%d/%Y"
%>

    <script src="/static/js/password-validation.js"></script>

    <div id="wrapper">
        <div id="page-wrapper">
            <div class="row">
                <div class="col-lg-8 col-sm-offset-2">
                    <h1 class="page-header">User Profile</h1>
                </div>
                <!-- /.col-lg-12 -->
            </div>
            <!-- /.row -->
            <div class="row">
                <div class="col-lg-8 col-sm-offset-2">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-dashboard fa-fw"></i> Account Information
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
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

                                <a href="#" id="view_api_key" class="list-group-item">
                                    <i class="fa fa-key fa-fw"></i> API Key

                                    <button type="submit" class="btn btn-default pull-right btn-xs" id="view_api_key_button"> View API Key</button>
                                    <span class="pull-right text-muted small" id="view_api_key_value" hidden>
                                    </span>
                                </a>
                            </div>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                    <!-- /.panel -->
                    <div class="panel panel-default">
##                        <div class="panel-heading">
##                            <i class="fa fa-clock-o fa-fw"></i> Settings
##                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">

    <form class="form-horizontal" role="form">
    <div class="form-group">
      <label class="control-label col-sm-2" for="email">Username:</label>
      <div class="col-sm-8">
          <p class="form-control-static">${user.username}</p>
##        <input type="email" class="form-control" id="new_username" placeholder="">
      </div>
    </div>
    <div class="form-group">
      <label class="control-label col-sm-2" for="email">Name:</label>
      <div class="col-sm-8">
        <input type="text" class="form-control" id="name" placeholder="${user.name}" maxlength="64">
      </div>
    </div>
    <div class="form-group">
      <div class="col-sm-offset-2 col-sm-10">
        <button type="submit" class="btn btn-default" id="submit_account_change">Update</button>
      </div>
    </div>
  </form>

##                            <a href="#" class="list-group-item">
##    </a>
##    <a href="#" class="list-group-item">
##                            </a>

                        </div>

                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                    <div class="panel panel-default col-sm-8">
##                        <div class="panel-heading">
##                            <i class="fa fa-clock-o fa-fw"></i> Settings
##                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">

##                            <a href="#" class="list-group-item">
##    </a>
##    <a href="#" class="list-group-item">
  <form method="POST" id="passwordForm" class="form-horizontal" role="form">
    <input type="hidden" name="username" id="username" value="${user.username}" />
    <div class="form-group">
      <label class="control-label col-sm-2" for="email">Change Password:</label>

      <div class="col-sm-10">
        <input type="password" class="form-control" name="password1" id="password1" placeholder="New Password" autocomplete="off">
      </div>
      <div class="col-sm-10"></br>
        <input type="password" class="form-control" name="password2" id="password2" placeholder="Repeat Password" autocomplete="off">
      </div>
    </div>
    <div class="form-group">
      <div class="col-sm-6 col-sm-offset-2">
        <button type="submit" class="btn btn-default" id="change_password">Change Password</button>
      </div>
    </div>
  </form>

</div>

                        <!-- /.panel-body -->
                    </div>
                    <div class="panel panel-default col-sm-4">
##                        <div class="panel-heading">
##                            <i class="fa fa-clock-o fa-fw"></i> Settings
##                        </div>
                        <!-- /.panel-heading -->
##                        <div class="panel-body">

##                            <a href="#" class="list-group-item">
##    </a>
                        <!-- /.panel-heading -->
##                        <div class="panel-body">
                            <div class="list-group">
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-comment fa-fw"></i> 8 Characters Long
                                    <span id="8char" class="pull-right glyphicon glyphicon-remove" style="color:#FF0004;"></span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-twitter fa-fw"></i> One Uppercase Letter
                                    <span id="ucase" class="pull-right glyphicon glyphicon-remove" style="color:#FF0004;"></span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-envelope fa-fw"></i> One Lowercase Letter
                                    <span id="lcase" class="pull-right glyphicon glyphicon-remove" style="color:#FF0004;"></span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-tasks fa-fw"></i> One Number
                                    <span id="num" class="pull-right glyphicon glyphicon-remove" style="color:#FF0004;"></span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-upload fa-fw"></i> Passwords Match
                                    <span id="pwmatch" class="pull-right glyphicon glyphicon-remove" style="color:#FF0004;"></span>
                                </a>
                            </div>
                            <!-- /.list-group -->
##                        </div>
                        <!-- /.panel-body -->
                    <!-- /.panel -->
                    <!-- /.panel -->
                    <!-- /.panel .chat-panel -->

##                        </div>

                        <!-- /.panel-body -->
                    </div>

                </div>

                <!-- /.col-lg-8 -->
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
       $('#view_api_key_button').prepend(" <i class='fa fa-spinner fa-spin'></i>");
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
                    $('#view_api_key_button').hide();

##                    $('#view_api_key_button').remove("i");
                    $("span[id*=view_api_key_value]").text(api_key);
                    $("span[id*=view_api_key_value]").show();
                }
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                var message;
                console.log("suspend fail");
                $("span[id*=view_api_key_value]").text('There was an error obtaining your API key. Try later.');
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
                        name: $("#name").val()
                        });

        account_change_url = APP_URL + "/api/v1/" + '${user.username}' + "/account?api_key=" + '${request.user.api_key}';
        $.ajax({
            type: "POST",   
            url: account_change_url,
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
