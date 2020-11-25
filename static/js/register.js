
$(function () {
    var user_name_check_submit = false
    var use_password_check_submit = false
    var user_password_again_check_submit = false
    var user_email_check_submit = false
    var user_email_verification_check_submit = false
    var user_number_check_submit = false


    // 用户名框失去焦点检测用户名是否重复或者符合要求
    $("#user_name").blur(function () {

        // 定义获取的标签值
        var user_name = $("#user_name").val()
        var check_span = $("#user_name_check_span")
        var check_input = $("#user_name")

        if (user_name == '')
        {
            check_input.addClass("is-invalid");
            check_span.html('用户名不能为空');
            user_name_check_submit = false
        }else if (user_name.length > 16)
        {
            check_input.addClass("is-invalid");
            check_span.html('用户名在8~16位之间');
            user_name_check_submit = false
        }else if (user_name.length < 8)
        {
            check_input.addClass("is-invalid");
            check_span.html('用户名在8~16之间');
            user_name_check_submit = false
        }else
            {
            $.ajax({
                url:"/register_check/",
                data:{"user_name":user_name,"csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val()
                },
                type:"POST",
                async:true,
                // dataType:"JSON",
                error:function(){
                    alert('发送失败')
                    console.log('发送失败')
                    user_name_check_submit = false
                },
                success:function (msg) {
                    msg = JSON.parse(msg)
                    if (msg.name_msg == true){
                        //账号已存在
                        check_span.html('用户名已被注册')
                        check_input.addClass("is-invalid");
                        user_name_check_submit = false
                    }else{
                        check_input.removeClass("is-invalid").addClass("is-valid");
                        check_span.empty()
                        user_name_check_submit = true
                    }
                }
                });
        }

    });

    // 密码框失去焦点实现
    $("#user_password").blur(function () {

        // 获取密码值
        var user_password = $("#user_password").val()
        var check_span = $("#user_password_check_span")
        var check_input = $("#user_password")

        if (user_password.length == 0  ){
            check_span.html('密码不能为空')
            check_input.addClass("is-invalid")
            use_password_check_submit = false
        }else if(user_password.length < 8 && user_password.length > 0){
            check_span.html('密码在8~16位之间')
            check_input.addClass("is-invalid")
            use_password_check_submit = false
        }else if (user_password.length>16){
            check_span.html('密码在8~16位之间')
            check_input.addClass("is-invalid")
            use_password_check_submit = false
        }else {
            check_input.removeClass("is-invalid").addClass("is-valid");
            check_span.empty()
            use_password_check_submit = true
        }

    })

    //密码核对框失去焦点测试密码是否一致
    $("#user_password_check").blur(function () {
        var user_password = $("#user_password").val()
        var user_password_check = $("#user_password_check").val()
        var user_pasword_check_input = $("#user_password_check")
        var user_password_check2_span = $("#user_password_check2_span")
        if (user_password_check.length == 0){
            user_pasword_check_input.removeClass("is-valid").addClass("is-invalid")
            user_password_check2_span.html('请再次输入密码')
            user_password_again_check_submit = false
        }else if (user_password != user_password_check){
            user_pasword_check_input.removeClass("is-valid").addClass("is-invalid")
            user_password_check2_span.html('密码不一致')
            user_password_again_check_submit = false
        }else {
            user_pasword_check_input.removeClass("is-invalid").addClass("is-valid")
            user_password_check2_span.empty()
            user_password_again_check_submit = true
        }

    })

    //邮箱框失去焦点测试邮箱是否符合规范
    $("#user_email").blur(function () {
        var user_email = $("#user_email").val()
        var user_email_check = $("#user_email")
        var user_email_check_span = $("#user_email_check_span")
        var user_email_check_re = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;

        // 邮箱判断
        if (user_email == ''){
            user_email_check.addClass("is-invalid")
            user_email_check_span.html('邮箱不能为空')
            user_email_check_submit= false
        }else if (user_email_check_re.test(user_email) == false){
            user_email_check.addClass("is-invalid")
            user_email_check_span.html('邮箱格式不正确')
            user_email_check_submit = false
        }else {
            $.ajax({
            url:"/register_check/",
            data:{"user_email":user_email,"csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val()
            },
            type:"POST",
            async:true,
            // dataType:"JSON",
            error:function(){
                alert('发送失败')
                console.log('发送失败')
                user_email_check_submit = false
            },
            success:function (msg) {
                msg = JSON.parse(msg)
                if ( msg.email_msg == true){
                    //账号已存在
                    user_email_check_span.html('邮箱已被注册')
                    user_email_check.addClass("is-invalid");
                    user_email_check_submit = false
                }else{
                    user_email_check.removeClass("is-invalid").addClass("is-valid");
                    user_email_check_span.empty()
                    user_email_check_submit = true
                    }
                }
                });
        }

    })

    //点击获取邮箱验证码
    $("#get_verification").click(function () {
        var user_email = $("#user_email").val()
        if (user_email == ''){
            $("#user_email").addClass('is-invalid')
            $("#user_email_verification_span").text('邮箱不能为空')
        }else {
            $("#user_email_verification_span").empty()
            get_verifiction(user_email)
        }
        //点击获取验证码按钮向后台获取验证码，并进入倒计时
        function get_verifiction(user_email) {
            var minutes = 300
            $.ajax({
                url: "/user/email_verification/",
                data: {
                    'user_email': user_email
                },
                type: "GET",
                success: function () {
                    $("#get_verification").removeClass('btn-primary').addClass('btn-secondary').attr('disabled', true)
                    setInterval(function () {
                        count_down()
                    }, 1000)

                    function count_down() {
                        if (minutes === 1) {
                            $("#get_verification").attr('disabled', false).removeClass('btn-secondary').addClass('btn-primary')
                                .text('获取验证码')

                        } else {
                            minutes--;
                            $('#get_verification').text('剩余' + minutes + '秒');
                        }
                    }
                }
            })
        }

    })

    //邮箱验证码输入框失去焦点，异步检测验证码是否正确
    $("#user_email_verification").blur(function () {
        var email_verification = $(this).val()
        if (email_verification == ''){
            $('#user_email_verification_span').text('验证码不能为空')
            user_email_verification_check_submit = false
        }else {
            $.ajax({
                url:'/user/email_verification/',
                data:{'email_verification':email_verification,
                    "csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val()},
                type:'POST',
                success:function (msg) {
                    console.log(typeof msg)
                    if (msg == 'true'){
                        $("#user_email_verification").removeClass('is-invalid').addClass('is-valid');
                        $('#user_email_verification_span').empty();
                        user_email_verification_check_submit = true
                    }else if (msg == 'false'){
                        $("#user_email_verification").addClass('is-invalid');
                        $('#user_email_verification_span').text('验证码错误');
                        user_email_verification_check_submit = false
                    }
                }
        })
        }



    })

    //手机号输入框失去焦点时删除所有除数字意外的符号后验证
    $("#user_number").blur(function () {
        var user_number = $("#user_number").val().replace(/[^0-9]/ig,"");
        var user_number_check = $("#user_number")
        var user_number_check_span = $("#user_number_check_span")
        if(user_number.length == 0){
            user_number_check_span.html('请输入手机号码')
            user_number_check.addClass("is-invalid")
            user_number_check_submit= false
        }else if (user_number.length == 11){
            user_number_check_span.empty()
            user_number_check.removeClass("is-invalid").addClass("is-valid")
            user_number_check_submit = true
        }else {
            user_number_check_span.html('请输入正确的手机号')
            user_number_check.removeClass("is-valid").addClass("is-invalid")
            user_number_check_submit = false
        }


    })

    //提交前检测是否符合提交条件
    $("#submit").click(function (e) {
        var submit_check = user_name_check_submit && use_password_check_submit
            && user_password_again_check_submit && user_email_check_submit
            && user_email_verification_check_submit && user_number_check_submit
        if (!submit_check){
            e.preventDefault();
            alert('请输入正确信息');
        }
    })
    //点击上一页图标，返回上一页
    $("#previous_page").click(function () {
            window.history.back(-1);

        })





})

