<%inherit file="/layout.mako" />
<%def name="title()">Login</%def>

<div class="container">
    <div class="row">
        <div class="col-sm-6 col-md-4 col-md-offset-4">
            <h1 class="text-center login-title">Sign in to continue to foo</h1>
            % if message is not '':
                <div class="alert alert-danger" role="alert">
                    <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>
                    <span class="sr-only">Error:</span>
                    ${message}
                    <!--<button type="button" class="close" data-dismiss="alert">&times;</button> -->
                </div>
            % endif

##            <div class="alert alert-error">
##                <a href="#" class="close" data-dismiss="alert">&times;</a>
##                <strong>Error!</strong> A problem has been occurred while submitting your data.
##            </div>


            <div class="panel panel-default">
                        <div class="text-center">
                          <h3><i class="fa fa-sign-in fa-4x"></i></h3>
                        </div>
                <form "${request.route_url('login')}" method="post" class="form-signin">

                <input type="hidden" name="came_from" value="${came_from}"/>
                <input type="text" class="form-control" placeholder="Email" name="email" value="${email}" required autofocus>
                <input type="password" class="form-control" placeholder="Password" name="password" value="${password}" required>

                <button class="btn btn-lg btn-primary btn-block" type="submit" name="form.submitted">
                    Sign in</button>
                <label class="checkbox pull-left">
                    <input type="checkbox" value="remember-me">
                    Remember me
                </label>
                <a href="${request.route_url('forgot_password')}" class="pull-right need-help">Forgot Password? </a><span class="clearfix"></span>
                </form>
            </div>
            <a href="#" class="text-center new-account">Create an account</a>
        </div>
    </div>
</div>


    <%def name="add_js()">
    <script type="text/javascript">

    $(function() {
        $('#forgotten_password').click(function() {
            $('#forgotten_password_panel').slideToggle();
            $("#forgotten_password_panel").css({ opacity: 1. });
        });
    });

    $(document).ready(function(){
        $(".close").click(function(){
            $(".alert").alert();
        });
    });
    </script>
    </%def>
