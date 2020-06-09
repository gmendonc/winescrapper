$(document).ready(function(){
    $('#best_deals_dat').DataTable({
        "columnDefs": [
            {
                "render": function (data, type, row) {
                    return '<a href=' + row[1] + '>' + data + '</a>';
                },
                "targets": 0
            },
            {
                "render": function (data, type, row) {
                    return '<a href=' + row[5] + '>' + data + '</a>';
                },
                "targets": 6
            },
            { "visible": false,  "targets": [ 1, 5 ] },
        ],
        "pageLength": 10
    });
});