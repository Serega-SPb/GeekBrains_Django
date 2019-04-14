window.onload = function () {
    $('[id^=counter_]').on('click', function(e){
        var pr_id = $(this).closest('tr').attr('id');
        var count = parseInt($(this).parent().children("span").text());
        if ($(this).attr('id').endsWith('inc')){
            count++;
        }
        else{
            count--;
        }
        $(this).parent().children("span").text(count);
        update_total_price($(this).closest('tr'))
        $.ajax({
            url: `/shopcart/edit/?pr_id=${pr_id}&count=${count}`,
            success: function(answer){
                if (answer != 'OK'){
                    location.reload();
                }
            }
        });
    })
}

function update_total_price(tr_elem){
    var count = parseInt(tr_elem.children().eq(2).children("span").text());
    var price = parseFloat(tr_elem.children().eq(3).text());
    tr_elem.children().eq(4).text((price*count).toFixed(2));

    var prices = $('[id=total]');
    var sum = 0;
    for (i = 0; i < prices.length; i++){
        sum += parseFloat(prices[i].innerText)
    }
    $('#total-price').text(sum.toFixed(2));

    $.ajax({
        url: '/shopcart/update_header',
        success: function(data){
            $('.header').html(data.result);
        }
    });
}