// 界面面刷新显示购物车商品数量
$(function () {
    // 异步显示购物车徽章数量
    $.ajax({
        url:"/cart/cart_number/",
        data:{
            "csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val()
        },
        type:"POST",
        async:true,
        success:function (cart_goods_quantity_sum_dic) {
            cart_goods_quantity_sum= JSON.parse(cart_goods_quantity_sum_dic).cart_goods_quantity__sum
            $("#cart_badge").html(cart_goods_quantity_sum);
        }
    })
    // 徽章超过99显示99+，=0隐藏
    $("#cart_badge").bind('DOMNodeInserted',function () {
        if ($("#cart_badge").text() > 99){
            $("#cart_badge").text("99+");
        }else if ($("#cart_badge").text() < 0){
            $("#cart_badge").css('visibility','hidden');
        }

    })
})