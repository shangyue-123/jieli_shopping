
$(function () {

    //页面加载时根据显示的商品类别，显示左侧蓝色方块
    var goods_category= $("#get_goods_category").val()
    $('.goods_category_list').removeClass('bg-primary text-white')
    $("#"+goods_category).addClass('bg-primary text-white')

    // 点击购物车，改变数量，上传数据库中增加购物车信息，购物车徽章改变
    // 购物车增加
    $(document).on('click',".add_cart",function () {
                //获取商品id
                var goods_id = this.id.substring(4,)
                // 购物车增加，改变购物车图片，显示输入框和减量框
                $("#text_"+goods_id).css('visibility','visible');
                $("#subtract_"+goods_id).css('visibility','visible');
                $("#add_"+goods_id).attr('src',"{% static 'img/icons/cart-plus.svg' %}")
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
                        $(".badge").html(cart_goods_quantity_sum)
                }

                })
            })
    // 购物车减少
    $(document).on('click',".subtract_cart",function () {
                //获取商品id
                var goods_id = this.id.substring(9,)
                var number = parseInt($("#text_"+goods_id).text())
                // 判断购物车数量，=0隐藏图片，>0异步传入数据库
                if (number == 0) {
                    $("#add_"+goods_id).attr('src',"{% static 'img/icons/cart.svg' %}");
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
                        $(".badge").html(cart_goods_quantity_sum)
                }

                })

                }
                else {
                    alert('购买商品不能为负数')
                }
            })


    //点击搜索图片，跳转商品页并显示搜索商品
    $("#search_img").click(function () {
            window.location.href=window.location.host+"/goods/goods_search/?search_input="+$("#search_input").val()
    })


    //滚动事件，异步请求商品信息，进行局部刷新
    // 遍历查找是否有特价商品，有的话显示特价，划出原价
    //点击左侧商品类别，刷新右侧商品
    $(".goods_preferential_show").hide()
    goods_special_get()
    scroll_get_goods()

    //点击左侧商品类别，刷新右侧商品
    $(".goods_category_list").click(function () {
        var goods_category = this.id
        var time = 0
        $('#goods_show').load("/goods/product_list/?time="+time+"&goods_category="+goods_category+" #goods_information", function () {
            goods_special_get()
        });
        $('.goods_category_list').removeClass('bg-primary text-white')
        $("#"+goods_category).addClass('bg-primary text-white')
        goods_special_get()
    })

    // 实时搜索
    $("#search_input").keyup(function () {
            goods_search_show();
        });

    //显示搜索的商品
    function goods_search_show() {
            $(".media").hide();
            var search_input = $("#search_input").val()
            $(".search_name").each(function () {
                var search_name = $(this).text()
                var judge = search_name.indexOf(search_input)
                if (judge > -1) {
                        $(this).parents(".media").show()
                };

            });

        };
    //获取特价商品
    function goods_special_get(){
        $.ajax({
            url:"",
            data:{"csrfmiddlewaretoken": $("[name = 'csrfmiddlewaretoken']").val(),},
            type:'POST',
            success:function (goods_preferential_json_list) {
                $.each(goods_preferential_json_list,function (goods_preferential_dic_list_key,goods_preferential_dic) {
                    var goods_id = goods_preferential_dic['goods']
                    var preferential_price = goods_preferential_dic['preferential_price']
                    $('#sell_price_'+goods_id).addClass("text-black-50 ").css('text-decoration','line-through')
                    $('#sell_price_'+goods_id).prev().addClass("text-black-50 ").css('text-decoration','line-through')
                    $("#"+goods_id).next().show()
                    // $("#goods_preferential_price_"+goods_id).prev().text()
                    $("#goods_preferential_price_"+goods_id).text('￥'+preferential_price)
                })
            }
        })

    }
    //滚动获取商品
    function scroll_get_goods() {
        var time = Number(1)
        var goods_count = $("#get_count").val()
        //获取检索次数
        var time_count = Math.ceil(goods_count/10)
        //滚动事件，异步请求商品信息，进行局部刷新
        $(window).scroll(function () {
            //全部内容高度
            var page_full = $(document).height()
            //页面高度
            var page_window = $(window).height()
            //滚动高度
            var bar_height = $(window).scrollTop()
            //获取商品类别
            var goods_category = $('.bg-primary')[0].id

            //动态刷新商品
            if (page_full-(bar_height+page_window) < 400 && time <= time_count){
                $('#goods_show_'+time).load("?time="+time+"&goods_category="+goods_category+" .media")
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

