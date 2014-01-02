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
            <h3>View API Key</h3>
        </div>

        <div class="large-8 columns">
            <form>
            </form>
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
});
</script>
