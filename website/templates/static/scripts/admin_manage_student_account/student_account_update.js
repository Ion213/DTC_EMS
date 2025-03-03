$(document).ready(function(){
        // UPDATE student aacount
        // Open the update modal
        $('#student_table').on('click', '.update-btn', function() {
            
            var selected_student_id = $(this).data('id');
            var student_id = $(this).data('student_id');
            var first_name = $(this).data('first_name');
            var last_name = $(this).data('last_name');
            var email = $(this).data('email');
            var password = $(this).data('password');
            var dep_id = $(this).data('dep_id');

            $('#selected_student_account_idT').val(selected_student_id);
            $('#update_student_idT').val(student_id);
            $('#update_first_nameT').val(first_name);
            $('#update_last_nameT').val(last_name);
            $('#update_emailT').val(email);
            $('#update_passwordT').val(password);
            $('#update_departmentT').val(dep_id);

            $('#update_student_account_modal').modal('show');
        });
        $('#update_student_account_form').submit(function(e) {
            e.preventDefault();
            $.ajax({
                type: 'PUT',
                url: '/update_student_account',
                data: $(this).serialize(),
                success: function(response) {
                    if (response.success) {
                        $('#update_student_account_modal').modal('hide');
                        student_acount_table.ajax.reload(null, false);
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