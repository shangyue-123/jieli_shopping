$(function () {
    $("#previous_page").click(function () {
        window.history.back(-1);

    })
    show_order_message()

    //点击左侧按钮，异步提交修改
    $(document).on('click',".button_change_left",function () {
        var order_id = this.id.slice(13)
        var order_status = Number($('#get_order_status_'+order_id).val());
        value_change_left(order_id,order_status)
    })
    //点击右侧按钮，异步提交
    $(document).on('click',".button_change_right",function () {
        var order_id = this.id.slice(19)
        var order_status = Number($('#get_order_status_'+order_id).val());
        value_change_right(order_id,order_status);
    })
    //滚动获取订单
    scroll_get_goods()

    function show_order_message() {
        //遍历所有ul显示订单状态
        $("ul").each(function () {
        var order_id = this.id;
        var order_status = Number($('#order_status_'+order_id).text());
        order_status_show(order_id,order_status)
        button_change_left(order_id,order_status)
        button_change_right(order_id,order_status)
        // button_change(order_id)
        show_price(order_id)
    });
    }
    //根据order_status显示订单状态
    function order_status_show(order_id,order_status) {
            switch (order_status) {
                case 0:
                    // $('#pay_'+order_id).css('visibility','visible');
                    $('#order_status_'+order_id).text('待支付');
                    break;
                case 1:
                    $('#order_status_'+order_id).text('待发货');
                    break;
                case 2:
                    $('#order_status_'+order_id).text('待收货');
                    // $('#pay_'+order_id).css('visibility','visible');
                    // $('#pay_'+order_id).val('已收货');
                    break;
                case 3:
                    $('#order_status_'+order_id).text('已收货');
                    // $('#pay_'+order_id).css('visibility','visible');
                    // $('#pay_'+order_id).val('退货');
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
                case 1:
                    $('#value_change_'+order_id).text('取消订单');
                    break;
                case 2:
                    $('#value_change_'+order_id).text('不可取消').addClass('bg-secondary');
                    // $('#value_change_'+order_id).text('客户已收货');
                    // $('#value_change_'+order_id).click(order_status_change_6(order_id));
                    break;
                case 3:
                    $('#value_change_'+order_id).text('退货');
                    // $('#value_change_'+order_id).click(order_status_change_8(order_id))
                    break;
                case 4:
                    $('#value_change_'+order_id).text('取消换货');
                    // $('#value_change_'+order_id).click(order_status_change_3(order_id))
                    break;
                case 5:
                    $('#value_change_'+order_id).text('取消退货');
                    // $('#value_change_'+order_id).click(order_status_change_3(order_id))
                    break;
                case 6:
                    $('#value_change_'+order_id).css('visibility','hidden');
                    break;
                case 7:
                case 9:
                case 10:
                    $('#value_change_'+order_id).text('删除订单');
                    break;
            };
        };
    //点击左侧按钮，异步提交信息，弹出提交成功警告框
    function value_change_left(order_id,order_status) {
        var order_status_change = order_status
        var url = "http://" + window.location.host + "/order/order_status_change/"
        switch (order_status) {
            case 0:
            case 1:
                order_status_change = 6
                break;
            case 2:
                order_status_change = order_status
                break;
            case 3:
                order_status_change = 5
                break;
            case 4:
                order_status_change = 11
                break;
            case 5:
                order_status_change = 12
                break;
            case 6:
                order_status_change = order_status
                break;
            case 7:
            case 9:
            case 10:
                order_status_change = order_status
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
    //根据订单状态改变右侧按钮功能
    function button_change_right(order_id,order_status) {
        // var order_status = Number($('#order_status_'+order_id).text());
        // console.log(order_status)
        // var payment_amount= $("#payment_method_"+order_id).text();
        switch (order_status) {
                case 0:
                    $('#value_change_right_'+order_id).text('支付').addClass('bg-danger');
                    break;
                case 1:
                    $('#value_change_right_'+order_id).text('更改地址').css('visibility','hidden');
                case 2:
                    $('#value_change_right_'+order_id).text('确认收货');
                    // $('#value_change_'+order_id).click(order_status_change_6(order_id));
                    break;
                case 3:
                    $('#value_change_right_'+order_id).text('换货');
                    // $('#value_change_'+order_id).click(order_status_change_8(order_id))
                    break;
                case 4:
                    $('#value_change_right_'+order_id).css('visibility','hidden');
                    // $('#value_change_'+order_id).click(order_status_change_3(order_id))
                    break;
                case 5:
                    $('#value_change_right_'+order_id).css('visibility','hidden');
                    // $('#value_change_'+order_id).click(order_status_change_3(order_id))
                    break;
                case 6:
                    $('#value_change_right_'+order_id).css('visibility','hidden');
                    break;
                case 7:
                case 9:
                case 10:
                    $('#value_change_right_'+order_id).css('visibility','hidden')
            };
        };
    //遍历所有右边按钮，点击按钮修改数据库参数并刷新界面
    function value_change_right(order_id,order_status) {
        var order_status_change = order_status
        var url = "http://" + window.location.host + "/order/order_status_change/"
        switch (order_status) {
                case 0:
                    alert('暂不支持网上支付')
                    break;
                case 1:
                    alert('地址修改功能开发中')
                    break;
                case 2:
                    order_status_change = 3;
                    // $('#value_change_'+order_id).click(order_status_change_6(order_id));
                    break;
                case 3:
                    order_status_change = 4;
                    // $('#value_change_'+order_id).click(order_status_change_8(order_id))
                    break;
                case 4:
                case 5:
                case 6:
                    alert('暂无此功能')
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
    //计算总价并显示
    function show_price(order_id) {
        var li = $("ul[id='"+order_id+"'] li").slice(1,-1)
        var total_price  = 0
        $(li).each(function () {
            var goods_id = this.id;
            console.log(order_id)
            var goods_sell_price = $("#goods_sell_price_"+order_id+'_'+goods_id).text();
            var cart_goods_quantity = $("#cart_goods_quantity_"+order_id+'_'+goods_id).text();
            var price = goods_sell_price * cart_goods_quantity
            total_price += price
        });
        $('#total_'+order_id).text(total_price)
    }
    //滚动获取订单
    function scroll_get_goods() {
        var time = Number(1)
        var order_count = $("#get_count").val()
        //获取检索次数
        var time_count = Math.ceil(order_count/5)
        //滚动事件，异步请求商品信息，进行局部刷新
        $(window).scroll(function () {
            //全部内容高度
            var page_full = $(document).height()
            //页面高度
            var page_window = $(window).height()
            //滚动高度
            var bar_height = $(window).scrollTop()
            console.log(page_full-(bar_height+page_window))

            //动态刷新商品
            if (page_full-(bar_height+page_window) < 400 && time <= time_count){
                $('#order_show_'+time).load("?time="+time+" .order_show",function () {
                    show_order_message()
                })
                $("#order_show_"+time).after(
                    $("<div/>",{
                        'id':'order_show_'+(time+1)
                    })
                )
                time = time+1
            }
        })
    }
    })