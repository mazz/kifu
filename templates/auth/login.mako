<%inherit file="/layout.mako" />
<%def name="title()">Login</%def>

<div class="container">
    <div class="row">
        <div class="col-sm-6 col-md-4 col-md-offset-4">
            <h1 class="text-center login-title">Sign in to continue to ~~~PROJNAME~~~</h1>
            <div class="account-wall">
                <img class="profile-img" src="https://lh5.googleusercontent.com/-b0-k99FZlyE/AAAAAAAAAAI/AAAAAAAAAAA/eu7opA4byxI/photo.jpg?sz=120"
                    alt="">
                <form "${request.route_url('login')}" method="post" class="form-signin">

                <input type="hidden" name="came_from" value="${came_from}"/>
                <input type="text" class="form-control" placeholder="Email" name="login" value="${login}" required autofocus>
                <input type="password" class="form-control" placeholder="Password" name="password" value="${password}" required>

                <button class="btn btn-lg btn-primary btn-block" type="submit">
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

    </script>
    </%def>
