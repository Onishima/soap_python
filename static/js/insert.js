$(function () {
    //Validación de campos de Bootstrap
    $('#contact-form').validator();

    $('#contact-form').on('submit', function (e) {
        if (!e.isDefaultPrevented()) {
            var url = "php/contacto_validation.php";
            
            //Envío de la información del formulario con una petición Ajax
            $.ajax({
                type: "POST",
                url: url,
                data: $(this).serialize(),
                success: function (data)
                {
                    //Variable para determinar el tipo del cuadro de texto
                    var messageAlert = 'alert-' + data.type;
                    var messageText = data.message;

                    var alertBox = '<div class="alert ' + messageAlert + ' alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + messageText + '</div>';
                    if (messageAlert && messageText) {
                        $('#contact-form').find('#divMessage').html(alertBox);
                        //Resetear los campos del formulario
                        $('#contact-form')[0].reset();
                    }
                }
            });
            return false;
        }
    })
});
