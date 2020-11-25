    $(function () {
        // 页面加载计算总价
        sum_price()
        // 点击加号增加数量，计算总价
        $('.cart_add').click(function () {
            var cart_goods_quantity = Number($(this).next().text())
            console.log(cart_goods_quantity)
            $(this).next().text(cart_goods_quantity+1)
            sum_price()
        })
        //点击减号减少数量，计算总价,数量为0时，删除元素
        $('.cart_dash').click(function () {
            var cart_goods_quantity = Number($(this).prev().text())
            console.log(cart_goods_quantity)
            if (cart_goods_quantity == 1){
                $(this).parents('.pay_list').remove()
            }else {
                $(this).prev().text(cart_goods_quantity-1)
            }
            sum_price()


        })
        //判断收件信息是否为空，为空则提醒输入信息，不为空则提交订单
        $("#order_submit").click(function () {
            //获取地址信息
            var consignee_address_get = $('#consignee_address').text().substring(3,);
            var consignee_name_get = $('#consignee_name').text().substring(4,);
            var consignee_number_get = $('#consignee_number').text().substring(5,);
            // console.log(consignee_address_get,consignee_name_get,consignee_number_get)
            var goods_json_get = {};
            var i = 0;
            var goods_id_arr = {}
             //判断收货地址是否为空
             if (consignee_address_get.length == 0 && consignee_name_get.length == 0 && consignee_number_get.length == 0 ){
                alert('请填写收货信息')
            } else {
                //向goods_id_list中添加商品id
                // 遍历添加商品信息
                $(".pay_list").each(function () {
                    goods_json_get[i] = {};
                    var goods_id = $(this).attr("id");
                    var goods_image = $("#goods_image_"+goods_id).attr("src")
                    var goods_name = $("#goods_name_"+goods_id).text()
                    var goods_sell_price = $("#goods_sell_price_"+goods_id).text()
                    var cart_goods_quantity = $("#cart_goods_quantity_"+goods_id).text()

                    goods_id_arr[goods_id] = cart_goods_quantity

                    goods_json_get[i]['goods_id'] = goods_id;
                    goods_json_get[i]['goods_image'] = goods_image;
                    goods_json_get[i]['goods_name'] = goods_name;
                    goods_json_get[i]['goods_sell_price'] = goods_sell_price;
                    goods_json_get[i]['cart_goods_quantity'] = cart_goods_quantity;
                    // goods_json_get[i]['consignee_address'] = consignee_address;
                    // goods_json_get[i]['consignee_name'] = consignee_name;
                    // goods_json_get[i]['consignee_number'] = consignee_number;
                    // goods_json_get[i]['user_name'] = user_name;

                    i+=1
                });
                var goods_json = JSON.stringify(goods_json_get)
                var goods_id_json = JSON.stringify(goods_id_arr)
                // console.log(goods_id_json)
                // console.log(goods_json)
                // 获取支付方式和支付金额
                var payment_method_get = $("input[type='radio']:checked").val();
                var payment_amount_get = $("#sum_price").text()
                // 获取订单ID
                var order_id_get = $("#order_id_get").val()
                // 提交地址
                var url = "http://" + window.location.host + "/pay/submit_order/"

                //获取使用积分数,待完成
                var integral_number_get = $("#integral_input").val()
                if (integral_number_get == ''){
                    integral_number_get = 0
                }

                var form = $("#submit");
                form.attr('action',url);
                form.attr('method','post');

                var goods_json_input = $('<input type="text" name="goods_json">')
                var payment_method = $('<input type="text" name="payment_method">')
                var payment_amount = $('<input type="text" name="payment_amount">')
                var consignee_name = $('<input type="text" name="consignee_name">')
                var consignee_address = $('<input type="text" name="consignee_address">')
                var consignee_number = $('<input type="text" name="consignee_number">')
                var order_id = $('<input type="text" name="order_id">')
                var integral_number = $('<input type="number" name="integral_number">')


                goods_json_input.attr('value',goods_json)
                payment_method.attr('value',payment_method_get)
                payment_amount.attr('value',payment_amount_get)
                consignee_name.attr('value',consignee_name_get)
                consignee_address.attr('value',consignee_address_get)
                consignee_number.attr('value',consignee_number_get)
                order_id.attr('value',order_id_get)
                integral_number.attr('value',integral_number_get)



                form.append(goods_json_input)
                form.append(payment_method)
                form.append(payment_amount)
                form.append(consignee_name)
                form.append(consignee_address)
                form.append(consignee_number)
                form.append(order_id)
                form.append(integral_number)

                $(document.body).append(form);
                form.submit();

                $.ajax({
                    url:"goods_sell_volume_add/",
                    data:{
                        "goods_id_json":goods_id_json,
                        "csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val()
                    },
                    type:"POST",
                    success:function () {
                        console.log('更改销量成功')
                    }
                })
                alert('订单提交成功')
            };
        });
        //点击修改地址
        $("#address_change").click(function () {
            var order_id=$('#order_id_get').val()
            window.location.href="/address/?order_id="+order_id
    });
        //点击积分,弹出模态框
        $("#integral_use").click(function () {
            $('#integral_modal').modal()
        })
        //点击全部使用将积分全部填入输入框,并计算预计节省
        $("#integral_all").click(function () {
            var integral_number = $("#integral_number").text()
            $("#integral_input").val(integral_number)
            var amount_number = discounts_integral(integral_number)
            $("#save_amount").text(amount_number)
        })

        //输入使用积分数量时，实时显示节省金额,如果积分大于拥有积分，限制输入
        $("#integral_input").keyup(function () {
            var integral_number_all = $("#integral_number").text()
            var integral_input_str = $("#integral_input").val().replace(/[^\d]/g,'');
            $("#integral_input").val(integral_input_str)

            var integral_input = parseFloat(integral_input_str)
            if (integral_number_all < integral_input){
                integral_input = integral_number_all
                $("#integral_input").val(integral_number_all)
            }
            var amount_number = discounts_integral(integral_input)
            $("#save_amount").text(amount_number)




        })
        //点击确定使用按钮，计算预计节省金额
        $("#sure_use_integral").click(function () {
            var save_amount = $("#save_amount").text()
            console.log(save_amount)
            if (save_amount == '0.00' | save_amount == '0'){
               $("#show_amount_integral").removeClass('text-danger')
               $("#show_amount_integral").text('去选择')
               $("#integral_modal").modal('hide')
            }else {
                $("#show_amount_integral").text('预计节省:￥'+save_amount)
                $("#show_amount_integral").addClass('text-danger')
                var sum_price = discounts_sum_price()
                if (sum_price < 0 ){
                    $("#show_amount_integral").text('去选择')
                    $("#show_amount_integral").removeClass('text-danger')
                    $("#integral_input").val('');
                    $("#save_amount").text('0')
                    alert('订单总价不能为负值')
                    discounts_sum_price()
                }else {
                    $("#integral_modal").modal('hide')
                }
            }



        })
        //点击右上角关闭图标，清空输入框内容
        $('#close').click(function () {
            $("#integral_input").val('');
            $("#save_amount").text('0')
        })
        //点击关闭窗口，清空输入框内容
        $("#close_button").click(function () {
            $("#integral_input").val('');
            $("#save_amount").text('0')
        })
        // 计算优惠总价
        function sum_price() {
            var sum_price = 0;
            $(".pay_list").each(function () {
                var goods_id = $(this).attr('id')
                var goods_sell_price = $("#goods_sell_price_" + goods_id).text()
                var cart_goods_quantity = $("#cart_goods_quantity_" + goods_id).text()
                // console.log(goods_id, goods_sell_price, cart_goods_quantity)
                sum_price += goods_sell_price * cart_goods_quantity

            });
            // console.log(sum_price)
            // $('#sum_price').text('￥' + sum_price)
            $('#sum_price_discounts').text('￥' + sum_price)
            discounts_sum_price()
        }
        //计算积分优惠金额
        function discounts_integral(integral_input) {
            if (isNaN(integral_input)){
                var amount_number = 0
            }else {
                 var amount_number = (integral_input/100).toFixed(2);
            }
            return amount_number
        }
        //计算优惠后的总价
        function discounts_sum_price() {
            var sum_price = parseFloat($("#sum_price_discounts").text().substr(1,))
            var carriage =parseFloat($('#carriage').text().substr(1,))
            var discounts_price_sum = 0
            $('.discounts_price').each(function () {
                var discounts_price = parseFloat($(this).text().substr(6,))
                if (isNaN(discounts_price)){
                    discounts_price_sum += 0
                }else {
                    discounts_price_sum = discounts_price_sum+discounts_price
                }
            })
            sum_price = sum_price-discounts_price_sum+carriage
            $("#discounts_sum_price").text('￥'+sum_price)
            $("#sum_price").text('￥'+sum_price)
            return sum_price
        }

    });