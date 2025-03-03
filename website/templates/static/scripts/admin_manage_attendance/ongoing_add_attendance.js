const successSound = new Audio('/static/sounds/success.mp3'); // Change path as needed
const failSound = new Audio('/static/sounds/invalid.mp3'); // Change path as needed

function playSound(sound) {
    sound.pause();  // Stop the current playback
    sound.currentTime = 0;  // Reset the audio to the beginning
    sound.play();  // Play the sound
}
//add IN
$(document).ready(function() {
    // ADD attendees


    $('#user-list').on('click', '.add-btn-in', function(e) {
        e.preventDefault();  // Prevent the default action

        var activity_Id = $("#activityComboBox").val();  // Get selected activity ID
        var user_Id = $(this).data('id');
        var name = $(this).data('name');

        if (!activity_Id) { // Corrected syntax
            failSound.play()
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'No Ongoing Event and Activity',
                confirmButtonText: 'OK',
                timer: 1500,
                timerProgressBar: true
            });
            return;  // Exit function if no activity is selected
        }

        $.ajax({
            type: 'POST',
            url: `/add_attendees_in/${activity_Id}/${user_Id}`, 
            success: function(response) {
                if (response.success) {
                    if (typeof ongoing_attendance_table !== "undefined") {
                        ongoing_attendance_table.ajax.reload(null, false);  // Reload table if defined
                    }
                    playSound(successSound);

                    Swal.fire({
                        icon: 'success',
                        title: '',
                        text: response.message,
                        confirmButtonText: 'OK',
                        timer: 1500,
                        timerProgressBar: true
                    });
                } else {
                    playSound(failSound)
                    Swal.fire({
                        icon: 'warning',
                        title: '',
                        text: response.message,
                        confirmButtonText: 'OK',
                        timer: 1500,
                        timerProgressBar: true
                    });
                }
            },
            error: function(xhr, status, error) {
                playSound(failSound)
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


//add OUT
$(document).ready(function() {
    // ADD attendees
    $('#user-list').on('click', '.add-btn-out', function(e) {
        e.preventDefault();  // Prevent the default action

        var activity_Id = $("#activityComboBox").val();  // Get selected activity ID
        var user_Id = $(this).data('id');
        var name = $(this).data('name');

        if (!activity_Id) { // Corrected syntax
            playSound(failSound)
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'No Ongoing Event and Activity',
                confirmButtonText: 'OK',
                timer: 1500,
                timerProgressBar: true
            });
            return;  // Exit function if no activity is selected
        }

        $.ajax({
            type: 'POST',
            url: `/add_attendees_out/${activity_Id}/${user_Id}`, 
            success: function(response) {
                if (response.success) {
                    if (typeof ongoing_attendance_table !== "undefined") {
                        ongoing_attendance_table.ajax.reload(null, false);  // Reload table if defined
                    }
                    playSound(successSound);
                    Swal.fire({
                        icon: 'success',
                        title: '',
                        text: response.message,
                        confirmButtonText: 'OK',
                        timer: 1500,
                        timerProgressBar: true
                    });
                } else {
                    playSound(failSound)
                    Swal.fire({
                        icon: 'warning',
                        title: '',
                        text: response.message,
                        confirmButtonText: 'OK',
                        timer: 1500,
                        timerProgressBar: true
                    });
                }
            },
            error: function(xhr, status, error) {
                playSound(failSound)
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
