
console.log('helooo')

// function searchUser(argument){
//     $(document).ready(function() {
//         $.ajax({
//             url: `/search/${argument}/`,
//             dataType: "html",
//             success: function(response) {
//                 $("#user_results").append(response);
//                 console.log($('#user_results'))
//                 console.log(response)
//             }
//         });
//     });
//     // window.location.href = `/search/${argument}/`
// };


function searchUser(argument) {
    const userResults = document.getElementById("user-results");
    userResults.innerHTML = ''
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const response = xhr.responseText;
            userResults.innerHTML += response;
            console.log(userResults);
            console.log(response);
        }
    };
    xhr.open("GET", "/search/" + argument + "/", true);
    xhr.send();
    // window.location.href = "/search/" + argument + "/";
};

function userProfile(user_id){
    window.location.href = `/user/${user_id}/`;
};