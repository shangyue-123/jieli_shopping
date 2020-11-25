$(function () {
    //搜索功能

    //点击搜索图片，跳转商品页并显示搜索商品
    $("#search_img").click(function () {
    window.location.href="/goods/goods_search/?search_input="+$("#search_input").val()
    })
    // 键盘输入异步搜索，调用搜索函数
    $("#search_input").keyup(function () {
            $("#search_list").empty();
            $.ajax({
                url: "/goods/goods_search/",
                data: {
                    'search_input':$("#search_input").val(),
                    "csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val(),
                },
                type: "POST",
                async: true,
                success:function (goods_name_list) {
                    // console.log(goods_name_list)

                    $.each(goods_name_list,function (key,goods_name) {
                        if ($("#search_input").val() == ''){
                            $("#search_list").empty();
                        }else {
                            addlist(goods_name);
                            goods_select();
                        }

                    });
                    }
            })
        })

    // 优惠功能
    //显示优惠价格
    goods_special_get()
    //遍历优惠商品，为优惠商品添加加入和减少购物车事件
    $('.flash_sales').each(function () {
            var goods_id = this.id
            add_cart(goods_id)
            subtract_cart(goods_id)
        })
    // 页面刷新时显示倒计时
    times_show()
    //每1分钟向服务器请求一次倒计时时间，倒计时时间为0时，刷新界面
    setInterval(times_show,60000)
    //每秒进行倒计时
    setInterval(times_down,1000)

    // 搜索栏添加列表
    function addlist(goods_name) {
        $('<a/>',{
            text:goods_name,
            class:'list-group-item list-group-item-action ' +
                'list-group-item-secondary col-11 select_list',
            style:"z-index: 999;opacity:0.95"
        }).appendTo($('#search_list'))
    }
    //点击搜索出来的列表，点击内容填入信息，然后隐藏列表
    function goods_select() {
        $(".select_list").click(function () {
            var goods_name  = $(this).text()
            $('#search_input').val(goods_name)
            $('.select_list').hide()
        })

    }
    // 购物车增加,异步传输给后端，修改数据库参数
    function add_cart(goods_id){
        $("#add_"+goods_id).click(function () {
            // 购物车增加，改变购物车图片，显示输入框和减量框
            $("#text_"+goods_id).css('visibility','visible');
            $("#subtract_"+goods_id).css('visibility','visible');
            $("#add_"+goods_id).attr('src','/static/img/icons/cart-plus.svg')
            var number = parseInt($("#text_"+goods_id).text())
            $("#text_"+goods_id).text(number += 1)
            // 异步改变购物车徽章数量，并传入数据库
            $.ajax({
                url:"/cart/cart_change/",
                data:{
                    "goods_id":goods_id,
                    "csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val(),
                    "cart_number": parseInt($("#text_"+goods_id).text()),
                    "cart_type": "add"
                    },
                type:"POST",
                async:true,
                success:function (cart_goods_quantity_sum_dic) {
                    cart_goods_quantity_sum= JSON.parse(cart_goods_quantity_sum_dic).cart_goods_quantity__sum
                    $("#cart_badge").html(cart_goods_quantity_sum)
            }

            })
        })
    }
    // 购物车减少，异步传输给后端，修改数据库参数
    function subtract_cart(goods_id){
        $("#subtract_"+goods_id).click(function () {
            var number = parseInt($("#text_"+goods_id).text())
            // 判断购物车数量，=0隐藏图片，>0异步传入数据库
            if (number == 1) {
                $("#add_"+goods_id).attr('src','/static/img/icons/cart.svg');
                $("#text_"+goods_id).css('visibility','hidden');
                $("#subtract_"+goods_id).css('visibility','hidden');
            }else if (number > 0 ){
                $("#text_"+goods_id).text(number -= 1)
                $.ajax({
                url:"/cart/cart_change/",
                data:{"goods_id":goods_id,
                      "csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val(),
                      "cart_number": parseInt($("#text_"+goods_id).text()),
                      "cart_type" : "subtract"
                    },
                type:"POST",
                async:true,
                success:function (cart_goods_quantity_sum_dic) {
                    cart_goods_quantity_sum= JSON.parse(cart_goods_quantity_sum_dic).cart_goods_quantity__sum
                    $("#cart_badge").html(cart_goods_quantity_sum)
            }

            })

            }
            else {
                alert('购买商品不能为负数')
            }
        })
    }
    //向服务器发起请求，显示优惠倒计时
    function times_show() {
            var server_date = new Date($.ajax({async:false}).getResponseHeader("Date"))
            // var server_local_time = server_date.toLocaleTimeString('korea',{hour12:false})
            var endtime = new Date(server_date.getFullYear(),server_date.getMonth(),
                server_date.getDate()+1,0,0,0)
            var time_difference = (endtime-server_date)/1000

            var hours = Math.floor(time_difference/3600);
            var modulo = time_difference%3600;
            var minutes = Math.floor(modulo/60);
            var seconds = modulo%60

            hours = times_to_string(hours)
            minutes = times_to_string(minutes)
            seconds = times_to_string(seconds)

            $("#hours_show").text(hours)
            $("#minutes_show").text(minutes)
            $("#seconds_show").text(seconds)

            if (hours=='00'&&minutes=='00'&&seconds=='00'){
                window.location.reload();
            }


        }
    //实现倒计时
    function times_down() {
            var hours = Number($("#hours_show").text())
            var minutes = Number($("#minutes_show").text())
            var seconds = Number($("#seconds_show").text())

            seconds--;
            if (seconds < 0){
                minutes -= 1;
                seconds = 59
            }else if (minutes < 0){
                hours -= 1;
                minutes = 59;
            }else if (hours < 0){
                hours = 23;
            }



            hours = times_to_string(hours)
            minutes = times_to_string(minutes)
            seconds = times_to_string(seconds)

            $("#hours_show").text(hours);
            $("#minutes_show").text(minutes);
            $("#seconds_show").text(seconds);

            if (hours=='00'&&minutes=='00'&&seconds=='00'){
                window.location.reload();
            }





        }
    //将时间的数字类型转换为字符类型
    function times_to_string(times) {
            if (times<10 && times >= 0){
                times = "0" + times
            };
            return times.toString()
        };
    //向服务器请求优惠信息，显示在商品上
    function goods_special_get(){
        $.ajax({
            url:"/goods/",
            data:{"csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val(),},
            type:'POST',
            success:function (goods_preferential_json_list) {
                $.each(goods_preferential_json_list,function (goods_preferential_dic_list_key,goods_preferential_dic) {
                    var goods_id = goods_preferential_dic['goods']
                    var preferential_price = goods_preferential_dic['preferential_price']
                    // $("#goods_preferential_price_"+goods_id).prev().text()
                    $("#goods_preferential_price_"+goods_id).text('￥'+preferential_price)
                })
            }
        })

    }
})

