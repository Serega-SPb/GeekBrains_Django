window.onload = function () {
    $('[id^=activation]').on('click', function(e){
        var s_id = $(this).closest('tr').attr('id');
        var ns = $(this).closest('table').attr('id');

        apply_activation($(this))

        $.ajax({
            url: `/admin_custom/activation?ns=${ns}&id=${s_id}`,
        })
    });
}

function apply_activation(sender){

    sender.closest('tr').children('.td-name').toggleClass('disable')

    var action = sender.text().trim();
    if (action.toLowerCase() == 'enabled')
    {
        sender.text('Disabled')
    }
    else
    {
        sender.text('Enabled')
    }
}