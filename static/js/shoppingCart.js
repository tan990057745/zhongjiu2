$(function(){
	var total=0
    $('.cart_message1_contentUl').each(function () {
    		var price = $(this).find('.cart_message1_content_li2').attr('price')
			var number = $(this).find('.cart_message1_content_li3').attr('number')
			var sum = price * number
			total = sum + total
			$(this).find('#sumprice').html(sum)
    })

	$('.end #totalprice').html(total)
})