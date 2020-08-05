$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();
    $('.results').hide();
    $('.reset').hide();
    $('#imageUpload').prop("disabled", false);
    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();
        
        var dir = "C:/Users/munta/OneDrive/Desktop/image-recognition-resnet50-flask/recommended";
        var fileextension = ".jpeg";
        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                // $('.results').show();
                $('.reset').show();
               
                $('.results').show();
                $('.img1').attr( "src", "static/"+data[0] )
                $('.img2').attr( "src", "static/"+data[1] )
                $('.img3').attr( "src", "static/"+data[2] )
                console.log(data)
            },
        });
    });

});

