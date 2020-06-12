$(document).ready(function(){
    $('#best_deals_datatable').DataTable({
        "columnDefs": [
            {
                "render": function (data, type, row) {
                    return '<a href=' + row[1] + '>' + data + '</a>';
                },
                "targets": 0
            },
            {
                "render": function (data, type, row) {
                    return '<a href=' + row[7] + '>' + data + '</a>';
                },
                "targets": 8
            },
            { "visible": false,  "targets": [ 1, 7 ] },
        ],
        "pageLength": 10
    });
});