function showModal(el){
    console.log(1);
    _targettedModal = document.querySelector('[data-modal-name="'+ el + '"]');
    _targettedModal.classList.add(modalActiveClass);
}

// function hideModal(event){
//     if(event === undefined || event.target.hasAttribute('data-modal-dismiss')) {
//         _targettedModal.classList.remove(modalActiveClass);
//     }
// }

function hideModal(){
    _targettedModal.classList.remove(modalActiveClass);
}

function bindEvents(el, callback){
    for (var i = 0; i < el.length; i++) {
        (function(i) {
            el[i].addEventListener('click', function(event) {
                callback(this, event);
            });
        })(i);
    }   
}

function triggerModal(){
    bindEvents(_triggers, function(that){
        showModal(that.dataset.modalTrigger);
    });
}

function dismissModal(){
    bindEvents(_dismiss, function(that){
        hideModal(event);
    });
}



var _targettedModal,
    _triggers = document.querySelectorAll('[data-modal-trigger]'),
    _dismiss = document.querySelectorAll('[data-modal-dismiss]'),
    modalActiveClass = "is-modal-active";
    
function initModal(){
    _targettedModal,
    _triggers = document.querySelectorAll('[data-modal-trigger]'),
    _dismiss = document.querySelectorAll('[data-modal-dismiss]'),
    modalActiveClass = "is-modal-active";
    
    triggerModal();
    dismissModal();
}