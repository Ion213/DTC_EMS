var table;
    //RENDER EVENT DATA
$(document).ready(function() {
    table = new DataTable('#event_table', {

        //table tools
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
                            title: 'EVENTS',
                            footer: false,
                            exportOptions: {columns: ':visible',rows: ':visible'},
                            },
                            
                        {extend: 'print',
                            title: 'EVENTS',
                            footer: false,
                            autoPrint: false,
                            exportOptions: {columns: ':visible',rows: ':visible'}
                            }, 

                        {extend: 'excel',
                            title: 'EVENTS',
                            footer: false,
                            exportOptions: {columns: ':visible',rows: ':visible'},
                            },   

                        {extend: 'csv',
                            title: 'EVENTS',
                            footer: false,
                            exportOptions: {columns: ':visible',rows: ':visible'},
                            },

                        {extend: 'pdf',
                            title: 'EVENTS',
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
                            title: 'EVENTS',
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
                            title: 'EVENTS',
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
                            title: 'EVENTS',
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
                            title: 'EVENTS',
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
                            title: 'EVENTS',
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
                        "targets": 5, // Target the first column (index 0)
                        "orderable": false // Disable ordering for this column
                    }
                ],



    //table fetch data
        ajax: '/render_event_data',
        columns: [
            { data: 'event' },
            { data: 'event_description' },
            {data: 'id',
                render: function(data, type, row) {
                    var activityRenderUrl = "/manage_activities_render_template/" + data;
                    return `
                        <a href="${activityRenderUrl}" class="btn btn-light btn-sm">
                           <i class="fa-solid fa-edit"></i>
                        </a>
                        <p style="display:inline;">${row.activity_count}</p> |
                        <p style="display:inline;">&#8369;${row.total_fines}</p>
                    `;
                }
            },
            { data: 'date_created' },
            { data: 'date_updated' },
            {data: 'id',
                render: function(data, type, row) {
                    return `
                        <button class="update-btn btn btn-warning btn-sm" 
                            data-id="${data}" 
                            data-event="${row.event}" 
                            data-description="${row.event_description}" style="display:inline;">
                            <i class="fa-solid fa-edit"></i>
                        </button>
                        <button class="delete-btn btn btn-danger btn-sm" 
                            data-id="${data}" style="display:inline;">
                            <i class="fa-solid fa-trash-can"></i>
                        </button>
                    `;
                }
            },   
        ],
        
    });   

});