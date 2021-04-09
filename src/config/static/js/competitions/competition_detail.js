function ready(fn) {
    if (document.readyState != 'loading'){
      fn();
    } else {
      document.addEventListener('DOMContentLoaded', fn);
    }
}

function ajax_tab_selection(type, url){
    var request = new XMLHttpRequest();
    request.open(type, url, true);

    request.onload = function() {
        if (this.status >= 200 && this.status < 400) {
            var resp = JSON.parse(this.response);
            document.getElementById('tab-data').innerHTML = resp['tab-data'];
        }
    };

    request.onerror = function() {
        alert('Something went wrong!');
    };

    request.send();
}

ready(function(){
    var active_tab = document.querySelector('a.tabs-tab-active');
    ajax_tab_selection('GET', active_tab.getAttribute('data'));

    var elems = document.querySelectorAll('a.tabs-tab');
    elems.forEach(
        function(elem){
            elem.addEventListener('click', function(event){
                elems_copy = Array.from(elems);
                elems_copy.forEach(el => el.classList.remove('tabs-tab-active'));
                elem.classList.add('tabs-tab-active');
                ajax_tab_selection('GET', elem.getAttribute('data'));
            }, true);
        }
    );

    // document.getElementById('create-group-competition').addEventListener('click', function(event){
    //     ajax_tab_selection('GET', elem.getAttribute('data'));
    // }, true)
})