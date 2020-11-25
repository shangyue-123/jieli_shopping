$(function () {
        //点击获取验证码按钮，检查邮箱格式，是否为空，正确则发送邮箱
        $("#get_verification").click(function () {
            var user_email = $("#user_email").val()
            var user_email_check = $("#user_email")
            var user_email_check_re = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;

             if (user_email == '') {
                user_email_check.addClass("is-invalid")
                alert('邮箱不能为空')
            } else if (user_email_check_re.test(user_email) == false) {
                user_email_check.addClass("is-invalid")
                alert('邮箱格式不正确')
            }else {
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
        });
        //点击提交按钮，验证信息是否填写
        $("#submit").click(function (e) {
            var user_email = $("#user_email").val()
            var verification = $("#verification").val()
            var retrieve_name = $("#retrieve_name").prop('checked')
            var retrieve_password = $("#retrieve_password").prop('checked')
            if (user_email == '') {
                e.preventDefault();
                alert('请输入邮箱')
            } else if (verification == '') {
                e.preventDefault();
                alert('请输入验证码')
            } else if (retrieve_name == false && retrieve_password == false) {
                e.preventDefault();
                alert('请选择找回内容')
            }
        })
        //点击上一页图标，返回上一页
        $("#previous_page").click(function () {
            window.history.back(-1);

        })
    })