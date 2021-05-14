import {ready, ajax_json_request} from '../services.js'


ready(function(){
    var active_tab = document.querySelector('input[type=radio][name=tabs]:checked');
    ajax_json_request('GET', active_tab.getAttribute('data'), document.getElementById('tab-data'), "tab-data");

    var elems = document.querySelectorAll('input[type=radio][name=tabs]');
    elems.forEach(
        function(elem){
            elem.addEventListener('click', function(event){
                var elems_copy = Array.from(elems);
                elems_copy.forEach(el => el.removeAttribute('checked'));
                elem.setAttribute('checked', 'true');
                ajax_json_request('GET', elem.getAttribute('data'), document.getElementById('tab-data'), "tab-data");
            }, true);
        }
    );
})