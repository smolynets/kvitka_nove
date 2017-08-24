
function to_basket() {
    $('button.to_basket').click(function(event){
        var flow = $(this).val();
        $.cookie(flow, flow, {'path': '/'});
        location.reload(true);
        return true;
     });
    }



function from_basket() {
    $('button.from_basket').click(function(event){
        var flow = $(this).val();
        $.removeCookie(flow, {'path': '/'});
        location.reload(true);
        return false;
     });
    }


    

function basket_form() {
    $('a.buy_ajax').click(function(event){
       var link = $(this);
       $.ajax({
       'url': link.attr('href'),
       'dataType': 'html',
       'type': 'get',
       'success': function(data, status, xhr){
          if (status != 'success') {
            alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
            return false;
        }
        var modal = $('#myModal'),
        html = $(data), form = html.find('#myform');
        modal.find('.modal-title').html(html.find('#basket_title').text());
        modal.find('.modal-body').html(form);
        modal.modal('show');
     }
    });
       return false;
       });
}





$(document).ready(function(){
    to_basket();
    from_basket();
    basket_form()
});