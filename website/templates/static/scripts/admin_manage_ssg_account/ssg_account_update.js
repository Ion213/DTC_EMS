$(document).ready(function(){
    // UPDATE student aacount
    // Open the update modal
    $('#ssg_table').on('click', '.update-btn', function() {
        
        var selected_ssg_id = $(this).data('id');
        var email= $(this).data('email');
        var password = $(this).data('password');


        $('#selected_ssg_account_idT').val(selected_ssg_id);
        $('#update_emailT').val(email);
        $('#update_passwordT').val(password);


        $('#update_ssg_account_modal').modal('show');
    });
    $('#update_ssg_account_form').submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: 'PUT',
            url: '/update_ssg_account',
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    $('#update_ssg_account_modal').modal('hide');
                    ssg_acount_table.ajax.reload(null, false);
                    Swal.fire({
                        icon: 'success',
                        title: 'Updated!',
                        text: response.message,
                        timer: 3000,
                        timerProgressBar: true
                    });
                } 
                else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: response.message,
                        timer: 3000,
                        timerProgressBar: true
                    });
                }
            },
            error: function(xhr, status, error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'An error occurred: ' + error,
                    timer: 3000,
                    timerProgressBar: true
                });
            }
        });
    });
})