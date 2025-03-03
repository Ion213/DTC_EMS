var upcoming_sched_table;

$(document).ready(function () {
        // Force the "Upcoming Events" tab to be active on page load
    $('#upcoming-tab').addClass('active').attr('aria-selected', 'true');
    $('#upcoming').addClass('show active');

    upcoming_sched_table = new DataTable('#upcoming_sched_table', {
        //table tools
        responsive:true,
        stateSave: true,
        paging: true,
        scrollCollapse: true,
        scrollX: true,
        scrollY: '50vh',
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
                            title: 'Upcoming Events',
                            footer: false,
                            exportOptions: {columns: ':visible',rows: ':visible'},
                            },
                            
                        {extend: 'print',
                            title: 'Upcoming Events',
                            footer: false,
                            autoPrint: false,
                            exportOptions: {columns: ':visible',rows: ':visible'}
                            }, 

                        {extend: 'excel',
                            title: 'Upcoming Events',
                            footer: false,
                            exportOptions: {columns: ':visible',rows: ':visible'},
                            },   

                        {extend: 'csv',
                            title: 'Upcoming Events',
                            footer: false,
                            exportOptions: {columns: ':visible',rows: ':visible'},
                            },

                        {extend: 'pdf',
                            title: 'Upcoming Events',
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
                            title: 'Upcoming Events',
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
                            title: 'Upcoming Events',
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
                            title: 'Upcoming Events',
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
                            title: 'Upcoming Events',
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
                            title: 'Upcoming Events',
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
                        "targets": [2,4], // Target the first column (index 0)
                        "orderable": false // Disable ordering for this column
                    }
                ],

        //table fetch data
        ajax: '/render_upcoming_events', 
        columns: [
            { data: 'event_name' },
            { data: 'scheduled_date'},
            
            { data: 'id', 
                    render: function(data, type, row) {
                        return `
                        <button class="view_activities-btn btn btn-light btn-sm" 
                            data-id="${data}"
                            data-event_name="${row.event_name}" 
                            style="display:inline;">
                            <i class="fa-regular fa-clock"></i> View Activities
                        </button>

                        `;
                    } 
            },
            { data: 'total_fines'},
            {
                data: 'id', // Maps to the key 'id' in the JSON
                render: function(data, type, row) {
                    return `
                        coming <i class="fa-solid fa-clock-rotate-left"></i>
                    `;
                }
            },   
        ]
    });
});

$(document).ready(function() {
    // Listen for clicks on tabs
    $('#upcoming-tab').on('click', function(event) {
        upcoming_sched_table.ajax.reload(null, false);
    });
});