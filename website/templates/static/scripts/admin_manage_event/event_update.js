$(document).ready(function() {

    // UPDATE EVENT
        // Open the update modal
        $('#event_table').on('click', '.update-btn', function() {
            var eventId = $(this).data('id');
            var eventName = $(this).data('event');
            var eventDescription = $(this).data('description');
            $('#selected_event_id').val(eventId);
            $('#update_event').val(eventName);
            $('#update_event_description').val(eventDescription);
            $('#updateEventModal').modal('show');
        });
        $('#updateEventForm').submit(function(e) {
            e.preventDefault();
            $.ajax({
                type: 'PUT',
                url: '/update_event',
                data: $(this).serialize(),
                success: function(response) {
                    if (response.success) {
                        $('#updateEventModal').modal('hide');
                        table.ajax.reload(null, false);
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