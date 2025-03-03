//add,delete,update schedule
$(document).ready(function() {
    //add schedule
    $('#add_schedule_form').submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/add_schedule',
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Added!',
                        text: response.message,
                        timer: 3000,
                        timerProgressBar: true
                    });
                    upcoming_sched_table.ajax.reload(null, false);
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

});