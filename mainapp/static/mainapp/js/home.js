const imageBox = document.getElementById('image-box');
const media = document.getElementById('media');
const imageLabel = document.getElementById('image-label');
const post = document.getElementById('post');
const shareBtn = document.getElementById('shareBtn');
const like = document.getElementById('like');
const likeIcon = document.getElementById('likeIcon');


// when a photo selected, show photo
// hide image uploaded icon
// add close button
// show share button
media.onchange = photo => {
    const [image] = [photo.target.files[0]];
    imageBox.innerHTML = `
        <img class="preview-image" src="${URL.createObjectURL(image)}" alt="">
        <button class="closeBtn">
            <i class="fa-solid fa-xmark" style="color: #ffffff;"></i>
        </button>
    `
    console.log(URL.createObjectURL(image))
    imageLabel.style.display = 'none';
    shareBtn.removeAttribute('disabled');
};

// when writing something in textarea, share button will be active
// and if textarea is empty, set disable share button
post.addEventListener('input',(text)=>{
    shareBtn.removeAttribute('disabled');
    if (text.target.value === ""){
        shareBtn.setAttribute('disabled','disabled');
    }
});




