<%def name="password_reset(user, reset)">
    <%
        if user.activation and user.activation.created_by == 'invite':
            title = "Please activate your new account"
            submit = "Activate"
        elif reset:
            title = "Reactivate account by resetting your password"
            submit = "Reset"
        else:
            title = "Change password"
            submit = "Change"
    %>


<div class="panel">
    <div class="row">
        <div class="large-4 columns">
        <a href="#" id="show_password" class="heading">
            <span aria-hidden="true" class="icon icon-lock" title="Change
            password"></span>
            ${title}
        </a>
        </div>

        <div class="large-8 columns">
        <div id="password_change"
            % if not reset:
                style="display: none; opacity: 0;"
            % endif
        >
                <form id="password_reset" method="POST">
                    % if message:
                        <div class="error">${message}</div>
                    % endif
                     % if reset:
                         <input type="hidden" name="username" id="username" value="${user.username}" />
                         <input type="hidden" name="code" id="code" value="${user.activation.code}" />
                     % endif

                    <div></div
                    <ul>
                        % if not reset:
                                    <h5>Current Password</h5>
                                    <input type="password" id="current_password" name="current_password" />
                        % endif

                        % if user.activation and user.activation.created_by == 'invite':
                                    <h5>Choose Username</h5>
                                    <input type="text" id="new_username" name="new_username" />
                        % endif

                                <h5>New Password</h5>
                                <input type="password" id="new_password" name="new_password" />
                                <h5></h5>
                                <input type="submit" id="submit_password_change" value="${submit}" class="button" />
                    </ul>
                </form>
            </div>
            <div id="password_msg" class="error" style="opacity: 0;"></div>
        </div>
    </div>
</div>

</%def>

