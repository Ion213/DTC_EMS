var ongoing_attendance_table;

$(document).ready(function () {
    $('#ongoing-tab').addClass('active').attr('aria-selected', 'true');
    $('#ongoing').addClass('show active');
    var selected_event_Name = document.getElementById('ongoing_attendance_table').dataset.attendanceName;
    // Initialize DataTable
    ongoing_attendance_table = new DataTable('#ongoing_attendance_table', {
        responsive:true,
        stateSave: true,
        paging: true,
        scrollCollapse: true,
        scrollX: true,
        scrollY: '120vh',
        select: true,

        layout: {
            top1Start: 'pageLength',
            top1End: 'search',
            topStart: 'info',
            topEnd: 'paging',
            bottomStart: 'pageLength',
            bottomEnd: 'search',
            bottom2Start: 'info',
            bottom2End: 'paging', 

            top3Start: {
                buttons: [{
                    extend: 'collection',
                    text: 'Export',
                    buttons: [
                        {extend: 'copy',
                            title: selected_event_Name,
                            footer: false,
                            exportOptions: {columns: ':visible',rows: ':visible'},
                            },
                            
                        {extend: 'print',
                            title: selected_event_Name,
                            footer: false,
                            autoPrint: false,
                            exportOptions: {columns: ':visible',rows: ':visible'}
                            }, 

                        {extend: 'excel',
                            title: selected_event_Name,
                            footer: false,
                            exportOptions: {columns: ':visible',rows: ':visible'},
                            },   

                        {extend: 'csv',
                            title: selected_event_Name,
                            footer: false,
                            exportOptions: {columns: ':visible',rows: ':visible'},
                            },

                        {extend: 'pdf',
                            title: selected_event_Name,
                            footer: false,
                            orientation: 'protrait',
                            pageSize: 'LEGAL',
                            exportOptions: {columns: ':visible',rows: ':visible'},
                            },      
                ]},

                    {
                    extend: 'collection',
                    text: 'Export All Page',
                    buttons: [
                        {extend: 'copy',
                            title: selected_event_Name,
                            footer: false,
                            exportOptions: {
                                columns: ':visible',
                                modifier: {
                                    page: 'all',
                                    search: 'none'   
                                    },
                                },
                        },
                            
                        {extend: 'print',
                            title: selected_event_Name,
                            footer: false,
                            autoPrint: false,
                            exportOptions: {
                                columns: ':visible',
                                modifier: {
                                    page: 'all',
                                    search: 'none'   
                                    },
                                },
                            }, 

                        {extend: 'excel',
                            title: selected_event_Name,
                            footer: false,
                            exportOptions: {
                                columns: ':visible',
                                modifier: {
                                    page: 'all',
                                    search: 'none'   
                                    },
                                },
                            },   

                        {extend: 'csv',
                            title: selected_event_Name,
                            footer: false,
                            exportOptions: {
                                columns: ':visible',
                                modifier: {
                                    page: 'all',
                                    search: 'none'   
                                    },
                                },
                            },

                        {extend: 'pdf',
                            title: selected_event_Name,
                            footer: false,
                            orientation: 'protrait',
                            pageSize: 'LEGAL',
                            exportOptions: {
                                columns: ':visible',
                                modifier: {
                                    page: 'all',
                                    search: 'none'   
                                    },
                                },
                            },

                    ]},
                    'colvis'  // Column visibility button
                ]
            }
        }, 
        columnDefs: [
            {
                targets: -1,  // Hide the last column (Action buttons)
                visible: false
            }
        ],
        columnDefs: [
                    {
                        "targets": 4, // Target the first column (index 0)
                        "orderable": false // Disable ordering for this column
                    }
                ],

        // Dynamic AJAX request with selected activity ID
        ajax: function (data, callback, settings) {
            var activity = $('#activityComboBox').val(); // Get selected combo box value
            $.ajax({
                url: `/manage_attendance_get_data/${activity}`, // Pass selected ID to backend
                dataType: 'json',
                success: function (response) {
                    if (response && Array.isArray(response.data)) {
                        callback({ data: response.data }); // Ensure data is passed correctly
                    } else {
                        callback({ data: [] }); // In case of no data or invalid response
                    }
                },
                error: function (xhr, status, error) {
                    console.error("Error fetching data:", error);
                    callback({ data: [] }); // Empty data on error
                }
            });
        },

        columns: [
            { data: 'activity_name' },
            { data: 'student_name' },
            { data: 'departments' },
            { data: 'time_in' },
            { data: 'time_out' },
            {
                data: 'id',
                render: function (data, type, row) {
                    return `
                        <button class="delete-btn btn btn-danger btn-sm" 
                            data-id="${data}"
                             style="display:inline;">
                            <i class="fa-solid fa-user-minus"></i>
                        </button>
                    `;
                }
            }
        ]
    });

    // Event listener for combo box change
    $('#activityComboBox').on('change', function () {
        ongoing_attendance_table.ajax.reload(null, false); // Reload the table when the combo box value changes
    });

    // Listen for clicks on tabs to reload data
    $('#ongoing-tab').on('click', function(event) {
        ongoing_attendance_table.ajax.reload(null, false);
    });

    
});

