// DELETE EVENT
$(document).ready(function() {
    $('#activity_table').on('click', '.delete-btn', function() {
        var activityId = $(this).data('id');
        Swal.fire({
            title: 'Are you sure?',
            text: 'You won\'t be able to undo this!',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, delete it!',
            cancelButtonText: 'Cancel'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: 'DELETE',
                    url: `/delete_activity/${activityId}`,
                    success: function(response) {
                        if (response.success) {
                            activity_table.ajax.reload(null, false);
                            Swal.fire({
                                icon: 'success',
                                title: 'Deleted!',
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
})