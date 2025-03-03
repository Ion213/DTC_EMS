$(document).ready(function(){

        // ADD STUDENT ACCOUNT
        $('#add_student_form').submit(function(e) {
            e.preventDefault();
            $.ajax({
                type: 'POST',
                url: '/add_student_account',
                data: $(this).serialize(),
                success: function(response) {
                    if (response.success) {
                        student_acount_table.ajax.reload(null, false);
                        Swal.fire({
                            icon: 'success',
                            title: 'Success',
                            text: 'Student account added successfully!',
                            confirmButtonText: 'OK',
                            timer: 1500,
                            timerProgressBar: true
                        });
                        $('#add_student_form')[0].reset();
                    } 
                    else {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: response.message,
                            confirmButtonText: 'OK',
                            timer: 1500,
                            timerProgressBar: true
                        });
                    }
                },
                error: function(xhr, status, error) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'An error occurred: ' + error,
                        confirmButtonText: 'OK',
                        timer: 1500,
                        timerProgressBar: true
                    });
                }
            });
        });
})