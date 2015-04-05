var unique_username_timer = null;
var username_exists = false;

$(document).ready(function() {

    $('#submit_forgot_signup').prop('disabled', true);
    $('#submit_account_change').prop('disabled', true);
    $('#change_password').prop('disabled', true);

    $("input[id=new_username]").keyup(function () {
        check_username_field();

//        console.log('unique_username_timer: ' + unique_username_timer);
//        console.log('user_username exists: ' + ($("#user_username").val() != undefined));
        if (unique_username_timer === null)
        {
            unique_username_timer = setTimeout(function() { unique_username($("#new_username").val()); }, 2000);
            $("span[id*=unique_username_api_value]").hide();
        }

    });


    $("input[type=password]").keyup(function () {
        var ucase = new RegExp("[A-Z]+");
        var lcase = new RegExp("[a-z]+");
        var num = new RegExp("[0-9]+");

        var long_password   = $("#password1").val().length >= 8;
        var uppercase       = ucase.test($("#password1").val());
        var lowercase       = lcase.test($("#password1").val());
        var numeric         = num.test($("#password1").val());
        var password_match  = $("#password1").val() == $("#password2").val();

        var pwnotmatchuname =  ($("#password1").val() == $("#password2").val()) && ($("#password1").val() != $("#new_username").val());
        console.log('pwnotmatchuname: ' + pwnotmatchuname);

        var all_good;
        if (long_password) {
            $("#8char").removeClass("glyphicon-remove");
            $("#8char").addClass("glyphicon-ok");
            $("#8char").css("color", "#00A41E");
        } else {
            $("#8char").removeClass("glyphicon-ok");
            $("#8char").addClass("glyphicon-remove");
            $("#8char").css("color", "#FF0004");
        }

        if (uppercase) {
            $("#ucase").removeClass("glyphicon-remove");
            $("#ucase").addClass("glyphicon-ok");
            $("#ucase").css("color", "#00A41E");
        } else {
            $("#ucase").removeClass("glyphicon-ok");
            $("#ucase").addClass("glyphicon-remove");
            $("#ucase").css("color", "#FF0004");
        }

        if (lowercase) {
            $("#lcase").removeClass("glyphicon-remove");
            $("#lcase").addClass("glyphicon-ok");
            $("#lcase").css("color", "#00A41E");
        } else {
            $("#lcase").removeClass("glyphicon-ok");
            $("#lcase").addClass("glyphicon-remove");
            $("#lcase").css("color", "#FF0004");
        }

        if (numeric) {
            $("#num").removeClass("glyphicon-remove");
            $("#num").addClass("glyphicon-ok");
            $("#num").css("color", "#00A41E");
        } else {
            $("#num").removeClass("glyphicon-ok");
            $("#num").addClass("glyphicon-remove");
            $("#num").css("color", "#FF0004");
        }

        if (password_match) {
            $("#pwmatch").removeClass("glyphicon-remove");
            $("#pwmatch").addClass("glyphicon-ok");
            $("#pwmatch").css("color", "#00A41E");
        } else {
            $("#pwmatch").removeClass("glyphicon-ok");
            $("#pwmatch").addClass("glyphicon-remove");
            $("#pwmatch").css("color", "#FF0004");
        }

        if (pwnotmatchuname) {
            $("#pwnotmatchuname").removeClass("glyphicon-remove");
            $("#pwnotmatchuname").addClass("glyphicon-ok");
            $("#pwnotmatchuname").css("color", "#00A41E");
        } else {
            $("#pwnotmatchuname").removeClass("glyphicon-ok");
            $("#pwnotmatchuname").addClass("glyphicon-remove");
            $("#pwnotmatchuname").css("color", "#FF0004");
        }


        //pwnotmatchuname
        all_good = long_password &lowercase & uppercase & numeric & password_match & pwnotmatchuname;

        console.log('all_good: ' + all_good);

        $('#submit_forgot_signup').prop('disabled', !all_good);
        $('#change_password').prop('disabled', !all_good);
    });

    $("input[id=name]").keyup(function () {
            var min_name_length = 1;
            var is_min_length   = $("#name").val().length >= min_name_length;

            $('#submit_account_change').prop('disabled', !is_min_length);

    });
});

function check_username_field()
{
        var vusername = new RegExp("^[^\-]?[a-zA-Z_0-9]+"); // do not allow a username to precede with one or more of `-`
        var valid_username  =  vusername.test($("#new_username").val());
//        var is_min_length   = $("#username1").val().length >= min_name_length;

        console.log('valid_username: ' + valid_username);
        if (valid_username && !username_exists)
        {
            $("#vusername").removeClass("glyphicon-remove");
            $("#vusername").addClass("glyphicon-ok");
            $("#vusername").css("color", "#00A41E");
        }
        else
        {
            $("#vusername").removeClass("glyphicon-ok");
            $("#vusername").addClass("glyphicon-remove");
            $("#vusername").css("color", "#FF0004");
        }
}


function unique_username(username)
{
    if (username.length > 0)
    {
        clearTimeout(unique_username_timer);
        unique_username_timer = null;

        var formData = JSON.stringify({
                    username: username,
                    });

        var resultString;
        $.ajax({
            type: "POST",   
                url: APP_URL + "/api/v1/" + username + "/usernameexists",
                data: formData,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data, textStatus, jqXHR)
            {
                var exists;
//                console.log("usernameexists success: " + data);

                for(key in data) {
                    if (key === "exists")
                    {
                        console.log("found success");
                        exists = data[key];
                    }

//                    console.log("key: " + key);
//                    console.log("value: " + data[key]);
    //                $('#view_api_key_button').hide();
                    var unique_username_result;
                    if (exists == true)
                    {
                        unique_username_result = 'This username is currently in use.'
                        username_exists = true;
                    }
                    else
                    {
                        unique_username_result = 'This username is available.'
                        username_exists = false;
                    }

                    $("span[id*=unique_username_api_value]").text(unique_username_result);
                    $("span[id*=unique_username_api_value]").show();

                    check_username_field();

    //##                    $('#view_api_key_button').remove("i");
    //                $("span[id*=view_api_key_value]").text(api_key);
    //                $("span[id*=view_api_key_value]").show();
                }
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                var message;
                console.log("usernameexists fail");
    //            $("span[id*=view_api_key_value]").text('There was an error obtaining your API key. Try later.');
            }
            });

    }
}
