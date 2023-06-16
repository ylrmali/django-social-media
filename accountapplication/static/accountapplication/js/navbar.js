/* open search */
const search = document.getElementById('search');
const searchBar = document.getElementById('search-bar');


search.addEventListener('click', ()=>{
    searchBar.style.display = 'block';
});

function closeSearch(){
    searchBar.style.display = 'none';
}

/* open notifications */
const notification = document.getElementById('notification-menu');
const actions = document.getElementById('actions');

actions.addEventListener('click', () => {
    notification.style.display = 'block';
});


/* notification */
function deleteNotification(element){
    element.remove()
};

function changeState(thisElement, targetElement){
    thisElement.innerHTML = `
        <div class="row" id='read'>
            <a class="re_follow_button"
                hx-get="{% url 'mainapp:refollow' current_user_id=noti.user.id target_user_id=noti.owner_user.id noti_id=noti.id %}">
                Sende Takip Et
            </a>
        </div>`;
};