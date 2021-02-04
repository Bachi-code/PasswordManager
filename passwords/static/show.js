const csrf = $('input[name="csrfmiddlewaretoken"]').val();

$('.show_password').on('click', function(){

    $.ajax({
        url: '/list/',
        type: 'post',
        data: {
            password_id: $(this).attr('id'),
            csrfmiddlewaretoken: csrf
        },
        cache : false,
        success: function(response){
            $(".modal-body").text("Your password is: " + response.password);
            $("#myModal").modal('show');
            },
        });
    });

$('.check_password').on('click', function(){

    $.ajax({
        url: '/list/',
        type: 'post',
        data: {
            password_id: $(this).attr('id'),
            csrfmiddlewaretoken: csrf,
            check_p: $(this).attr('data-check')
        },
        cache : false,
        success: function(response){
            if (response.password === 0)
            {
                $(".modal-body").text("Your password wasn't pwned");
                $("#myModal").modal('show');
            }
            else {
                $(".modal-body").text("Your password was pwned: " + response.password + " times.");
                $("#myModal").modal('show');
            }
            },
        });
    });

    $('#myModal').on('hidden.bs.modal', function () {
        $('.modal-body').html('');
    });
