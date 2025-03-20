$(document).ready(function() {
    //adds a product to basket
    $('#add_to_basket').click(function(){
        var productIdVar;
        productIdVar = $(this).attr('data-productid');

        $.get('/shopsphere/basket/',
            {'product_id': productIdvar},
            function(data) {
                $('#basket_content').html(data);
            }
        )
    })

    //the purchase of the singluar product 
    $('#buy_now').click(function(){
        var productIdVar;
        productIdVar = $(this).attr('data-productid');

        $.get('/shopsphere/your_details/',
            {'product_id': productIdVar},
            function(data) {
                $('#product_purchased').html(data);
            }
        )
    })
});