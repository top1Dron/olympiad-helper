import {ready, updateURLParameter } from '../services.js'

ready(function(){
    document.getElementById('id_difficulty').addEventListener('change', function(e){
        document.location.href = updateURLParameter(window.location.search, 'difficulty', document.getElementById('id_difficulty').value);
    });
    document.getElementById('id_classification').addEventListener('change', function(e){
        document.location.href = updateURLParameter(
            window.location.search, 
            'classification', 
            document.getElementById('id_classification').value);
    });
    document.getElementById('id_number').addEventListener('keydown', function(e){
        if (e.key == 'Enter'){
            document.location.href = updateURLParameter(
                window.location.search, 
                'number', 
                document.getElementById('id_number').value);
        }
    });
})
