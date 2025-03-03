$(document).ready(function() {

    // UPDATE activity
        // Open the update modal
        $('#fees_table').on('click', '.update-btn', function() {
            var selected_fees_id = $(this).data('id');
            var fees_name = $(this).data('fees_name');
            var fees_amount = $(this).data('fees_amount');

            console.log('Selected Fees ID:', selected_fees_id);
            console.log('Fees Name:', fees_name);
            console.log('Fees Amount:', fees_amount);

            $('#selected_fees_idT').val(selected_fees_id);
            $('#update_fees_nameT').val(fees_name);
            $('#update_fees_amountT').val(fees_amount);

            $('#update_fees_modal').modal('show');
        });

        $('#update_fees_form').submit(function(e) {
            e.preventDefault();
            $.ajax({
                type: 'PUT',
                url: '/update_fee',
                data: $(this).serialize(),
                success: function(response) {
                    if (response.success) {
                        $('#update_fees_modal').modal('hide');
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