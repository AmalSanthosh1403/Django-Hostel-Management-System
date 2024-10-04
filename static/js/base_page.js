$(document).ready(function(){
    // hostel
    $('#room').mouseover(function(){
        // alert('hello world')
        $('#dropdwonContent').show()
    })

    $('#room').mouseout(function(){
        $('#dropdwonContent').hide()
    })

    $('#dropdwonContent').mouseover(function(){
        $('#dropdwonContent').show()
    })
    $('#dropdwonContent').mouseout(function(){
        $('#dropdwonContent').hide()
    });


    
    $('#ManageMess').mouseover(function(){
        $('#addMessDropdown').show()
    })

    $('#ManageMess').mouseout(function(){
        $('#addMessDropdown').hide()
    })

    $('#addMessDropdown').mouseover(function(){
        $('#addMessDropdown').show()
    })

    $('#addMessDropdown').mouseout(function(){
        // alert('hello world')
        $('#addMessDropdown').hide()
    })


})

