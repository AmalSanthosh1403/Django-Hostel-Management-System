// $(document).ready(function(){
//     $('.selectedDate').click(function(){
//         // alert('hello world')
//         const dateId = $(this).data('date-id')
//         $('#meals_details').toggle(200)
//     })

   


// })


$(document).ready(function(){
    $('.selectedDate').click(function(){
        // Get the unique id for the clicked row
        const dateId = $(this).data('date-id');
        
        // Toggle the corresponding meal details row
        $('#meals_details_' + dateId).toggle(200);
    });
});
