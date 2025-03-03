$(document).ready(function () {
    $('#c_user-search').on('input', function () {
        const input = $(this).val().trim();
        const userList = $('#c_user-list');

        // Clear results if input is empty
        if (input === '') {
            userList.empty().append('<li class="list-group-item text-muted">Please enter a name of user to add.</li>');
            return;
        }

        // Send AJAX request
        $.ajax({
            url: '/add_filter_users',
            type: 'GET',
            data: { input: input },
            success: function (response) {
                userList.empty();

                if (response.user && response.user.length) {
                    response.user.forEach(user => {
                        if (!$(`#user-${user.id}`).length) { // Prevent duplicates
                            userList.append(`
                                <li id="user-${user.id}" class="list-group-item d-flex justify-content-between align-items-center">
                                    <span>${user.first_name} ${user.last_name} - ${user.department}</span>
                                    <button class="add-btn btn btn-primary btn-sm" 
                                        data-id="${user.id}"
                                        data-name="${user.first_name} ${user.last_name}">
                                        <i class="fa-solid fa-plus"></i> Add Student
                                    </button>
                                </li>
                            `);
                        }
                    });
                } else {
                    userList.append('<li class="list-group-item text-muted">No users found.</li>');
                }
            },
            error: function (xhr, status, error) {
                console.error('AJAX Error:', status, error);
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'An error occurred while fetching users. Please try again later.',
                    confirmButtonText: 'OK'
                });
            }
        });
    });

    let activityID;

    // Open the add attendance modal
    $(document).on('click', '.add-attendance', function () {
        activityID = $(this).data('activity-id');
        activity_name=$(this).data('activity-name')
        console.log(activity_name)

        $('#activity_title').text(`${activity_name}:`)
        $('#add_attendees_completed_activity').modal('show');
    });

    // Handle adding attendance
    $('#c_user-list').on('click', '.add-btn', function (e) {
        e.preventDefault();
        const user_Id = $(this).data('id');

        if (!activityID) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'No Ongoing Event and Activity',
                confirmButtonText: 'OK',
                timer: 1500,
                timerProgressBar: true
            });
            return;
        }

        $.ajax({
            type: 'POST',
            url: `/add_attendees_in_out/${activityID}/${user_Id}`,
            success: function (response) {
                if (response.success) {
                    completed_event_activity_attendance_table.ajax.reload(null, false);
                    $('#add_attendees_completed_activity').modal('hide');
                    $('#c_add_form')[0].reset();

                    Swal.fire({
                        icon: 'success',
                        title: 'Success',
                        text: response.message,
                        confirmButtonText: 'OK',
                        timer: 1500,
                        timerProgressBar: true
                    });

                    $(`#user-${user_Id}`).remove(); // Remove user from list after adding
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Already Attended',
                        text: response.message,
                        confirmButtonText: 'OK',
                        timer: 1500,
                        timerProgressBar: true
                    });
                }
            },
            error: function (xhr, status, error) {
                console.error('AJAX Error:', status, error);
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
});
