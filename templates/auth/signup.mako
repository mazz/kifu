<%inherit file="/layout.mako" />
<%def name="title()">Sign up for baz!</%def>
<div class="signup_form" class="block">

      <div class="large-12 columns">
        <div class="panel">
            <div class="row">
                <div class="large-12 columns">
                    <h1>Signup</h1>
                </div>
            </div>

        % if message:
            <div class="row">
                <div class="large-12 columns">
                    <p id="signup_msg" class="success">${message}</p>
                </div>
            </div>

        % else:

            <div class="row">
                <div class="large-12 columns">
                    <h5>If you'd like to have an account please submit your email address.</h5>
                </div>
            </div>
            <div class="row">
                <div class="large-12 columns">
                <br/>
                </div>
            </div>

            <form id="#signup_form" action="signup_process" method="POST">
            <div class="row">
                <div class="large-12 columns">
                    <h5>Email Address</h5>
                </div>
            </div>

            <div class="row">
                <div class="large-12 columns">
                    <input type="email" id="email" name="email" />
                </div>
            </div>


            <div class="row">
                <div class="small-3 columns">
                    <input type="submit" id="send_signup" name="send_signup" class="postfix small button expand" value="Sign Up" />
                </div>
            </div>
            </form>
        %endif

        % if errors:
            <div class="row">
                <div class="large-12 columns">
                    <div id="signup_msg" class="error">${errors['email']}</div>
                </div>
            </div>
        % endif

        </div>
      </div>
</div>