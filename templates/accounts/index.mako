<%inherit file="/layout.mako" />
<%def name="title()">Account Information: ${user.username}</%def>
<%namespace file="func.mako" import="account_nav, password_reset"/>
<%
    date_fmt = "%m/%d/%Y"
%>
${account_nav()}

<div class="panel">
    <div class="row">
        <div class="large-4 columns">
            <h3>Account Information</h3>
                <h5>${user.username}</h5>
                <h5>Member since:
                    % if user.signup:
                        ${user.signup.strftime(date_fmt)}
                    % else:
                        Unknown
                    % endif
                <h5>
                <h5>Last Seen: <span>
                    % if user.last_login:
                        ${user.last_login.strftime(date_fmt)}
                    % else:
                        Not logged in
                    % endif
                <h5>
            </div>

            <div class="large-8 columns">
                <form>
                    <h5>Name</h5>
                    <input type="text" id="name" name="name" value="${user.name}" />
                    <h5>Email</h5>
                    <input type="email" id="email" name="email" value="${user.email}" />
                    <div class="row">
                    <div class="small-3 columns">
                        <input type="button" id="submit_account_change" value="Update" class="button" class="postfix small button expand"/>
                    </div>
                    </div>
                        <div class="row">
                            <div class="large-12 columns">
                            <div id="account_msg" class="error"></div>
                        </div>
                    </div>
                </form>
            </div>
    </div>
</div>

% if user.has_invites():
<div id="invite_container">
</div>
% endif

<div class="panel">
    <div class="row">
        <div class="large-4 columns">
            <a href="#" id="view_api_key" class="heading">
            <span aria-hidden="true" class="icon icon-lock" title="View API Key"></span>
            <h3>View API Key</h3></a>
        </div>

        <div class="large-8 columns">
            <div id="view_api_key_view" style="display: none; opacity: 0;">
            </div>
            <div class="row">
                <div class="large-12 columns">
                    <div data-alert class="" id="view_api_status">
                    </div>
                </div>
            </div>

            <div id="password_msg" class="error" style="opacity: 0;"></div>
        </div>
    </div>
</div>

${password_reset(user, reset=False)}

<%def name="add_js()">
    <script type="text/javascript">
        /*
        YUI().use('node', 'bookie-view', 'console', function (Y) {
            Y.on('domready', function () {
                var api_cfg = {
                    url: APP_URL + '/api/v1',
                    username: '${request.user.username}',
                    api_key: '${request.user.api_key}',
                },
                account_view = new Y.bookie.AccountView({
                    api_cfg: api_cfg
                });

                % if user.has_invites():
                    var invite_view = new Y.bookie.InviteView({
                        api_cfg: api_cfg,
                        user: {
                            invite_ct: ${user.invite_ct}
                        }
                    });
                    invite_view.render();
                % endif
            });
        });
        */
    </script>
</%def>


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
                $('#changepassword-status').removeClass('alert-box').removeClass('warning').removeClass('round').addClass('success').addClass('radius').addClass('alert-box');
                $('#forgotten_password_panel').slideToggle();

                $('#changepassword-status').html(message);
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                var message;
                console.log("account change fail");
                $('#changepassword-status').removeClass('alert-box').removeClass('success').removeClass('radius').addClass('warning').addClass('round').addClass('alert-box');
                $('#forgotten_password_panel').slideToggle();

                $('#changepassword-status').html(textStatus);
            }
        });

    });

});
</script>
