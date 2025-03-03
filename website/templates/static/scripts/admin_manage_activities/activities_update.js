$(document).ready(function() {
// UPDATE activity
        // Open the update modal
        $('#activity_table').on('click', '.update-btn', function() {
            var selected_activity_id = $(this).data('id');
            var activity_name = $(this).data('activity_name');
            var start_time= $(this).data('start_time');
            var end_time = $(this).data('end_time');
            var fines = $(this).data('fines');

            var formattedStartTime = start_time.replace(/(AM|PM)/i, '').trim();
            var formattedEndTime = end_time.replace(/(PM|AM)/i, '').trim();

            $('#selected_activity_idT').val(selected_activity_id);
            $('#update_activity_nameT').val(activity_name);
            $('#update_activity_startT').val(formattedStartTime);
            $('#update_activity_endT').val(formattedEndTime);
            $('#update_finesT').val(fines);

            $('#update_activity_modal').modal('show');
        });

        $('#update_activity_form').submit(function(e) {
            e.preventDefault();
            $.ajax({
                type: 'PUT',
                url: '/update_activities',
                data: $(this).serialize(),
                success: function(response) {
                    if (response.success) {
                        $('#update_activity_modal').modal('hide');
                        activity_table.ajax.reload(null, false);
                        Swal.fire({
                            icon: 'success',
                            title: 'Updated!',
                            text: response.message,
                            timer: 3000,
                            timerProgressBar: true
                        });
                    } else {
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