    <div class="row">
        <div class="large-12 columns">

            <div class="row">
                <div class="large-12 columns">
                    <div class="row">
                        <div class="large-12 columns">
                            <br/>
                        </div>
                    </div>

                    <form>

                    <div class="row">
                        <div class="large-12 columns">
                            <h5>Email</h5>
                        </div>
                    </div>

                    <div class="row">
                        <div class="large-12 columns">
                             <input type="email" id="email" name="email" value="" />
                        </div>
                    </div>

                    <div class="row">
                        <div class="small-4 columns">
                             <input type="button" id="submit_forgotten" value="Reset" class="small button expand" />
                        </div>
                    </div>
                    </form>
                </div>
        </div>
    </div>

    <div class="row">
        <div class="large-12 columns">
            <h5>If you've forgotten your password. We can reset it.</h5>
            <h5>Please submit your email address you used to sign into the account in the form and a reset link will be emailed to you.</h
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
