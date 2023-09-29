
function close_modal(dialog, e) {
    const dialogDimensions = dialog.getBoundingClientRect()

    
    if (
      e.clientX < dialogDimensions.left ||
      e.clientX > dialogDimensions.right ||
      e.clientY < dialogDimensions.top ||
      e.clientY > dialogDimensions.bottom
    ) {
      
      dialog.close()
    }
  }


  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Check if the cookie name matches the CSRF cookie name (default: 'csrftoken')
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function follow_user(user_id) {

  var follow_btn = document.getElementById(user_id)

  var is_following = (follow_btn?.innerText === 'Following')

  var xhttp = new XMLHttpRequest()
  xhttp.onreadystatechange = function () {
      if (this.readyState == 4) {
          if (this.status == 200) {
              if (is_following) {
                  // already followed make it unfollow
                  follow_btn.innerText = 'Follow'
              }
              else {
                  follow_btn.innerText = "Following"
              }
              // reload the page
              location.reload();
          }
          else {
              // handle error respons
          }
      }
  }

  xhttp.open("POST", "/follow/", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("user_id=" + user_id)

}


