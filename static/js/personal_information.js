 $(function () {
        // $("#bottom").addClass('pb-3')
        $("#address_change").click(function () {
        window.location.href="/address/"
    });
        $("#register").click(function () {
            window.location.href="http://" + window.location.host + "/user/register/"
        });
        $("#login").click(function () {
            window.location.href="http://" + window.location.host + "/user/login/"
        });
        $("#logout").click(function () {
            window.location.href="http://" + window.location.host + "/user/logout/"
        });

        var is_login = $("#is_login").val()
        if (is_login=='True'){
            $("#login").css('display',"none");
            $("#register").css('display',"none");
            $("#logout").css('display',"inline");
        }else{
            $("#login").css('display',"inline");
            $("#register").css('display',"inline");
            $("#logout").css('display',"none");
        };

        $("#previous_page").click(function () {
            window.history.back(-1);
        })

        $("#code_QR").hide()
        $("#show_QR").click(function () {
            $("#code_QR").fadeToggle(300)
        })

    });