$(function () {
    //定义全局变量


    // 勾选商品改变总价,全选按钮，购物车数量变化并异步到数据库
    Total();
    //页面加载，获取特价商品信息
    goods_special_get()
    //滚动事件
    scroll_get_goods()

    // 复选框点击调用计算函数,如果所有商品按钮选择，全选按钮被选择
    $(".calculate_price").click(function () {
        if ($(".calculate_price:checked").length === $(".calculate_price").length){
            $("#all_select").prop("checked",true)
        }else {
            $("#all_select").prop("checked",false)
        }

        Total();

        });
    // 点击全选和取消全选
    $('#all_select').click(function () {
        if (this.checked){
            $(".calculate_price").prop("checked",true);
        }else {
            $(".calculate_price").prop("checked",false);
        }
        Total();
    });
    //点击商品数量加减，异步更改购物车数量并上传数据库
    // 点击加号事件
    $(".cart_add").click(function () {
        var goods_id = this.id.substring(9,)
        console.log(goods_id)
        $.ajax({
            url:"/cart/cart_change/",
            data:{
                "goods_id": goods_id,
                "csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val(),
                "cart_number": parseInt($("#cart_goods_quantity_"+goods_id).text()),
                "cart_type" : "add",
            },
            type:"POST",
            async:true,
            success:function (cart_goods_quantity_sum_dic) {
                cart_goods_quantity_sum= JSON.parse(cart_goods_quantity_sum_dic).cart_goods_quantity;
                $("#cart_goods_quantity_"+goods_id).html(cart_goods_quantity_sum);
                Total();
            }
        })


    })
    // 点击减号事件
    $(".cart_dash").click(function () {
        var goods_id = this.id.substring(10,)
        console.log(goods_id)
        $.ajax({
            url:"/cart/cart_change/",
            data:{
                "goods_id": goods_id,
                "csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val(),
                "cart_number": parseInt($("#cart_goods_quantity_"+goods_id).text()),
                "cart_type" : "subtract",
            },
            type:"POST",
            async:true,
            // 成功时改变购物车数量，如果数量为0，则删除元素
            success:function (cart_goods_quantity_sum_dic) {
                cart_goods_quantity= JSON.parse(cart_goods_quantity_sum_dic).cart_goods_quantity;
                if (cart_goods_quantity == 0){
                    $("#head_"+goods_id).remove()
                }else {
                    $("#cart_goods_quantity_"+goods_id).html(cart_goods_quantity);
                };
                Total();
            }
        })


    })

    // 实时模糊搜索
    $("#search_input").keyup(function () {
            var i = 1
            $(".media").hide();
            var search_input = $("#search_input").val()
            $(".search_name").each(function () {
                var search_name = $(this).text()
                var judge = search_name.indexOf(search_input)
                // 避免商品信息被搜索栏遮住
                if (judge > -1) {
                    if (i == 1) {
                        $(this).parents(".media").show().addClass("mt-5");
                        i += 1
                    } else {
                        $(this).parents(".media").show()
                    }
                };
            })
        })

    // 点击结算，提交商品
    $(":button").click(function () {
            var goods_message = {};
            var i = 0;
            var payment_amount = $('#sum_price').text()
            // 遍历所有商品
            $(".calculate_price").each(function () {
                // 确定勾选状态
                var select_state = $(this).prop('checked')
                // 如果勾选
                if (select_state == true){
                    goods_message[i] = {};
                  // 获取商品信息
                    var goods_id = $(this).val()
                    var goods_name = $("#goods_name_"+goods_id).text()
                    var goods_sell_price = $("#goods_sell_price_"+goods_id).text()
                    var cart_goods_quantity = $("#cart_goods_quantity_"+goods_id).text()
                    var goods_image = $("#goods_image_"+goods_id).attr('src')


                    var url ="http://"+window.location.host+"/pay/"
                    // 创建提交表单跳转
                    var form = $('#submit');
                    form.attr('action',url);
                    form.attr('method','post');

                    // 信息放入字典中
                    goods_message[i]['goods_id'] = goods_id;
                    goods_message[i]['goods_sell_price'] = goods_sell_price;
                    goods_message[i]['goods_name'] = goods_name
                    goods_message[i]['cart_goods_quantity'] = cart_goods_quantity
                    goods_message[i]['goods_image'] = goods_image
                    var input_goods_message = $('<input type="text" name="goods_message">')
                    var input_payment_amount = $('<input type="text" name="payment_amount">')
                    goods_message_json = JSON.stringify(goods_message)
                    input_goods_message.attr('value',goods_message_json)
                    input_payment_amount.attr('value',payment_amount)
                    form.append(input_goods_message)
                    form.append(input_payment_amount)
                    $(document.body).append(form);
                    form.submit();
                    i+=1
                };

            });
        })




    //异步获取商品信息
    function goods_special_get() {
            $.ajax({
            url:"",
            data:{"csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val(),},
            type:'POST',
            success:function (goods_preferential_json_list) {
                $.each(goods_preferential_json_list,function (goods_preferential_dic_list_key,goods_preferential_dic) {
                    console.log(goods_preferential_dic)
                    var goods_id = goods_preferential_dic['goods']
                    var preferential_price = goods_preferential_dic['preferential_price']
                    var preferential_span = $("<span/>",{
                        "class":'badge badge-pill badge-warning ml-1',
                        "id":"badge_"+goods_id,
                        'text': '特价商品'
                    })
                    if ($("#badge_"+goods_id).length == 0){
                        $('#goods_sell_price_'+goods_id).after(preferential_span)
                        $('#goods_sell_price_'+goods_id).text(preferential_price)
                    }

                })



            }
        })

        }
    // 计算勾选总价
    function Total(){
        var sum_number = 0;
        $(".calculate_price").each(function () {
            var checked = $(this).prop("checked");
            if(checked == true){
                var id = $(this).val();
                var number = $("#goods_sell_price_"+id).text();
                var quantity =$("#cart_goods_quantity_"+id).text();
                sum_number += number * quantity
            }
            $("#sum_price").text(sum_number.toFixed(2))
        })
    }
    //滚动事件，异步请求商品信息，进行局部刷新
    function scroll_get_goods() {
        //定义加载次数
        var time = Number(1)
        //定义可以加载的商品数量
        var goods_count = $("#get_count").val()
        //获取检索次数
        var time_count = Math.ceil(goods_count/15)
        //滚动事件，异步请求商品信息，进行局部刷新
        console.log(time)
        $(window).scroll(function () {
            //全部内容高度
            var page_full = $(document).height()
            //页面高度
            var page_window = $(window).height()
            //滚动高度
            var bar_height = $(window).scrollTop()

            //动态刷新商品
            if (page_full-(bar_height+page_window) < 400 && time <= time_count){
                $('#goods_show_'+time).load("?time="+time+" .media")
                $("#goods_show_"+time).after(
                    $("<div/>",{
                        'id':'goods_show_'+(time+1)
                    })
                )
                time = time+1
                goods_special_get()
            }
        })
    }

})