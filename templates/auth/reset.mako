<%inherit file="/layout.mako" />
##<%namespace file="../accounts/func.mako" import="password_reset"/>
##<%def name="title()">Activate your account</%def>
##
##${password_reset(user, reset=True)}

<script type="text/javascript" src="/static/js/jquery.alphanum.js"></script>
<script src="/static/js/reset-enable.js"></script>

        <div id="page-wrapper">
            <div class="row">
                <div class="col-md-8 col-md-offset-2">
                    % if user.activation.created_by == 'forgot_password':
                        <h1 class="page-header">Change Password</h1>
                    % else:
                        % if user.activation.created_by == 'signup':
                            <h1 class="page-header">Enable Account</h1>
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

##            <p class="text-center">created_by: ${user.activation.created_by}</p>
##            <p class="text-center">user.username: ${user.username}</p>

            <form method="POST" id="passwordForm" class="form-horizontal" role="form">

            % if user.activation.created_by == 'signup':
                <input type="text" class="input-lg form-control" name="new_username" id="new_username" placeholder="Username" autocomplete="off" maxlength="32">
                <span class="pull-right text-muted small" id="unique_username_api_value" hidden>
                </span>

            % endif

                </br>

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
                        <input type="submit" class="col-xs-12 btn btn-primary btn-load btn-lg" data-loading-text="Enabling Account..." value="Enable Account" id="submit_forgot_signup">
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
                                    <span id="vusername" class="pull-right fa fa-times" style="color:#973132;"></span>
                                </a>
                            % endif

                                <a href="#" class="list-group-item">
                                    <i class="fa fa-comment fa-fw"></i> 8 Characters Long
                                    <span id="8char" class="pull-right fa fa-times" style="color:#973132;"></span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-twitter fa-fw"></i> One Uppercase Letter
                                    <span id="ucase" class="pull-right fa fa-times" style="color:#973132;"></span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-envelope fa-fw"></i> One Lowercase Letter
                                    <span id="lcase" class="pull-right fa fa-times" style="color:#973132;"></span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-tasks fa-fw"></i> One Number
                                    <span id="num" class="pull-right fa fa-times" style="color:#973132;"></span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-upload fa-fw"></i> Passwords Match
                                    <span id="pwmatch" class="pull-right fa fa-times" style="color:#973132;"></span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-upload fa-fw"></i> Username is not Password
                                    <span id="pwnotmatchuname" class="pull-right fa fa-times" style="color:#973132;"></span>
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
