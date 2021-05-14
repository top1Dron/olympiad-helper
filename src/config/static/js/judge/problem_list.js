import {ready, updateURLParameter } from '../services.js'

ready(function(){
    document.getElementById('id_difficulty').addEventListener('change', function(e){
        // filtered_problems_display_on_select(document.getElementById('id_difficulty'));
        document.location.href = updateURLParameter(window.location.search, 'difficulty', document.getElementById('id_difficulty').value);
    });
    document.getElementById('id_classification').addEventListener('change', function(e){
        document.location.href = updateURLParameter(
            window.location.search, 
            'classification', 
            document.getElementById('id_classification').value);
        // filtered_problems_display_on_select(document.getElementById('id_classification'));
    });
    document.getElementById('id_number').addEventListener('keydown', function(e){
        if (e.key == 'Enter'){
            // var url = '?' + document.getElementById('id_number').getAttribute('name') + '=' + document.getElementById('id_number').value;
            // document.location.href = url;
            document.location.href = updateURLParameter(
                window.location.search, 
                'number', 
                document.getElementById('id_number').value);
        }
    });
    
    function filtered_problems_display_on_select(filter){
        var current_filter_params = window.location.search.toString();
        var url = '?' + filter.getAttribute('name') + '=' + filter.value;
        
        // if selected filter is already in url
        if (current_filter_params.includes(filter.getAttribute('name'))){

            // getting start position of new selection in current url param and length of url param name
            var indexOfNewUrlParam = current_filter_params.indexOf(filter.getAttribute('name'));
            var lenOfNewUrlParam = filter.getAttribute('name').length;

            // getting lenhth of current url param with value and replace it on new selected value
            var oldUrlParamLength = indexOfNewUrlParam + lenOfNewUrlParam;

            // getting chars after = 
            var checkStr = current_filter_params[oldUrlParamLength+1] + current_filter_params[oldUrlParamLength+2];
            checkStr = checkStr.toString()

            // if not exists (at the end of url params without selected value)
            if (checkStr == 'NaN'){
                oldUrlParamLength += 1;
            }

            // check on selected value at the middle
            else if (checkStr == checkStr.toUpperCase()){
                oldUrlParamLength += 3;
            }

            // if value in the middle and not selected (sample: ?classification=&diffic...)
            else{
                oldUrlParamLength += 1;
            }
            var oldUrlParam = current_filter_params.substring(indexOfNewUrlParam, oldUrlParamLength);
            url = current_filter_params.replace(oldUrlParam, filter.getAttribute('name') + '=' + filter.value);
        }
        else{
            url += current_filter_params.replace('?', '&');
        }
        document.location.href = url;
    }
})
