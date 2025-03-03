$(document).ready(function() {
    //upcomming table update
    //updateschedule modal
    // Open the update schedule modal
    $('#upcoming_sched_table').on('click', '.update_schedule-btn', function() {
        var schedule_id = $(this).data('id');
        var event_name = $(this).data('event_name');
        var scheduled_date = $(this).data('scheduled_date');

        var monthMap = {
            January: '01', February: '02', March: '03', April: '04', May: '05', June: '06',
                July: '07', August: '08', September: '09', October: '10', November: '11', December: '12'
            };
        var formattedDate = scheduled_date
            .replace(/-\w+$/, '') // Remove the weekday name
            .replace(/-\w+-/, (match) => `-${monthMap[match.slice(1, -1)]}-`);

        $('#update_selected_schedule_idT').val(schedule_id);
        $('#update_event_nameT').text(event_name); 
        $('#update_schedule_dateT').val(formattedDate);

        $('#update_schedule_modal').modal('show');
    });
    $('#update_schedule_form').submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: 'PUT',
            url: '/update_schedule',
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    $('#update_schedule_modal').modal('hide');
                    upcoming_sched_table.ajax.reload(null, false);
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

});



$(document).ready(function() {
    //ongoing table update
    //updateschedule modal
    // Open the update schedule modal
    $('#ongoing_sched_table').on('click', '.update_schedule-btn', function() {
        var schedule_id = $(this).data('id');
        var event_name = $(this).data('event_name');
        var scheduled_date = $(this).data('scheduled_date');

        var monthMap = {
            January: '01', February: '02', March: '03', April: '04', May: '05', June: '06',
                July: '07', August: '08', September: '09', October: '10', November: '11', December: '12'
            };
        var formattedDate = scheduled_date
            .replace(/-\w+$/, '') // Remove the weekday name
            .replace(/-\w+-/, (match) => `-${monthMap[match.slice(1, -1)]}-`);

        $('#update_selected_schedule_idT').val(schedule_id);
        $('#update_event_nameT').text(event_name); 
        $('#update_schedule_dateT').val(formattedDate);

        $('#update_schedule_modal').modal('show');
    });
    $('#update_schedule_form').submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: 'PUT',
            url: '/update_schedule',
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    $('#update_schedule_modal').modal('hide');
                    ongoing_sched_table.ajax.reload(null, false);
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

});