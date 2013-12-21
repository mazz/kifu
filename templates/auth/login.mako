<%inherit file="/layout.mako" />
<%def name="title()">Login</%def>

<div class="login_form" class="block">
    <form action="${request.route_url('login')}" method="post" class="login form">

    <div class="row">
      <div class="large-12 columns">
        <div class="panel">
            <div class="row">
                <div class="large-12 columns">
                    <h1>Log In</h1>
                </div>
            </div>

            <div class="row">
                <div class="large-12 columns">
                    <p class="error">${message}</p>
                    <input type="hidden" name="came_from" value="${came_from}"/>
                </div>
            </div>

            <div class="row">
                <div class="large-12 columns">
                    <h5>Username</h5>
                </div>
            </div>

            <div class="row">
                <div class="large-12 columns">
                    <input type="text" name="login" value="${login}"/>
                </div>
            </div>

            <div class="row">
                <div class="large-12 columns">
                    <h5>Password</h5>
                </div>
            </div>

            <div class="row">
                <div class="large-12 columns">
                    <input type="password" name="password" value="${password}"/>
                </div>
            </div>

            <div class="row">
                <div class="small-3 columns">
                    <input type="submit" name="form.submitted" class="postfix small button expand" value="Log In"/>
                </div>
            </div>

        </form>
        </div>
      </div>
    </div>

    <div class="row">
        <div class="large-12 columns">
            <div class="row">
                <div class="large-12 columns">
                <a href="#" data-dropdown="drop2">Forgot Password</a>
                <div id="drop2" data-dropdown-content class="f-dropdown content">
                <form action="${request.route_url('login')}" method="post" class="forgot password form" id="drop" class="[tiny small medium large content]f-dropdown" data-dropdown-content>
                <h5>Enter the email you signed-up with to reset your password:</h5>
                <input type="text" name="forgot_password_email" value="forgot_password_email"/>
                <input type="submit" name="form.submitted" class="postfix small button expand" value="Reset Password"/>
                </form>
                </div>
                </div>
            </div>
        </div>
    </div>


