$(document).ready(function () {
    $('#user-search').on('input', function () {
        const input = $(this).val().trim();

        // Clear results if input is empty
        if (input === '') {
            $('#user-list').empty().append('<li class="list-group-item text-muted">Please enter a name of user to add.</li>');
            return;
        }

        // Send AJAX request
        $.ajax({
            url: '/add_filter_users',
            type: 'GET',
            data: { input: input },
            success: function (response) {
                const userList = $('#user-list');
                userList.empty();

                if (response.user && response.user.length) {
                    response.user.forEach(user => {
                        userList.append(`
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                ${user.first_name} ${user.last_name} ${user.department}
                                <button class="add-btn-in btn btn-success btn-sm" 
                                    data-id="${user.id}"
                                    data-name="${user.first_name} ${user.last_name}" 
                                    style="display:inline;">
                                    <i class="fa-solid fa-square-plus"></i>IN
                                </button>
                                <button class="add-btn-out btn btn-warning btn-sm" 
                                    data-id="${user.id}"
                                    data-name="${user.first_name} ${user.last_name}" 
                                    style="display:inline;">
                                    <i class="fa-regular fa-square-plus"></i>OUT
                                </button>
                            </li>

                        `);
                    });
                } else {
                    userList.append('<li class="list-group-item text-muted">No users found.</li>');
                }
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'An error occurred while fetching users. Please try again later.',
                    confirmButtonText: 'OK'
                });
            }
        });
    });
});
