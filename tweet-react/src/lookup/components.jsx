
export const loadTweets = (setTweets , username) => {
    let url;
    if (username) {
        url = `http://127.0.0.1:8000/tweets/?username=${username}`
    } else {
        url = 'http://127.0.0.1:8000/tweets/'
    }
    fetch(url).then(response => response.json()).then(r => {
      setTweets(r)
    }).catch(e => alert("there was an error"));
}

export const handleDidLike = (id , callback , content , action) => {
    const xhr = new XMLHttpRequest()
    const csrftoken = getCookie('csrftoken')
    xhr.open("POST" , "http://127.0.0.1:8000/tweet/action/")
    xhr.setRequestHeader("Content-Type" , "application/json")
    if(csrftoken) {
        // xhr.setRequestHeader("HTTP_X_REQUESTED_WITH" , "XMLHttpRequest")
        xhr.setRequestHeader("X-Requested-With" , "XMLHttpRequest") 
        xhr.setRequestHeader("X-CSRFToken" , csrftoken)
    }
    const data = JSON.stringify({
        id : id,
        action : action,
        content : content
    })
    xhr.onload = () => {
        console.log(xhr.status)
        callback(xhr.response , xhr.status)
    }  
    xhr.onerror = (e) => {
        alert("there was an error2")
    }
    xhr.send(data)
}


export const createTweet = (content , callback) => {
    const xhr = new XMLHttpRequest()
    const csrftoken = getCookie('csrftoken')
    xhr.open("POST" , "http://127.0.0.1:8000/create-tweet")
    xhr.setRequestHeader("Content-Type" , "application/json")
   
    if(csrftoken) {
        // xhr.setRequestHeader("HTTP_X_REQUESTED_WITH" , "XMLHttpRequest")
        xhr.setRequestHeader("X-Requested-With" , "XMLHttpRequest") 
        xhr.setRequestHeader("X-CSRFToken" , csrftoken)
    }
    const data = JSON.stringify({
        content : content
    })
    xhr.onload = () => {
        callback(xhr.response , xhr.status)
    }  
    xhr.onerror = (e) => {
        alert("there was an error in create tweet")
    }
    xhr.send(data)
}

const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}