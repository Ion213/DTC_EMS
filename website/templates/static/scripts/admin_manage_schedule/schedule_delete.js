
$(document).ready(function() {

        //UPCOMING TABLE DELETE
        // DELETE schedule
    $('#upcoming_sched_table').on('click', '.delete_schedule-btn', function() {
        var sched_id = $(this).data('id');
        Swal.fire({
            title: 'Are you sure to cancel this schedule?',
            text: 'You won\'t be able to undo this!',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, Cancel it!',
            cancelButtonText: 'Cancel'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: 'DELETE',
                    url: `/delete_schedule/${sched_id}`,
                    success: function(response) {
                        if (response.success) {
                            upcoming_sched_table.ajax.reload(null, false);
                            Swal.fire({
                                icon: 'success',
                                title: 'Canceled!',
                                text: response.message,
                                confirmButtonText: 'OK',
                                timer: 1500,
                                timerProgressBar: true
                            });
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
            }
        });
    });
    
});

$(document).ready(function() {

    //ongoing TABLE DELETE
    // DELETE schedule
$('#ongoing_sched_table').on('click', '.delete_schedule-btn', function() {
    var sched_id = $(this).data('id');
    Swal.fire({
        title: 'Event has already started, Are you sure to cancel this event?',
        text: 'You won\'t be able to undo this!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, cancel it!',
        cancelButtonText: 'Cancel'
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                type: 'DELETE',
                url: `/delete_schedule/${sched_id}`,
                success: function(response) {
                    if (response.success) {
                        ongoing_sched_table.ajax.reload(null, false);
                        Swal.fire({
                            icon: 'success',
                            title: 'Canceled!',
                            text: response.message,
                            confirmButtonText: 'OK',
                            timer: 1500,
                            timerProgressBar: true
                        });
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
        }
    });
});

});





$(document).ready(function() {

    //completed TABLE DELETE
    // DELETE schedule
$('#completed_sched_table').on('click', '.delete_schedule-btn', function() {
    var sched_id = $(this).data('id');
    Swal.fire({
        title: 'Are you sure to deleted this schedule?',
        text: 'You won\'t be able to undo this!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, Delete it!',
        cancelButtonText: 'Cancel'
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                type: 'DELETE',
                url: `/delete_schedule/${sched_id}`,
                success: function(response) {
                    if (response.success) {
                        completed_sched_table.ajax.reload(null, false);
                        Swal.fire({
                            icon: 'success',
                            title: 'Canceled!',
                            text: response.message,
                            confirmButtonText: 'OK',
                            timer: 1500,
                            timerProgressBar: true
                        });
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
        }
    });
});

});