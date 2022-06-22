$(document).ready(function () {
  const park_id = window.location.pathname.split("/")[2];
  show_map(park_id);
  show_reviews(park_id);
});

function show_map(park_id) {
  $.ajax({
    type: "GET",
    url: `/api/parks/${park_id}`,
    success: function (response) {
      if (response.result == "success") {
        const park = response.park;

        let map = new naver.maps.Map("park-map", {
          center: new naver.maps.LatLng(park["위도"], park["경도"]),
          zoom: 17,
          zoomControl: true,
          zoomControlOptions: {
            style: naver.maps.ZoomControlStyle.SMALL,
            position: naver.maps.Position.TOP_RIGHT
          }
        });

        let marker = new naver.maps.Marker({
          position: new naver.maps.LatLng(park["위도"], park["경도"]),
          map: map
        });
      }
    },
  });
}

function show_reviews(park_id) {
  $.ajax({
    type: "GET",
    url: `/api/reviews/${park_id}`,
    success: function (response) {
      if (response.result == "success") {
        const reviews = response.reviews;

        if (!reviews) {
          $('#review-empty').show();
          $('#review-list').hide();
          return;
        }

        $('#review-list').show();
        $('#review-empty').hide();

        const user_id = decodeURIComponent(getCookieValue("user_id"));

        for (let review of reviews) {
          let temp_html = ``
          if (user_id == review.userid) {
            temp_html = `<ul>
                           <li class="list-all list-park">
                             <div class="wrap-comment">
                               <p>⭐ <span class="list-rate">${review.rate}</span></p>
                               <p>${review.comment}<em class="list-username">-${review.username}</em></p>
                               <button type="button" onclick="delete_review('${review._id}')">삭제</button>
                             </div>
                           </li>
                         </ul>`
          } else {
            temp_html = `<ul>
                           <li class="list-all list-park">
                             <div class="wrap-comment">
                               <p>⭐ <span class="list-rate">${review.rate}</span></p>
                               <p>${review.comment}<em class="list-username">-${review.username}</em></p>
                             </div>
                           </li>
                         </ul>`
          }
          $('#review-list').append(temp_html);
        }
      }
    },
  });
}

function delete_review(review_id) {
  console.log(review_id);
  $.ajax({
    type: "DELETE",
    url: `/api/reviews`,
    data: {
      review_id: review_id
    },
    success: function (response) {
      if (response.result == "success") {
        alert("리뷰가 삭제되었습니다.");
        location.reload();
      }
    },
  });
}

const getCookieValue = (key) => {
  let cookieKey = key + "="; 
  let result = "";
  const cookieArr = document.cookie.split(";");
  
  for(let i = 0; i < cookieArr.length; i++) {
    if(cookieArr[i][0] === " ") {
      cookieArr[i] = cookieArr[i].substring(1);
    }
    
    if(cookieArr[i].indexOf(cookieKey) === 0) {
      result = cookieArr[i].slice(cookieKey.length, cookieArr[i].length);
      return result;
    }
  }
  return result;
}

const createReview = (e) => {
  e.preventDefault();
  const user_id = decodeURIComponent(getCookieValue("user_id"));
  const username = decodeURIComponent(getCookieValue("username"));
  const park_id = window.location.pathname.split("/")[2];
  const comment = $("#review-comment").val();
  const rate = $("#review-rate").val();

  if (comment == "" || rate == "") {
    return alert("빈 값을 모두 입력해주세요.");
  }

  $.ajax({
    type: "POST",
    url: "/api/reviews",
    data: {
      user_id: user_id,
      username: username,
      park_id: park_id,
      comment: comment,
      rate: rate,
    },
    success: function (response) {
      console.log(response);
      alert(response["msg"]);
      setTimeout(function() {
        toggleReviewOn();
        location.reload();
      },400);
    },
  });
};

const reviewSection = document.querySelector(".sect-review");
const reviewForm = document.querySelector(".review-form");
const btnCancel = document.querySelector('.btn-cancel');
const btnAddreview = document.querySelector(".btn-addreview");

const toggleReviewOn = () => {
  reviewSection.classList.toggle('on');
}

btnAddreview.addEventListener("click", toggleReviewOn);
btnCancel.addEventListener("click", toggleReviewOn);
reviewForm.addEventListener("submit", (e) => createReview(e));