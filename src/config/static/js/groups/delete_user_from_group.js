function delete_user_from_group(delete_url){
    if(confirm('Are you sure you want to delete this user from group?')){
        var request = new XMLHttpRequest();
        request.open('DELETE', delete_url, true);

        request.onload = function() {
            if (this.status >= 200 && this.status < 400) {
                var resp = JSON.parse(this.response);
                alert(resp['message']);
                location.reload();
            }
        };

        request.onerror = function() {
            alert('Something went wrong!');
        };
        data = {
            'csrfmiddlewaretoken': getCookie('csrftoken'),
        };
        request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        request.send();
    }
    else {

    }
}

function change_user_role_in_group(change_role_url, member_id){
    var request = new XMLHttpRequest();
    request.open('POST', change_role_url, true);
    request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

    var data = {
        csrfmiddlewaretoken: getCookie('csrftoken'),
        'member_id': document.getElementById('id_role' + member_id.toString()).getAttribute('member_id'),
        'member_role': document.getElementById('id_role' + member_id.toString()).value,
    };

    request.onload = function() {
        if (this.status >= 200 && this.status < 400) {
            location.reload();
        }
    };

    request.onerror = function() {
        alert('Something went wrong!');
    };

    request.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    data = JSON.stringify(data);
    request.send(data);
}

function getCookie(name) {

    var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
};

function ajax_create_competition_page(type, url){
    var request = new XMLHttpRequest();
    request.open(type, url, true);

    request.onload = function() {
        if (this.status >= 200 && this.status < 400) {
            var resp = JSON.parse(this.response);
            document.getElementById('tab-data').innerHTML = resp['tab-data'];
            flatpickr(".js-flatpickr-dateTime", {
                enableTime: true,
                dateFormat: "d.m.Y H:i",
            });
        }
    };

    request.onerror = function() {
        alert('Something went wrong!');
    };

    request.send();
}