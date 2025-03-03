var student_acount_table
$(document).ready(function () {

        $('#generate-btn').click(function () {
            $.ajax({
                url: '/generate_student_id',
                method: 'GET',
            success: function (data) {
                    $('#student_idT').val(data.random_id); // Set the generated ID in the input field
            },
            error: function () {
                    alert('Failed to generate student ID. Please try again.');
            }
        });
    });

    $('#update_student_account_modal').on('click', '#generate-btn', function() {
            $.ajax({
                url: '/generate_student_id',
                method: 'GET',
            success: function (data) {
                    $('#update_student_idT').val(data.random_id); // Set the generated ID in the input field
            },
            error: function () {
                    alert('Failed to generate Access ID. Please try again.');
            }
        });
    });


    student_acount_table = new DataTable('#student_table', {
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
                            title: 'STUDENTS ACCOUNT',
                            footer: false,
                            exportOptions: {columns: ':visible',rows: ':visible'},
                            },
                            
                        {extend: 'print',
                            title: 'STUDENTS ACCOUNT',
                            footer: false,
                            autoPrint: false,
                            exportOptions: {columns: ':visible',rows: ':visible'}
                            }, 

                        {extend: 'excel',
                            title: 'STUDENTS ACCOUNT',
                            footer: false,
                            exportOptions: {columns: ':visible',rows: ':visible'},
                            },   

                        {extend: 'csv',
                            title: 'STUDENTS ACCOUNT',
                            footer: false,
                            exportOptions: {columns: ':visible',rows: ':visible'},
                            },

                        {extend: 'pdf',
                            title: 'STUDENTS ACCOUNT',
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
                            title: 'STUDENTS ACCOUNT',
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
                            title: 'STUDENTS ACCOUNT',
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
                            title: 'STUDENTS ACCOUNT',
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
                            title: 'STUDENTS ACCOUNT',
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
                            title: 'STUDENTS ACCOUNT',
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
                        "targets": 8, // Target the first column (index 0)
                        "orderable": false // Disable ordering for this column
                    }
                ],

    //table fetch data
        ajax: `/render_student_account_data`,
        columns: [
            { data: 'student_ID' },
            { data: 'first_name' },
            { data: 'last_name' },
            { data: 'email' },
            { data: 'password'
                //render: function(data, type, row) {
                //        return data ? `
                //       ${data.substring(0, 6)}...
                 //      ` : 
                 //      'N/A';
                //  }
            },
            {data: 'dep_id',
                render: function(data, type, row) {
                    return `
                          <strong> 
                          ${row.department}/
                          ${row.year}/
                          ${row.section}
                          </strong>
                     `;
                }
            },
            { data: 'date_registered' },
            { data: 'date_updated' },
            {data: 'id',
                render: function(data, type, row) {
                    return `
                        <button class="update-btn btn btn-warning btn-sm" 
                            data-id="${data}"
                            data-student_id="${row.student_ID}"
                            data-first_name="${row.first_name}" 
                            data-last_name="${row.last_name}"
                            data-email="${row.email}"
                            data-password="${row.password}"
                            data-dep_id="${row.dep_id}" 
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