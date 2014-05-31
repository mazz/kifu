<%inherit file="/layout.mako" />

<%def name="title()">Sign up for wtf!</%def>

<%def name="signup_form()">
    <form formid="signup_form" method="post" action="${request.route_url('signup_process')}">

        <div class="row collapse">
            <div class="large-12 columns">

                <h3>${self.title()}</h3>
                ${form.email.label}
                ${form['email']}

              <input type="submit" id="send_signup" name="send_signup" value="Sign up" class="radius button"/>
            </div>
        </div>

    </form>

</%def>

<!-- Signup Details -->
    % if signup_success_message:
        <div class="row collapse">
            <div class="large-12 columns">
                % for msg in request.session.pop_flash():
                    <div data-alert class="alert-box success">
                        ${msg}
                    </div>
                % endfor
            </div>
        </div>
    % elif signup_error_message:
        <div class="row collapse">
            <div class="large-12 columns">
                % for msg in request.session.pop_flash():
                    <div data-alert class="alert-box alert">
                        ${msg}
                        <a href="#" class="close">&times;</a>
                    </div>
                % endfor
            </div>
        </div>

        ${self.signup_form()}

    % else:
        <div class="row collapse">
            <div class="large-12 columns">
                % for field, errors in form.errors.iteritems():
                    <div data-alert class="alert-box alert">
                        ${field}: ${ ', '.join(errors)}
                        <a href="#" class="close">&times;</a>
                    </div>
                % endfor
            </div>
        </div>

        ${self.signup_form()}
    % endif

    <!-- End Signup Details -->
