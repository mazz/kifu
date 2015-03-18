<%inherit file="/layout.mako" />

<%def name="title()">Sign up for foo!</%def>

<div class="container">
    <div class="row">
        <div class="row">
            <div class="col-md-4 col-md-offset-4">
                <div class="panel panel-default">
                    % if message is not '':
                        <div class="alert alert-success" role="alert">
                        <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>
                        <span class="sr-only">Error:</span>
                        ${message}
                        <!--<button type="button" class="close" data-dismiss="alert">&times;</button> -->
                        </div>
                    % endif

                    <div class="panel-body">
                        <div class="text-center">
                          <h3><i class="fa fa-thumbs-o-up fa-4x"></i></h3>
                          <h2 class="text-center">Sign Up With foo!</h2>
                          <p>Enter your email and a confirmation link with an assigned password will be sent to you.</p>
                            <div class="panel-body">

                              <form "${request.route_url('signup')}" method="post" class="form">
                                <fieldset>
                                  <div class="form-group">
                                    <div class="input-group">
                                      <span class="input-group-addon"><i class="glyphicon glyphicon-envelope color-blue"></i></span>

                                      <input name="email" placeholder="email address" class="form-control" type="email" oninvalid="setCustomValidity('Please enter a valid email address!')" onchange="try{setCustomValidity('')}catch(e){}" required="">
                                    </div>
                                  </div>
                                  <div class="form-group">
                                    <input class="btn btn-lg btn-primary btn-block" value="Sign Up" type="submit" name="form.submitted">
                                  </div>
                                </fieldset>
                              </form>

                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

##<div class="container" xmlns="http://www.w3.org/1999/html">
##    <div class="row">
##        <div class="col-sm-6 col-md-4 col-md-offset-4">
##            <h1 class="text-center login-title">Sign up for foo</h1>
##            % if message is not '':
##                <div class="alert alert-danger" role="alert">
##                    <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>
##                    <span class="sr-only">Error:</span>
##                    ${message}
##                    <!--<button type="button" class="close" data-dismiss="alert">&times;</button> -->
##                </div>
##            % endif
##
####            <div class="alert alert-error">
####                <a href="#" class="close" data-dismiss="alert">&times;</a>
####                <strong>Error!</strong> A problem has been occurred while submitting your data.
####            </div>
##            <div class="account-wall">
##                <form formid="signup_form" method="post" action="${request.route_url('signup')}" class="form-signin">
##
####                <input type="hidden" name="came_from" value="${came_from}"/>
##                <input type="text" class="form-control" placeholder="Email" name="email" value="${email}" required autofocus>
##                    </br>
##
##                <button class="btn btn-lg btn-primary btn-block" type="submit" name="form.submitted">
##                    Sign up</button>
##                <a href="${request.route_url('forgot_password')}" class="pull-right need-help">Forgot Password? </a><span class="clearfix"></span>
##
##                </form>
##            </div>
##        </div>
##    </div>
##</div>


##<%def name="signup_form()">
##    <form formid="signup_form" method="post" action="${request.route_url('signup')}">
##
##        <div class="row collapse">
##            <div class="large-12 columns">
##
##                <h3>${self.title()}</h3>
##                ${form.email.label}
##                ${form['email']}
##
##              <input type="submit" id="send_signup" name="send_signup" value="Sign up" class="radius button"/>
##            </div>
##        </div>
##
##    </form>
##
##</%def>
##
##<!-- Signup Details -->
##    % if signup_success_message:
##        <div class="row collapse">
##            <div class="large-12 columns">
##                % for msg in request.session.pop_flash():
##                    <div data-alert class="alert-box success">
##                        ${msg}
##                    </div>
##                % endfor
##            </div>
##        </div>
##    % elif signup_error_message:
##        <div class="row collapse">
##            <div class="large-12 columns">
##                % for msg in request.session.pop_flash():
##                    <div data-alert class="alert-box alert">
##                        ${msg}
##                        <a href="#" class="close">&times;</a>
##                    </div>
##                % endfor
##            </div>
##        </div>
##
##        ${self.signup_form()}
##
##    % else:
##        <div class="row collapse">
##            <div class="large-12 columns">
##                % for field, errors in form.errors.iteritems():
##                    <div data-alert class="alert-box alert">
##                        ${field}: ${ ', '.join(errors)}
##                        <a href="#" class="close">&times;</a>
##                    </div>
##                % endfor
##            </div>
##        </div>
##
##        ${self.signup_form()}
##    % endif

    <!-- End Signup Details -->
