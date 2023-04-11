/* open search */
const search = document.getElementById('search');
const searchBar = document.getElementById('search-bar');


search.addEventListener('click', ()=>{
    searchBar.style.display = 'block';
});

function closeSearch(){
    searchBar.style.display = 'none';
}