export function ready(fn) {
    if (document.readyState != 'loading'){
      fn();
    } else {
      document.addEventListener('DOMContentLoaded', fn);
    }
}

export function ajax_json_request(type, url, fillingElement, responseKey){
    var request = new XMLHttpRequest();
    request.open(type, url, true);

    request.onload = function() {
        if (this.status >= 200 && this.status < 400) {
            var resp = JSON.parse(this.response);
            fillingElement.innerHTML = resp[responseKey];
        }
    };

    request.onerror = function() {
        alert('Something went wrong!');
    };

    request.send();
}

export function ajax_json_fill_array(type, url, fillingArray, responseKey){
    var request = new XMLHttpRequest();
    request.open(type, url, true);


    request.onload = function() {
        if (this.status >= 200 && this.status < 400) {
            var resp = JSON.parse(this.response);
            resp[responseKey].forEach(element => {
                fillingArray.push(element);
            });
        }
    };

    request.onerror = function() {
        alert('Something went wrong!');
    };

    request.send();
}

export function getCookie(name) {

    var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
};