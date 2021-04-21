function delete_user_from_group(delete_url){
    if(confirm('Are you sure you want to delete this user from group?')){
        var request = new XMLHttpRequest();
        request.open('DELETE', delete_url, true);

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
    else {

    }
}


function ajax_create_competition_page(type, url){
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