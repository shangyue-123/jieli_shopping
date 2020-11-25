$(function () {
        // 点击修改图标进入信息变更界面
        $(".image").click(function () {
        var url_search = window.location.search
        console.log(this)
        var consignee_id_get = $(this).attr("id");
        console.log(consignee_id_get)
        var consignee_name_get = $("#consignee_name_"+consignee_id_get).text()
        var consignee_number_get = $("#consignee_number_"+consignee_id_get).text()
        var consignee_address_get = $("#consignee_address_"+consignee_id_get).text()
        console.log(consignee_name_get,consignee_number_get,consignee_address_get)
        var url = "http://" + window.location.host + "/user/address/"+url_search
        console.log(url)

        var form = $('#submit');
        form.attr('action',url);
        form.attr('method','post');

        var consignee_id = $('<input type="text" name="consignee_id">')
        var consignee_name = $('<input type="text" name="consignee_name">')
        var consignee_number = $('<input type="text" name="consignee_number">')
        var consignee_address = $('<input type="text" name="consignee_address">')

        consignee_id.attr('value',consignee_id_get)
        consignee_name.attr('value',consignee_name_get)
        consignee_number.attr('value',consignee_number_get)
        consignee_address.attr('value',consignee_address_get)

        form.append(consignee_id);
        form.append(consignee_name);
        form.append(consignee_number);
        form.append(consignee_address);

        $(document.body).append(form);
        form.submit();
    })
        //点击按钮，新建收货信息
        $(":button").click(function () {
            var url_search = window.location.search
            if (url_search == ''){
                window.location.href="http://" + window.location.host + "/user/address/address_change/"
            }else {
                window.location.href="http://" + window.location.host + "/user/address/address_change/"+url_search
            }

        })
        //点击上一页图标，返回上一页
        $("#previous_page").click(function () {
            window.history.back(-1);

        })
        //如果order_id不为空点击地址卡片，传入地址信息给数据库，
        //如果order_id为空则点击无效
        $(".order_address_change").click(function () {
            var order_id = $('#order_id_get').val()
            console.log(order_id)
            if (order_id == 'None' || order_id == ''){
                console.log('进入if函数')
            }else {
                console.log('进入else函数')
                var consignee_name = $(this).children().first().text()
                var consignee_number = $(this).children().first().next().text()
                var consignee_address = $(this).children().last().text()
                console.log(consignee_name)
                console.log(consignee_number)
                console.log(consignee_address)
                var url = "http://"+window.location.host+"/pay/pay_address_change/"
                var form = $('#submit_address_change');
                form.attr('action',url);
                form.attr('method','post');
                var input_consignee_name = $('<input type="text" name="consignee_name">')
                var input_consignee_number = $('<input type="text" name="consignee_number">')
                var input_consignee_address = $('<input type="text" name="consignee_address">')
                var input_order_id = $('<input type="text" name="order_id">')

                input_consignee_name.attr('value',consignee_name)
                input_consignee_number.attr('value',consignee_number)
                input_consignee_address.attr('value',consignee_address)
                input_order_id.attr('value',order_id)

                form.append(input_consignee_name)
                form.append(input_consignee_number)
                form.append(input_consignee_address)
                form.append(input_order_id)

                $(document.body).append(form);
                form.submit();

                }
        })








    })