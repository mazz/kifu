<%inherit file="/layout.mako" />
##<%namespace file="../accounts/func.mako" import="password_reset"/>
##<%def name="title()">Activate your account</%def>
##
##${password_reset(user, reset=True)}

<%
    date_fmt = "%m/%d/%Y"
%>

<script src="/static/js/password-validation.js"></script>

        <div id="page-wrapper">
            <div class="row">
                <div class="col-md-8 col-md-offset-2">
                    <h1 class="page-header">Update Account</h1>
                </div>
                <!-- /.col-lg-12 -->
            </div>
            <!-- /.row -->
            <div class="row">
                <div class="col-md-4 col-md-offset-2">
                    <!-- /.panel -->
                    <!-- /.panel -->
<!--                    <div class="panel panel-default"> -->
                        <!-- /.panel-heading -->
            % if message is not '':
                <div class="alert alert-danger" role="alert" alert-dismissable>
                    <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>
                    <span class="sr-only">Error:</span>
                    ${message}
                    <button type="button" class="close" data-dismiss="alert">&times;</button>
                </div>
            % endif

            <p class="text-center">Use the form below to change your password.</p>
            <form method="POST" id="passwordForm">
                <input type="hidden" name="username" id="username" value="${user.username}" />
                <input type="hidden" name="code" id="code" value="${user.activation.code}" />
                <input type="password" class="input-lg form-control" name="password1" id="password1" placeholder="New Password" autocomplete="off">
                </br>
                <input type="password" class="input-lg form-control" name="password2" id="password2" placeholder="Repeat Password" autocomplete="off">
                </br>
                <input type="submit" class="col-xs-12 btn btn-primary btn-load btn-lg" data-loading-text="Changing Password..." value="Change Password" id="change_password">
            </form>
<!--                    </div> -->
                    <!-- /.panel -->
                </div>
                <!-- /.col-lg-8 -->
                <div class="col-lg-4">
                        <!-- /.panel-heading -->
                        <div class="panel-body">
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
                        </div>
                        <!-- /.panel-body -->
                    <!-- /.panel -->
                    <!-- /.panel -->
                    <!-- /.panel .chat-panel -->
                </div>
                <!-- /.col-lg-4 -->
            </div>
            <!-- /.row -->
        </div>
        <!-- /#page-wrapper -->
