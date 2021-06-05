$('#id_avatar').change(function(event){
    if(typeof event.target.files[0] !== 'undefined'){
        $('#avatar').attr("src", URL.createObjectURL(event.target.files[0]));
    }
    else {
        URL.revokeObjectURL($('#avatar').attr("src"));
        $('#avatar').attr("src", "/static/img/default-image.jpg")
    }
});