 //RENDER Activities DATA
 var activity_table
 $(document).ready(function() {
    //var selected_event_Id = "{{ selected_event.id }}";
    var selected_event_Id = document.getElementById('activity_table').dataset.eventId;
    var selected_event_Name = document.getElementById('activity_table').dataset.eventName;
    activity_table = new DataTable('#activity_table', {
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


    //table fetch data
        ajax: `/render_activities_data/${selected_event_Id}`,
        columns: [
            { data: 'activity_name' },
            { data: 'start_time' },
            { data: 'end_time' },
            { data: 'fines',
                render: function(data, type, row) {
                    return `
                        <p>&#8369;${data}</p>
                       
                    `;
                }

             },
            {data: 'id',
                render: function(data, type, row) {
                    return `
                        <button class="update-btn btn btn-warning btn-sm" 
                            data-id="${data}" 
                            data-activity_name="${row.activity_name}"
                            data-start_time="${row.start_time}"
                            data-end_time="${row.end_time}" 
                            data-fines="${row.fines}" 
                            style="display:inline;">
                            <i class="fa-solid fa-edit"></i>
                        </button>
                        <button class="delete-btn btn btn-danger btn-sm" 
                            data-id="${data}" 
                            style="display:inline;">
                            <i class="fa-solid fa-trash-can"></i>
                        </button>
                     `;
                }
            }
        ]
    });

});