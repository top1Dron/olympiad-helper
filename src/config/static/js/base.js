import {ready, checkOverflow} from './services.js'

ready(function(){
    var form_element = document.getElementById('form_menu');
    var increseHeight = 10, cnt=0;
    while(checkOverflow(form_element) && cnt < 100){
        var currentValue = parseInt(getComputedStyle(form_element).height, 10);
        form_element.style.height = (currentValue + increseHeight) + "px";
        cnt++;
    }
})