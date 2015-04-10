var unique_username_timer = null;
var g_username_exists = false;
var ucase = new RegExp("[A-Z]+");
var lcase = new RegExp("[a-z]+");
var num = new RegExp("[0-9]+");
//var vusername = new RegExp("^[^\-]?"); // do not allow a username to precede with one or more of `-`
//var vusername = new RegExp("^[^\-]?\\w+"); // do not allow a username to precede with one or more of `-`
//var whitespace = new RegExp("\\s+"); // whitespace
var g_valid_username = false;
var g_calling_timer = false;

$(document).ready(function() {

    $('#submit_forgot_signup').prop('disabled', true); // reset/enable page

    $('#new_username').alphanum({
        allowSpace: false, // Allow the space character
        allow: '_',
        allowOtherCharSets: true
    });

    $("input[id=new_username]").keyup(function () {
        $('#submit_forgot_signup').prop('disabled', true); // reset/enable page
        if (g_calling_timer == false)
        {
            console.log('calling unique_username_rest');
            g_calling_timer = true;
            unique_username_timer = setTimeout(function() { unique_username_rest($("#new_username").val()); }, 2000);
            $("span[id*=unique_username_api_value]").hide();
        }

    });

    $("input[type=password]").keyup(function () {
        update_ui();
    });
});

function unique_username_rest(username)
{
    clearTimeout(unique_username_timer);
    g_calling_timer = false;

    console.log("unique_username_rest: " + username);
    if (username.length > 0)
    {

        var formData = JSON.stringify({
                    username: username,
                    });
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
                    exists = data[key]['exists'];
                    console.log("value: " + data[key]['exists']);

    //                $('#view_api_key_button').hide();
                    var unique_username_result;
                    if (exists == true)
                    {
                        unique_username_result = 'This username is currently in use.'
                        g_username_exists = true;
                        g_valid_username = false;
                    }
                    else
                    {
                        unique_username_result = 'This username is available.'
                        g_username_exists = false;
                        g_valid_username = true;
                    }

                    $("span[id*=unique_username_api_value]").text(unique_username_result);
                    $("span[id*=unique_username_api_value]").show();

                    update_ui();

                }
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                var message;
                console.log("usernameexists fail");
            }
            });

    }
}

function update_ui()
{
    var long_password   = $("#password1").val().length >= 8;
    var uppercase       = ucase.test($("#password1").val());
    var lowercase       = lcase.test($("#password1").val());
    var numeric         = num.test($("#password1").val());
    var password_match  = ($("#password1").val() == $("#password2").val()) & long_password;

    var pwnotmatchuname =  ($("#password1").val() == $("#password2").val()) & ($("#password1").val() != $("#new_username").val());

    if (long_password)
    {
        $("#8char").removeClass("fa-times");
        $("#8char").addClass("fa-check");
        $("#8char").css("color", "#00A41E");
    }
    else
    {
        $("#8char").removeClass("fa-check");
        $("#8char").addClass("fa-times");
        $("#8char").css("color", "#973132");
    }

    if (uppercase)
    {
        $("#ucase").removeClass("fa-times");
        $("#ucase").addClass("fa-check");
        $("#ucase").css("color", "#00A41E");
    }
    else
    {
        $("#ucase").removeClass("fa-check");
        $("#ucase").addClass("fa-times");
        $("#ucase").css("color", "#973132");
    }

    if (lowercase)
    {
        $("#lcase").removeClass("fa-times");
        $("#lcase").addClass("fa-check");
        $("#lcase").css("color", "#00A41E");
    }
    else
    {
        $("#lcase").removeClass("fa-check");
        $("#lcase").addClass("fa-times");
        $("#lcase").css("color", "#973132");
    }

    if (numeric)
    {
        $("#num").removeClass("fa-times");
        $("#num").addClass("fa-check");
        $("#num").css("color", "#00A41E");
    }
    else
    {
        $("#num").removeClass("fa-check");
        $("#num").addClass("fa-times");
        $("#num").css("color", "#973132");
    }

    if (password_match)
    {
        $("#pwmatch").removeClass("fa-times");
        $("#pwmatch").addClass("fa-check");
        $("#pwmatch").css("color", "#00A41E");
    }
    else
    {
        $("#pwmatch").removeClass("fa-check");
        $("#pwmatch").addClass("fa-times");
        $("#pwmatch").css("color", "#973132");
    }

    if (pwnotmatchuname)
    {
        $("#pwnotmatchuname").removeClass("fa-times");
        $("#pwnotmatchuname").addClass("fa-check");
        $("#pwnotmatchuname").css("color", "#00A41E");
    }
    else
    {
        $("#pwnotmatchuname").removeClass("fa-check");
        $("#pwnotmatchuname").addClass("fa-times");
        $("#pwnotmatchuname").css("color", "#973132");
    }
    var passwords_valid = long_password && lowercase && uppercase && numeric && password_match && pwnotmatchuname;

    var username_ok = g_valid_username && !g_username_exists;
    var password_ok = long_password;

    if (username_ok)
    {
        $("#vusername").removeClass("fa-times");
        $("#vusername").addClass("fa-check");
        $("#vusername").css("color", "#00A41E");
    }
    else
    {
        $("#vusername").removeClass("fa-check");
        $("#vusername").addClass("fa-times");
        $("#vusername").css("color", "#973132");
    }

    $('#submit_forgot_signup').prop('disabled', (!passwords_valid || !username_ok)); // reset/enable page

}