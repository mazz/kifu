<%inherit file="/layout.mako" />
##<%namespace file="../accounts/func.mako" import="password_reset"/>
##<%def name="title()">Activate your account</%def>
##
##${password_reset(user, reset=True)}

<script src="/static/js/password-validation.js"></script>

        <div id="page-wrapper">
            <div class="row">
                <div class="col-md-8 col-md-offset-2">
                    % if user.activation.created_by == 'forgot_password':
                        <h1 class="page-header">Update Account</h1>
                    % else:
                        % if user.activation.created_by == 'signup':
                            <h1 class="page-header">Create Account</h1>
                        % endif
                    % endif
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

##            <p class="text-center">Use the form below to change your password.</p>
            <p class="text-center">created_by: ${user.activation.created_by}</p>
            <p class="text-center">user.username: ${user.username}</p>

            <form method="POST" id="passwordForm" class="form-horizontal" role="form">

                % if user.activation.created_by == 'forgot_password':
                    ## if forgot password, provide user.username so we can make sure the new password is not the same as the pre-existing user.username
                    <input type="text" class="input-lg form-control" name="new_username" id="new_username" placeholder="${user.username}" autocomplete="off" maxlength="32">
##                    <input type="hidden" name="user_username" id="user_username" value="${user.username}" />
                % else:
                    % if user.activation.created_by == 'signup':
                        <input type="text" class="input-lg form-control" name="new_username" id="new_username" placeholder="Username" autocomplete="off" maxlength="32">
                    % endif
                % endif

##                <input type="text" class="input-lg form-control" name="new_username" id="new_username" placeholder="${user.username}" autocomplete="off" maxlength="32">

                </br>

##                <input type="hidden" name="username" id="username" value="${user.username}" />

                <input type="hidden" name="username" id="username" value="${user.username}" />
                <input type="hidden" name="code" id="code" value="${user.activation.code}" />
                <input type="password" class="input-lg form-control" name="password1" id="password1" placeholder="New Password" autocomplete="off">
                </br>
                <input type="password" class="input-lg form-control" name="password2" id="password2" placeholder="Repeat Password" autocomplete="off">
                </br>


                % if user.activation.created_by == 'forgot_password':
                    <input type="submit" class="col-xs-12 btn btn-primary btn-load btn-lg" data-loading-text="Changing Password..." value="Change Password" id="submit_forgot_signup">
                % else:
                    % if user.activation.created_by == 'signup':
                        <input type="submit" class="col-xs-12 btn btn-primary btn-load btn-lg" data-loading-text="Creating Account..." value="Create Account" id="submit_forgot_signup">
                    % endif
                % endif



            </form>
                    <!-- /.panel -->
                </div>
                <!-- /.col-lg-8 -->
                <div class="col-lg-4">
                        <!-- /.panel-heading -->
                        <div class="panel-body">
                            <div class="list-group">

                            % if user.activation.created_by == 'signup':
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-comment fa-fw"></i> Valid Username
                                    <span id="vusername" class="pull-right glyphicon glyphicon-remove" style="color:#FF0004;"></span>
                                </a>
                            % endif

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
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-upload fa-fw"></i> Username is not Password
                                    <span id="pwnotmatchuname" class="pull-right glyphicon glyphicon-remove" style="color:#FF0004;"></span>
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
