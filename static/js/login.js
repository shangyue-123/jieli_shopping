$(function () {

        //确定是否符合提交条件，不符合，阻止提交
        $("#submit").click(function (e) {
            var check_name = user_name_check()
            var check_password = user_password_check()

            if (!(check_name && check_password)){
                e.preventDefault();
                alert('请输入正确的账号密码')
            }

            //用户名输入框合法性检测
            function user_name_check () {
                var user_name = $("#user_name").val()
                var user_name_check_span = $("#user_name_check_span")
                var check_name = false
                if (user_name == ''){
                    $("#user_name").addClass('is-invalid');
                    user_name_check_span.text('用户名不能为空')
                    check_name = false
                }else if (user_name.length > 16){
                    $("#user_name").addClass('is-invalid');
                    user_name_check_span.text('用户名在8~16位之间')
                    check_name = false
                }else if (user_name.length < 8){
                    $("#user_name").addClass('is-invalid');
                    user_name_check_span.text('用户名在8~16位之间')
                    check_name = false
                }else {
                    $("#user_name").removeClass('is-invalid').addClass('is-valid');
                    user_name_check_span.empty()
                    check_name = true
                }
                return check_name
            }
            //密码合法性检测
            function user_password_check() {
                var user_password = $("#user_password").val();
                var user_password_check_span = $("#user_password_check_span")
                var check_password = false
                if (user_password.length == 0){
                    $("#user_password").addClass('is-invalid');
                    user_password_check_span.text('密码不能为空');
                    check_password = false
                }else if (user_password.length < 8 && user_password.length > 0){
                    $("#user_password").addClass('is-invalid');
                    user_password_check_span.text('密码在8~16位之间')
                    check_password = false
                }else if (user_password.length>16){
                    $("#user_password").addClass('is-invalid');
                    user_password_check_span.text('密码在8~16位之间')
                    check_password = false
                }else {
                    $("#user_password").removeClass("is-invalid").addClass("is-valid");
                    user_password_check_span.empty()
                    check_password = true
                }
                return check_password
            }
        })



        //点击注册跳转
        $("#register").click(function () {
             window.location.href="http://" + window.location.host + "/user/register/"
        })
        //点击找回账号密码跳转
        $("#retrieve").click(function () {
            window.location.href="http://"+window.location.host+"/user/retrieve/"
        })
        //点击上一页图标，返回上一页
        $("#previous_page").click(function () {
            window.history.back(-1);
        })

    })