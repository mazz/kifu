<%inherit file="/layout.mako" />
<%def name="title()">Account Information: ${user.username}</%def>
<%namespace file="func.mako" import="account_nav, password_reset"/>
<%
    date_fmt = "%m/%d/%Y"
%>
${account_nav()}

<div class="form yui3-g">
    <div class="yui3-u-1-4 account_info">
        <div class="heading">

        <div class="large-12 columns">
            <div class="panel">
                <div class="row">
                    <div class="large-12 columns">
                        <h3>Account Information</h3>
                    </div>
                </div>


                <div class="row">
                    <div class="large-12 columns">
                        <h5>${user.username}</h5>
                    </div>
                </div>

                <div class="row">
                    <div class="large-12 columns">
                        <h5>Member since:
                            % if user.signup:
                                ${user.signup.strftime(date_fmt)}
                            % else:
                                Unknown
                            % endif
                        <h5>
                    </div>
                </div>

                <div class="row">
                    <div class="large-12 columns">
                        <h5>Last Seen: <span>
                            % if user.last_login:
                                ${user.last_login.strftime(date_fmt)}
                            % else:
                                Not logged in
                            % endif
                        <h5>
                    </div>
                </div>

                <div class="row">
                    <div class="large-12 columns">
                        <br/>
                    </div>
                </div>

                <form>
                    <div class="row">
                        <div class="large-12 columns">
                            <h5>Name</h5>
                        </div>
                    </div>

                    <div class="row">
                        <div class="large-12 columns">
                            <input type="text" id="name" name="name" value="${user.name}" />
                        </div>
                    </div>

                    <div class="row">
                        <div class="large-12 columns">
                            <h5>Email</h5>
                        </div>
                    </div>

                    <div class="row">
                        <div class="large-12 columns">
                            <input type="email" id="email" name="email" value="${user.email}" />
                        </div>
                    </div>

                    <div class="row">
                        <div class="small-3 columns">
                            <input type="button" id="submit_account_change" value="Update" class="button" class="postfix small button expand"/>
                        </div>
                    </div>

                </form>
                <div class="row">
                    <div class="large-12 columns">
                        <div id="account_msg" class="error"></div>
                    </div>
                </div>
            </div>
        </div>

    </div>

</div>

% if user.has_invites():
<div id="invite_container">
</div>
% endif

<div class="form">
    <a href="" id="show_key" class="heading">
        <span aria-hidden="true" class="icon icon-key" title="Api Key"></span>
        <em class="icon">Api Key</em>
        View API Key</a>
    <div id="api_key_container" style="display: none; opacity: 0;">
        <form>
            <ul>
                <li>
                    <label>Api Key</label>
                    <span id="api_key"></span>
                </li>
            </ul>
            <div class="details">
            Your Api Key is used to validate your account when using outside
            services. This includes anything making Api calls on your behalf such
            as the mobile site, outside scripts, or client applications.
            </div>
        </form>
    </div>
</div>

${password_reset(user, reset=False)}

<%def name="add_js()">
    <script type="text/javascript">
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
    </script>
</%def>
