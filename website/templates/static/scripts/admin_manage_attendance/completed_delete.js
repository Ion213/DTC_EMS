$(document).ready(function() {
    // DELETE Attendance Record
    $('#completed_event_activity_attendance_table').on('click', '.delete-btn', function() {
        var attendanceId = $(this).data('id');

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
                    url: `/delete_attendees_ended/${attendanceId}`,
                    success: function(response) {
                        if (response.success) {
                            $("#completed_event_activity_attendance_table").DataTable().ajax.reload(null, false);
                            Swal.fire({
                                icon: 'success',
                                title: 'Deleted!',
                                text: response.message,
                                confirmButtonText: 'OK',
                                timer: 1500,
                                timerProgressBar: true
                            });
                        } else {
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
                    error: function() {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: 'An error occurred while deleting the record.',
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
