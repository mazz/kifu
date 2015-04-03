var unique_username_timer = null;

$(document).ready(function() {

    $('#submit_forgot_signup').prop('disabled', true);
    $('#submit_account_change').prop('disabled', true);
    $('#change_password').prop('disabled', true);

    $("input[id=new_username]").keyup(function () {
        var vusername = new RegExp("^[^\-]?[a-zA-Z_0-9]+"); // do not allow a username to precede with one or more of `-`
        var valid_username  =  vusername.test($("#new_username").val());
//        var is_min_length   = $("#username1").val().length >= min_name_length;

        console.log('valid_username: ' + valid_username);
        if (valid_username)
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
        console.log('unique_username_timer: ' + unique_username_timer);
        console.log('user_username exists: ' + ($("#user_username").val() != undefined));
        if (unique_username_timer === null)
        {
            unique_username_timer = setTimeout(function() { unique_username(); }, 1000);
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

        var pwnotmatchuname =  ($("#password1").val() == $("#password2").val()) && ($("#password1").val() != $("#username1").val());

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
        all_good = long_password &lowercase & uppercase & numeric & password_match;

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

function unique_username()
{
    console.log('unique_username')
    unique_username_timer = null;
}
