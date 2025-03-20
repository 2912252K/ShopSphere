/* 
$(document).ready(function() {
    //while searching for products it will provide suggestions
    $('#search-input').keyup(function() {
        var query;
        query = $(this).val();

        $.get('/shopsphere/suggest/',
            {'suggest': query},
            function(data) {
                $('#product-listing').html(data);
            })
    });
}); 
*/
