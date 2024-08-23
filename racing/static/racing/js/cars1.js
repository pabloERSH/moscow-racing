"use strict"

const ratings = document.querySelectorAll('.rating');
if(ratings.length > 0){
    initRatings();
}

function initRatings(){
    let ratingActive, ratingValue;
    const rateSocket = new WebSocket(`ws://${window.location.host}/ws/socket-server/`);

    function setRatingArgs(rating){
        ratingActive = rating.querySelector('.rating-active');
        ratingValue = rating.querySelector('.rating-value');
    }

    function setRatingActiveWidth(index = ratingValue.innerHTML){
        const ratingActiveWidth = index / 0.05;
        ratingActive.style.width = `${ratingActiveWidth}%`;
    }

    function send_new_rating(value, rating_id){
        rateSocket.send(JSON.stringify({
                'userRating': value,
                'carId': rating_id
        }))
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

    rateSocket.onmessage = function(e){
        let data = JSON.parse(e.data)
        if(data['type'] === 'error'){
            alert(data['message']);
        }else{
            let newRating = data['newRating'];
            let newCount = data['newCount'];
            let carId = data['carId'];
            let rating = document.getElementById(carId);
            rating.querySelector('.rating-value').innerHTML = newRating;
            rating.querySelector('.rating-count').innerHTML = newCount;
            setRatingArgs(rating);
            setRatingActiveWidth();
        }
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
                    if(!rating.classList.contains('rating-sending')) {
                        rating.classList.add('rating-sending');
                        send_new_rating(ratingItem.value, rating.id);
                        rating.classList.remove('rating-sending');
                    }
                }else{
                    ratingValue.innerHTML = index + 1;
                    setRatingActiveWidth();
                }
            });
        }
    }
}
