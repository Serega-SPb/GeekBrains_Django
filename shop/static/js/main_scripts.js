window.onload = function () {
    update_category_active('0');
    $('.cat-link').on( 'click', function(event) {
        target = event.target
        if (target.hasAttribute('id')) {
            var id = $(target).attr('id')
            $.ajax({
               url: `/catalog/ajax?cat_id=${id}`,
               success: function (data) {
                    $('.ctg-items').html(data.result);
               },
            });
            event.preventDefault();
            update_category_active(id);
       }
    });

    function update_category_active(id){
        $('.cat-link').each(function(){
            if (this.id == id){
                $(this).addClass('cat-active cat-bd-active')
            }
            else{
                $(this).removeClass('cat-active cat-bd-active')
            }
        })
    }
}