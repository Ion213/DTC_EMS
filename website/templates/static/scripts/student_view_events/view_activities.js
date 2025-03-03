var activity_table
$(document).ready(function() {
//upcoming show activities
    $('#upcoming_sched_table').on('click', '.view_activities-btn', function () {
        var schedule_id = $(this).data('id');
        var event_name = $(this).data('event_name');  // Get event ID
        $('#event_name_act').text(event_name);
        // Show the modal
        $('#show_activities_modal').modal('show');

        // Load activities for this event using AJAX
        loadActivities(schedule_id);
            // Function to load activities in the modal
        function loadActivities(schedule_id) {
            activity_table = new DataTable('#activity_table', {
                ajax: '/render_activities/' + schedule_id, // Fetch activities for the event
                destroy: true,  // Destroy previous instance if already created
                columns: [
                    { data: 'activity_name' },
                    { data: 'start_time'},
                    { data: 'end_time'}, 
                    { data: 'fines',
                        render: function(data, type, row) {
                            return `
                               
                                <p>&#8369;${data}</p>
                               
                            `;
                        }
                     },

                ]
            });
        }
    });
});

$(document).ready(function() {
    //onggoing show activities
        $('#ongoing_sched_table').on('click', '.view_activities-btn', function () {
            var schedule_id = $(this).data('id');
            var event_name = $(this).data('event_name');
            $('#event_name_act').text(event_name);
            // Show the modal
            $('#show_activities_modal').modal('show');
    
            // Load activities for this event using AJAX
            loadActivities(schedule_id);
                // Function to load activities in the modal
            function loadActivities(schedule_id) {
                activity_table = new DataTable('#activity_table', {
                    ajax: '/render_activities/' + schedule_id, // Fetch activities for the event
                    destroy: true,  // Destroy previous instance if already created
                    columns: [
                        { data: 'activity_name' },
                        { data: 'start_time'},
                        { data: 'end_time'}, 
                        { data: 'fines',
                            render: function(data, type, row) {
                                return `
                                   
                                    <p>&#8369;${data}</p>
                                   
                                `;
                            }
                         },
    
                    ]
                });
            }
        });
});

$(document).ready(function() {
    //completed show activities
        $('#completed_sched_table').on('click', '.view_activities-btn', function () {
            var schedule_id = $(this).data('id');
            var event_name = $(this).data('event_name');
            $('#event_name_act').text(event_name);
            // Show the modal
            $('#show_activities_modal').modal('show');
    
            // Load activities for this event using AJAX
            loadActivities(schedule_id);
                // Function to load activities in the modal
            function loadActivities(schedule_id) {
                activity_table = new DataTable('#activity_table', {
                    ajax: '/render_activities/' + schedule_id, // Fetch activities for the event
                    destroy: true,  // Destroy previous instance if already created
                    columns: [
                        { data: 'activity_name' },
                        { data: 'start_time'},
                        { data: 'end_time'}, 
                        { data: 'fines',
                            render: function(data, type, row) {
                                return `
                                   
                                    <p>&#8369;${data}</p>
                                   
                                `;
                            }
                         },
    
                    ]
                });
            }
        });
});