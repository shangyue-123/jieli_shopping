//页面加载前隐藏卡片详情
(function ($) {
    $('.card-body').hide()
    $('.card-footer').hide()
    $('.card_show').click(function () {
        var order_id = this.id
        $('#card_body_'+order_id).toggle();
        $('#card_foot_'+order_id).toggle();
    });

})(jQuery)
//页面加载修改按钮内容，更改功能
$(function () {
    //遍历显示卡片内容
    $(".card_show").each(function () {
        var order_id = this.id
        var order_status = Number($('#order_status_'+order_id).text());
        var order_payment_method = Number($('#payment_method_'+order_id).text());
        button_change_left(order_id,order_status)
        button_change_right(order_id,order_status)
        order_status_show(order_id,order_status)
        order_status_text_show(order_id,order_status)
        payment_method_show(order_id,order_payment_method)
        // $('#value_change_'+order_id).click(value_change(order_id,order_status))
    })
    //计时器异步查找新订单
    setInterval(order_new,10000)

    //左侧按钮提交
    $(".button_change_left").click(function () {
        var order_id = this.id.slice(13)
        var order_status = Number($('#get_order_status_'+order_id).val());
        value_change_left(order_id,order_status)
    });
    //右侧按钮提交
    $(".button_change_right").click(function () {
        var order_id = this.id.slice(19)
        var order_status = Number($('#get_order_status_'+order_id).val());
        value_change_right(order_id,order_status);
    })

    //点击搜索按钮按钮，显示订单信息
    $(".order_select").click(function () {
        $('.order_select').not(this).removeClass("bg-primary")
        $('.order_all').removeClass("bg-primary")
        $(this).addClass("bg-primary")


        $("div[class='card']").hide()
        var order_status = this.id
        $("input[value='"+order_status+"']").parents('.card').show()
    });
    $(".order_all").click(function () {
        $(this).addClass("bg-primary")
        $('.order_select').removeClass("bg-primary")
        $("div[class='card']").show()
    })

    // 实时搜索
    $("#search_input").keyup(function () {
        var search_input = $("#search_input").val()
        $('.order_all').removeClass("bg-primary")
        $('.order_select').removeClass("bg-primary")
        $(".card").hide()
        console.log(search_input)
        var search = $(".card").find('span').filter(":contains('"+search_input+"')")
        console.log(search)
        search.parents(".card").show();


    })

    //异步查询新订单，有订单动态添加
    function order_new() {
        var order_id = $("#get_order_id_max").val()
        $.ajax({
            url:"order_new/",
            data:{
                'order_id':order_id,
                "csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val()
            },
            type:'POST',
            dataType:"json",
            success:function (order_dic_tuple) {
                // console.log(order_dic_tuple)
                // console.log(typeof order_dic_tuple)
                var order_dic_json = JSON.parse(order_dic_tuple)
                console.log(order_dic_json)
                // console.log(typeof order_dic_json)
                $.each(order_dic_json,function (index,value) {
                    // console.log(index)
                    // console.log(value)
                    order_add(index,value)
                })
            }
        })

    }
    //动态添加的标签内容
    function order_add(index,value) {
        //获取JSON中的订单ID
        var order_id = value.pk
        //获取JSON中的订单创建时间
        var order_time = value.fields.order_time
        //取出订单创建时间的日期字符串
        var order_time_data = new Date(order_time).toLocaleDateString()
        //取出订单创建时间的时间字符串
        var order_time_time = new Date(order_time).toLocaleTimeString('korea',{hour12:false}).substring(0,5)
        //将日期字符串按照"/"进行分割
        var order_time_data_array = order_time_data.split('/')
        //获取JSON中的订单状态
        var order_status = Number(value.fields.order_status);
        //获取JSON中的支付方式
        var order_payment_method = Number(value.fields.payment_method);

        //将接收到的最大id标记
        $("#get_order_id_max").val(value.pk)
        // console.log(order_id)
        //创建卡片标签，并向标签内添加卡片头，卡片身体，卡片脚
        var div_card = $("<div/>",{
            "class":"card",
        }).append(
            $("<div/>",{
            "class":"card-header card_show",
            "id":order_id,
            }),
            $("<div/>",{
            "class":"card-body",
            "id":"card_body_"+order_id,
            }),
            $("<div/>",{
            "class":"card-footer",
            "id":"card_foot_"+order_id,
            }),
        )
        //将卡片放在所有订单的最上方
        $("#get_order_id_max").after(div_card)
        // console.log('完成添加卡片三部分')
        // 往卡片头内添加内容
        var div_card_header_img = $("<img/>",{
                "class":"float-right pt-1",
                "src":"../../static/img/icons/chevron-down.svg",

            });
        var div_card_header_span_1 = $("<span/>",{
               "text":"用户名："+value.fields.user_name ,
            });
        var div_card_header_span_2 = $("<span/>",{
               "class":"float-right mr-3",
               "id":"order_status_" +value.pk,
               "text":value.fields.order_status,
            });
        var div_card_header_span_3 = $("<span/>",{
            "class":"badge badge-pill badge-warning ml-1",
            "text":"新订单"
        })
        // console.log($("#"+order_id).id)
        // console.log(div_card_header_img,div_card_header_span_1,div_card_header_span_2)
        $("#"+order_id).append(div_card_header_img, div_card_header_span_1,div_card_header_span_3, div_card_header_span_2)


        //往卡片身体里添加三部分内容
        var card_text_1 = $("<p/>",{
            "class":"card-text h5"
        });
        var card_text_2 = $("<p/>",{
            "class":"card-text border-top mb-0 mt-1"
        });
        var card_text_3 = $("<p/>",{
            "class":"card-text border-top border-bottom mt-1"
        })
        //卡片身体三部分加入到卡片中间
        $("#card_body_"+order_id).append(card_text_1,card_text_2,card_text_3)

        //向卡片身体三部分中的第一部分添加标签
        var card_text_1_span = $("<span/>",{
            "text":"商品名称和数量："
        })
        var card_text_1_br = $("<br>")
        $("#card_body_"+order_id+" p:first-child").append(card_text_1_span,card_text_1_br)
        $.each(value.fields.goods_json,function (i,v) {
            // console.log("进入到each函数")
            var card_text_1_span_1 = $("<span/>",{
                "text":v.goods_name,
            });
            var card_text_1_span_2 = $("<span/>",{
                "text":"*"+v.cart_goods_quantity,
            });
            card_text_1.append(card_text_1_span_1,card_text_1_span_2)
        })

        //向卡片身体三部分中的第二部分添加标签
        var card_text_2_span_1 = $("<span/>",{
            "text":"收件人姓名:"
        })
        var card_text_2_span_2 = $("<span/>",{
            "text":value.fields.consignee_name
        })
        var card_text_2_span_3 = $("<span/>",{
            "text":"收件人电话:"
        })
        var card_text_2_span_4 = $("<span/>",{
            "text":value.fields.consignee_number
        })
        var card_text_2_span_5 = $("<span/>",{
            "text":"收件人地址:"
        })
        var card_text_2_span_6 = $("<span/>",{
            "text":value.fields.consignee_address
        })
        $("#card_body_"+order_id+" p:eq(1)").append(
            card_text_2_span_1,card_text_2_span_2,"<br>",
            card_text_2_span_3,card_text_2_span_4,"<br>",
            card_text_2_span_5,card_text_2_span_6,"<br>",
        )

        //向卡片身体三部分中的第三部分添加标签
        var card_text_3_span_1 = $("<span/>",{
            "text":"订单创建时间:"
        });
        var card_text_3_span_2 = $("<span/>",{
            "text":order_time_data_array[0]+"年"+order_time_data_array[1]+
                "月"+order_time_data_array[2]+"日"+" "+order_time_time
        });
        var card_text_3_span_3 = $("<span/>",{
            "text":"支付方式:"
        });
        var card_text_3_span_4 = $("<span/>",{
            "text":value.fields.payment_method,
            "id":"order_payment_method_"+order_id
        });
        var card_text_3_span_5 = $("<span/>",{
            "text":"支付金额:￥"
        });
        var card_text_3_span_6 = $("<span/>",{
            "text":value.fields.payment_amount,
        });
        var card_text_3_input = $("<input/>",{
            "class":"order_status",
            "value":value.fields.order_status,
            "id":"get_order_status_"+order_id,
            "style":"display:none "
        })
        var card_text_3_span_7 = $("<span/>",{
            "text":"订单状态:"
        })
        var card_text_3_span_8 = $("<span/>",{
            "id":"order_status_text_"+order_id,
            "text":value.fields.order_status,
        })
        // var card_text_3_br = $("<br>")
        $("#card_body_"+order_id+" p:last").append(
            card_text_3_span_1,card_text_3_span_2,'<br>',
            card_text_3_span_3,card_text_3_span_4,'<br>',
            card_text_3_span_5,card_text_3_span_6,'<br>',
            card_text_3_input,
            card_text_3_span_7,card_text_3_span_8,'<br>',
        )

        //向卡片脚添加内容
        var card_foot_a_1 = $("<a/>",{
            "class":"btn btn-primary text-white button_change_left",
            "id":"value_change_"+order_id,
            "text":"确认收货",
        });
        var card_foot_a_2 = $("<a/>",{
            "class":"btn btn-primary text-white float-right button_change_right",
            "id":"value_change_right_"+order_id,
            "text":"取消订单",
        })

        $("#card_foot_"+order_id).append(card_foot_a_1,card_foot_a_2)

        button_change_left(order_id,order_status)
        button_change_right(order_id,order_status)
        order_status_show(order_id,order_status)
        order_status_text_show(order_id,order_status)
        payment_method_show(order_id,order_payment_method)

        $("#value_change_"+order_id).click(function (){
            value_change_left(order_id,order_status)
        })
        $("#value_change_right_"+order_id).click(function (){
            value_change_right(order_id,order_status)
        })

        $("#card_body_"+order_id).hide()
        $("#card_foot_"+order_id).hide()
        $("#"+order_id).click(function () {
            $('#card_body_'+order_id).toggle();
            $('#card_foot_'+order_id).toggle();
        })

    }
    //根据order_status在卡片头显示订单状态
    function order_status_show(order_id,order_status) {
            // var order_status = Number($('#order_status_'+order_id).text());
            switch (order_status) {
                case 0:
                    $('#order_status_'+order_id).text('待支付');
                    break;
                case 1:
                    $('#order_status_'+order_id).text('待发货');
                    break;
                case 2:
                    $('#order_status_'+order_id).text('待收货');
                    break;
                case 3:
                    $('#order_status_'+order_id).text('已收货');
                    break;
                case 4:
                    $('#order_status_'+order_id).text('换货');
                    break;
                case 5:
                    $('#order_status_'+order_id).text('退货');
                    break;
                case 6:
                    $('#order_status_'+order_id).text('订单取消中');
                    break;
                case 7:
                    $('#order_status_'+order_id).text('订单已取消');
                    break;
                case 9:
                    $('#order_status_'+order_id).text('完成换货');
                    break;
                case 10:
                    $('#order_status_'+order_id).text('完成退货');
                    break;
                case 11:
                    $('#order_status_'+order_id).text('取消换货');
                    break;
                case 12:
                    $('#order_status_'+order_id).text('取消退货');
                    break;

            };
        };
    //根据订单状态改变左侧按钮功能
    function button_change_left(order_id,order_status) {
        // var order_status = Number($('#order_status_'+order_id).text());
        // var payment_amount= $("#payment_method_"+order_id).text();
        switch (order_status) {
                case 0:
                    $('#value_change_'+order_id).text('已发货');
                    break;
                case 1:
                    $('#value_change_'+order_id).text('已发货');
                    break;
                case 2:
                    $('#value_change_'+order_id).text('客户已收货');
                    // $('#value_change_'+order_id).click(order_status_change_6(order_id));
                    break;
                case 3:
                    $('#value_change_'+order_id).text('退货');
                    // $('#value_change_'+order_id).click(order_status_change_8(order_id))
                    break;
                case 4:
                    $('#value_change_'+order_id).text('完成换货');
                    // $('#value_change_'+order_id).click(order_status_change_3(order_id))
                    break;
                case 5:
                    $('#value_change_'+order_id).text('完成退货');
                    // $('#value_change_'+order_id).click(order_status_change_3(order_id))
                    break;
                case 6:
                    $('#value_change_'+order_id).text('确定取消');
                    break;
                case 7:
                case 9:
                case 10:
                    $('#value_change_'+order_id).text('删除订单');
                    break;
            };
        };
    //根据订单状态改变右侧按钮功能
    function button_change_right(order_id,order_status) {
        // var order_status = Number($('#order_status_'+order_id).text());
        // console.log(order_status)
        // var payment_amount= $("#payment_method_"+order_id).text();
        switch (order_status) {
                case 0:
                case 1:
                case 2:
                    $('#value_change_right_'+order_id).text('取消订单');
                    // $('#value_change_'+order_id).click(order_status_change_6(order_id));
                    break;
                case 3:
                    $('#value_change_right_'+order_id).text('换货');
                    // $('#value_change_'+order_id).click(order_status_change_8(order_id))
                    break;
                case 4:
                    $('#value_change_right_'+order_id).text('取消换货');
                    // $('#value_change_'+order_id).click(order_status_change_3(order_id))
                    break;
                case 5:
                    $('#value_change_right_'+order_id).text('取消退货');
                    // $('#value_change_'+order_id).click(order_status_change_3(order_id))
                    break;
                case 6:
                    $('#value_change_right_'+order_id).text('不可取消');
                    break;
                case 7:
                case 9:
                case 10:
                    $('#value_change_right_'+order_id).hide()
            };
        };
    //根据order_status在卡片中显示订单状态
    function order_status_text_show(order_id,order_status) {
            // var order_status = Number($('#order_status_'+order_id).text());
            switch (order_status) {
                case 0:
                    $('#order_status_text_'+order_id).text('待支付');
                    break;
                case 1:
                    $('#order_status_text_'+order_id).text('待发货');
                    break;
                case 2:
                    $('#order_status_text_'+order_id).text('待收货');
                    break;
                case 3:
                    $('#order_status_text_'+order_id).text('已收货');
                    break;
                case 4:
                    $('#order_status_text_'+order_id).text('换货');
                    break;
                case 5:
                    $('#order_status_text_'+order_id).text('退货');
                    break;
                case 6:
                    $('#order_status_text_'+order_id).text('订单取消中');
                    break;
                case 7:
                    $('#order_status_text_'+order_id).text('订单已取消');
                    break;
                case 9:
                    $('#order_status_text_'+order_id).text('完成换货');
                case 10:
                    $('#order_status_text_'+order_id).text('完成退货');
            };
        };
    //根据payment_method在卡片中显示支付方式
    function payment_method_show(order_id,order_payment_method) {
         switch (order_payment_method) {
                case 0:
                    $('#order_payment_method_'+order_id).text('现金支付');
                    break;
                case 1:
                    $('#order_payment_method_'+order_id).text('微信支付');
                    break;
                case 2:
                    $('#order_payment_method_'+order_id).text('支付宝支付');
                    break;
            };
        };
    //遍历所有左边按钮，点击按钮修改数据库参数并刷新界面
    function value_change_left(order_id,order_status) {
        var order_status_change = order_status
        var url = "http://" + window.location.host + "/order/order_status_change/"
        switch (order_status) {
            case 0:
            case 1:
                order_status_change = 2
                break;
            case 2:
                order_status_change = 3
                break;
            case 3:
                order_status_change = 5
                break;
            case 4:
                order_status_change = 9
                break;
            case 5:
                order_status_change = 10
                break;
            case 6:
                order_status_change = 7
                break;
            case 7:
            case 9:
            case 10:
            case 11:
            case 12:
                order_status_change = 8
                break;
        }
        $.ajax({
            url:url,
            data:{
                "order_id":order_id,
                "order_status":order_status_change,
                "csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val(),
            },
            type:"POST",
            success:function () {
                alert('订单修改成功')
                window.location.reload()
            }
        })

        }
     //遍历所有右边按钮，点击按钮修改数据库参数并刷新界面
    function value_change_right(order_id,order_status) {
        var order_status_change = order_status
        var url = "http://" + window.location.host + "/order/order_status_change/"
        switch (order_status) {
                case 0:
                case 1:
                case 2:
                    order_status_change = 6
                    // $('#value_change_'+order_id).click(order_status_change_6(order_id));
                    break;
                case 3:
                    order_status_change = 4;
                    // $('#value_change_'+order_id).click(order_status_change_8(order_id))
                    break;
                case 4:
                    order_status_change = 11;
                    break;
                case 5:
                    order_status_change = 12;
                    // $('#value_change_'+order_id).click(order_status_change_3(order_id))
                    break;
                case 6:
                    order_status_change = order_status
                    break;
            };
        $.ajax({
            url:url,
            data:{
                "order_id":order_id,
                "order_status":order_status_change,
                "csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val(),
            },
            type:"POST",
            success:function () {
                alert('订单修改成功')
                window.location.reload()
            }
        })
     };
})
