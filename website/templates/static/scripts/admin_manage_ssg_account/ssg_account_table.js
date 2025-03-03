var ssg_acount_table
$(document).ready(function () {

    ssg_acount_table = new DataTable('#ssg_table', {
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
                            title: 'SSG ACCOUNT',
                            footer: false,
                            exportOptions: {columns: ':visible',rows: ':visible'},
                            },
                            
                        {extend: 'print',
                            title: 'SSG ACCOUNT',
                            footer: false,
                            autoPrint: false,
                            exportOptions: {columns: ':visible',rows: ':visible'}
                            }, 

                        {extend: 'excel',
                            title: 'SSG ACCOUNT',
                            footer: false,
                            exportOptions: {columns: ':visible',rows: ':visible'},
                            },   

                        {extend: 'csv',
                            title: 'SSG ACCOUNT',
                            footer: false,
                            exportOptions: {columns: ':visible',rows: ':visible'},
                            },

                        {extend: 'pdf',
                            title: 'SSG ACCOUNT',
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
                            title: 'SSG ACCOUNT',
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
                            title: 'SSG ACCOUNT',
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
                            title: 'SSG ACCOUNT',
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
                            title: 'SSG ACCOUNT',
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
                            title: 'SSG ACCOUNT',
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
        ajax: `/render_ssg_account_data`,
        columns: [
            { data: 'email' },
            { data: 'password',
                //render: function(data, type, row) {
                //        return data ? `
                //        ${data.substring(0, 20)}...
                //       ` : 
                //       'N/A';
                //  }
            },
            { data: 'date_registered' },
            { data: 'date_updated' },
            {data: 'id',
                render: function(data, type, row) {
                    return `
                        <button class="update-btn btn btn-warning btn-sm" 
                            data-id="${data}"
                            data-email="${row.email}"
                            data-password="${row.password}"
                            style="display:inline;">
                            <i class="fa-solid fa-edit"></i>
                        </button>
                        <button class="delete-btn btn btn-danger btn-sm" 
                            data-id="${data}" style="display:inline;">
                            <i class="fa-solid fa-trash-can"></i>
                        </button>
                    `;
                }
            }, 
        ]
    });

});