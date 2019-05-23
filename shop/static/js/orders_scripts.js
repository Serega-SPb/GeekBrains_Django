//var totalQuantityElem, totalCostElem, $forms

window.onload = function () {
    var totalQuantityElem = $('#total_quantity');
    var totalCostElem = $('#total_cost');
    var $forms = $('.formset').filter(function()
        {return $(this).find('#price').text() != ''});

    $('[id$=quantity]').on('change', function(e){
        var target = e.target;
        if (target.value <= 0)
        {
            tr = $(target).closest('tr')
            tr.remove();
        }
        updateSummary();
    })

    $('.formset').formset({
        addText: '+',
        deleteText: 'X',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });

    $('.add-row').on('click', function(e)
    {
       $('#order_form select').last().change(productSelectionChanged);
       count = $('[id$=quantity]').last();
       count.val(0);
       count.on('change', function(e){updateForms();});
    });

    $('#order_form select').change(productSelectionChanged);

    function productSelectionChanged(event)
    {
       var target = event.target;
       id = $(target).find('option:selected').val();
       if (id){
            $.ajax({
                url: `/catalog/get_product_price?id=${id}`,
                success: function(answer){
                    td = $(target).closest('tr').children('td')[2];
                    $(td).html('<span id="price" class="order-price">'+ answer['price'] +'</span>');
                    updateForms();
                }
            });
       }

       count = $($(target).closest('tr').children('td')[1]).children('input');
       if (count.val() == 0)
       {
            count.val(1);
       }

    }

    function updateForms()
    {
        $forms = $('.formset').filter(function(){
            return $(this).find('#price').text() != '';});
        updateSummary();
    }

    function updateSummary()
    {
        var tempQuantity = 0, tempCost = 0;
        $forms.each(function(i, f){
            q = parseInt($(f).find('[id$=quantity]').val());
            p = parseFloat($(f).find('#price').text());

            tempQuantity += q;
            tempCost += p*q
        });
        totalQuantityElem.text(tempQuantity);
        totalCostElem.text(tempCost.toFixed(2));
    }

    function deleteOrderItem(row)
    {
        $forms = $($forms).not(row);
        row.remove();
        updateSummary();
    }
};

