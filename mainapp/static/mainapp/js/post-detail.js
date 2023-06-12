//! first wait for load like button
setTimeout(()=> {

    const likeIcon = document.getElementById('likeIcon');
    
    likeIcon.addEventListener('click',() => {
        const likeControl = likeIcon.getAttribute('data-like-control');
        console.log(likeControl)
        if (likeControl === 'True') {//#e73c04
            likeIcon.setAttribute('data-like-control', 'False');
            likeIcon.style.color = 'white';
        }
        else{
            console.log('asd')
            likeIcon.setAttribute('data-like-control', 'True');
            likeIcon.style.color = '#e73c04';
        }
    });
}, 1000);