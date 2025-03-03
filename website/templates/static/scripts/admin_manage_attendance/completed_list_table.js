let completed_event_activity_attendance_table;

$(document).ready(function () {
 

    // Fetch completed events
    fetchCompletedEvents();

    function fetchCompletedEvents() {
        $.getJSON("/get_completed_events/", function (data) {
            let eventsList = $("#completed-events-list");
            eventsList.empty();

            if (data.length === 0) {
                eventsList.append('<li class="list-group-item">No completed events.</li>');
            } else {
                data.forEach(event => {
                    let eventItem = `<li class="list-group-item d-flex justify-content-between align-items-center">
                         <span>${event.event_name}: ${event.scheduled_date}</span>

                        <div class="d-flex">
                            <button class="btn btn-sm btn-primary me-2 toggle-activities" data-event-id="${event.id}">
                               <i class="fa-regular fa-eye"></i>
                            </button>
                        </div>
                    </li>

                    <ul class="list-group mt-2 event-activities d-none" id="activities-${event.id}">
                        <h7>Activities:</h7>
                        ${event.activities.map(activity => `
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <button class="btn btn-sm btn-light view-attendance" 
                                            data-activity-id="${activity.id}" 
                                            data-activity-event="${event.event_name}"
                                            data-activity-name="${activity.name}">${activity.name}: ${activity.start_time}-${activity.end_time}
                                        <i class="fa-solid fa-table"></i>
                                    </button>
                                <div class="d-flex gap-1">
                                    
                                    <button class="btn btn-sm btn-primary add-attendance" 
                                            data-activity-id="${activity.id}" 
                                            data-activity-event="${event.event_name}"
                                            data-activity-name="${activity.name}">
                                        <i class="fa-solid fa-plus"></i>
                                    </button>
                                </div>
                            </li>`).join('')}
                    </ul>`;

                    eventsList.append(eventItem);
                });
            }
        });
    }

    // Toggle activities for each event
    $(document).on("click", ".toggle-activities", function () {
        let eventId = $(this).data("event-id");
        let activitiesList = $(`#activities-${eventId}`);

        if (activitiesList.hasClass("d-none")) {
            activitiesList.removeClass("d-none");
            $(this).html('<i class="fa-regular fa-eye-slash"></i>').removeClass("btn-primary").addClass("btn-danger");
        } else {
            activitiesList.addClass("d-none");
            $(this).html('<i class="fa-regular fa-eye"></i>').removeClass("btn-danger").addClass("btn-primary");
        }
    });

    // Load attendance table when clicking "View Attendance"
    $(document).on("click", ".view-attendance", function () {
        let $this = $(this);
        let activityId = $this.data("activity-id");
        let eventName = $this.data("activity-event");
        let activityName = $this.data("activity-name");

        $(".view-attendance").removeClass("active");
        $this.addClass("active");

        $("#attendance_name").text(eventName + " - " + activityName);
        loadAttendance(activityId, eventName, activityName);
    });
    $(document).on("click", ".add-attendance", function () {
        let $this = $(this);
        let activityId = $this.data("activity-id");
        let eventName = $this.data("activity-event");
        let activityName = $this.data("activity-name");
    
        // Remove active class from all view-attendance buttons
        $(".view-attendance").removeClass("active");

        $(`.view-attendance[data-activity-id="${activityId}"]`).addClass("active");
    
        // Update attendance name text
        $("#attendance_name").text(eventName + " - " + activityName);
    
        // Load the attendance data
        loadAttendance(activityId, eventName, activityName);
    });

    function loadAttendance(activityId, eventName, activityName)  {
        if ($.fn.DataTable.isDataTable("#completed_event_activity_attendance_table")) {
            completed_event_activity_attendance_table.ajax.url(`/manage_attendance_get_data/${activityId}`).load();
            return;
        }

        completed_event_activity_attendance_table = $("#completed_event_activity_attendance_table").DataTable({
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
                            title: `${eventName}: ${activityName}`,
                            footer: false,
                            exportOptions: {columns: ':visible',rows: ':visible'},
                            },
                            
                        {extend: 'print',
                            title: `${eventName}: ${activityName}`,
                            footer: false,
                            autoPrint: false,
                            exportOptions: {columns: ':visible',rows: ':visible'}
                            }, 

                        {extend: 'excel',
                            title: `${eventName}: ${activityName}`,
                            footer: false,
                            exportOptions: {columns: ':visible',rows: ':visible'},
                            },   

                        {extend: 'csv',
                            title: `${eventName}: ${activityName}`,
                            footer: false,
                            exportOptions: {columns: ':visible',rows: ':visible'},
                            },

                        {extend: 'pdf',
                            title: `${eventName}: ${activityName}`,
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
                            title: `${eventName}: ${activityName}`,
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
                            title: `${eventName}: ${activityName}`,
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
                            title: `${eventName}: ${activityName}`,
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
                            title: `${eventName}: ${activityName}`,
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
                            title: `${eventName}: ${activityName}`,
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
            "ajax": {
                "url": "/manage_attendance_get_data/" + activityId,
                "type": "GET",
                "dataSrc": "data"
            },
            "columns": [
                {"data":"activity_name"},
                { "data": "student_name" },
                { "data": "departments" },
                { "data": "time_in" },
                { "data": "time_out" },
                { "data": "id",
                    render: function (data, type, row) {
                        return `
                            <button class="delete-btn btn btn-danger btn-sm" 
                                data-id="${data}"
                                style="display:inline;">
                                <i class="fa-solid fa-trash-can"></i>
                            </button>
                        `;
                    }
                }
            ],
        });
    }
})