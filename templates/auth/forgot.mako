<%inherit file="/layout.mako" />
<%def name="title()">Forgot Password</%def>

<hr>
<div class="container">
    <div class="row">
        <div class="row">
            <div class="col-md-4 col-md-offset-4">
                <div class="panel panel-default">
                    <div class="panel-body">
                        <div class="text-center">
                          <h3><i class="fa fa-lock fa-4x"></i></h3>
                          <h2 class="text-center">Forgot Password?</h2>
                          <p>You can reset your password here.</p>
                            <div class="panel-body">

                              <form "${request.route_url('forgot_password')}" method="post" class="form">
                                <fieldset>
                                  <div class="form-group">
                                    <div class="input-group">
                                      <span class="input-group-addon"><i class="glyphicon glyphicon-envelope color-blue"></i></span>

                                      <input name="email" placeholder="email address" class="form-control" type="email" oninvalid="setCustomValidity('Please enter a valid email address!')" onchange="try{setCustomValidity('')}catch(e){}" required="">
                                    </div>
                                  </div>
                                  <div class="form-group">
                                    <input class="btn btn-lg btn-primary btn-block" value="Send My Password" type="submit" name="form.submitted">
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


<script type="text/javascript">

    $(function()
    {
        $('#submit_forgotten').click(function()
        {
            console.log("submit_forgotten");

            var formData = {email:$("#email").val()};
            var resultString;
            $.ajax({
                type: "POST",   
                url: APP_URL + "/api/v1/suspend",
                data: formData,
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
                    $('#loginpanel-status').removeClass('alert-box').removeClass('warning').removeClass('round').addClass('success').addClass('radius').addClass('alert-box');
                    $('#forgotten_password_panel').slideToggle();

                    $('#loginpanel-status').html(message);
                },
                error: function (jqXHR, textStatus, errorThrown)
                {
                    var message;
                    console.log("suspend fail");

                    $('#loginpanel-status').removeClass('alert-box').removeClass('success').removeClass('radius').addClass('warning').addClass('round').addClass('alert-box');
                    $('#forgotten_password_panel').slideToggle();

                    $('#loginpanel-status').html(errorThrown);
                }
            });
        });
    });

    </script>
