function delete_problem_from_competition(delete_url){
    if(confirm('Are you sure you want to delete this problem from competition?')){
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

function getCookie(name) {

    var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
};