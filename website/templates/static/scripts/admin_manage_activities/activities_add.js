$(document).ready(function() {

    // ADD Activty
    $('#add_activity_form').submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/add_activity',
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    activity_table.ajax.reload(null, false);
                    Swal.fire({
                        icon: 'success',
                        title: 'Success',
                        text: 'Activity added successfully!',
                        confirmButtonText: 'OK',
                        timer: 1500,
                        timerProgressBar: true
                    });
                    $('#add_activity_form')[0].reset();
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