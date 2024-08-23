"use strict"

const ratings = document.querySelectorAll('.rating');
if(ratings.length > 0){
    initRatings();
}

function initRatings(){
    let ratingActive, ratingValue;
    function setRatingArgs(rating){
        ratingActive = rating.querySelector('.rating-active');
        ratingValue = rating.querySelector('.rating-value');
    }

    function setRatingActiveWidth(index = ratingValue.innerHTML){
        const ratingActiveWidth = index / 0.05;
        ratingActive.style.width = `${ratingActiveWidth}%`;
    }

    function setRating(rating){
        setRatingArgs(rating);
        setRatingActiveWidth();
        if (rating.classList.contains('rating-set')){
            checkRating(rating);
        }
    }

    for(let index = 0; index < ratings.length; index++){
        setRating(ratings[index]);
    }

    function checkRating(rating) {
        const ratingItems = rating.querySelectorAll('.rating-item');
        for (let index = 0; index < ratingItems.length; index++){
            const ratingItem = ratingItems[index];
            ratingItem.addEventListener("mouseenter", function (e) {
                setRatingArgs(rating);
                setRatingActiveWidth(ratingItem.value);
            });
            ratingItem.addEventListener("mouseleave", function (e) {
                setRatingActiveWidth();
            });
            ratingItem.addEventListener("click", function (e) {
                setRatingArgs(rating);
                if(rating.dataset.ajax) {
                    setRatingValue(ratingItem.value, rating);
                }else{
                    ratingValue.innerHTML = index + 1;
                    setRatingActiveWidth();
                }
            });
        }
    }

    async function setRatingValue(value, rating){
        if(!rating.classList.contains('rating-sending')) {
            rating.classList.add('rating-sending');
            let response = await fetch("/add_rate/", {
                method: 'POST',
                body: JSON.stringify({
                    userRating: value,
                    carId: rating.id
                }),
                headers: {
                    'content-type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
            if (response.ok){
                const result = await response.json();
                const type = result.type;
                if(type === 'answer'){
                    const newRating = result.newRating;
                    const newCount = result.newCount;
                    ratingValue.innerHTML = newRating;
                    rating.querySelector('.rating-count').innerHTML = newCount;
                    setRatingActiveWidth();
                }else if(type === 'error'){
                    const msg = result.message;
                    alert(msg);
                }
                rating.classList.remove('rating-sending');
            } else {
                alert("Ошибка!");
                rating.classList.remove('rating-sending');
            }
        }
    }
}

// Функция для получения CSRF токена из cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
