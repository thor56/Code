$(document).ready(function() {
    $('#cust_list').on('change', function() {
        var cust_id = $(this).val();
        $.ajax({
            url: '/get_dynamic_data',
            data: {cust_id: cust_id},
            success: function(data) {
                // Update the page with the dynamic data
                $('#dynamic_data_container').html(data);
            }
        });
    });
});
