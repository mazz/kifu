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
                <div class="small-4 columns">
                    <input type="submit" name="form.submitted" class="small button expand" value="Log In"/>
                </div>
            </div>

        </form>
        </div>
      </div>
    </div>

    <div class="row">
        <div class="large-12 columns">
            <div class="panel callout radius" id="Content">
                <div class="row">
                    <div class="large-12 columns">
                        <a href="#" id="forgotten_password" class="toggle_forgotten">Forgotten Password</a>

                        <div id="forgotten_password_panel" style="display: none; opacity: 0;">
                            <%include file="forgot.mako"/>
                        </div>
                    </div>
                </div>
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
