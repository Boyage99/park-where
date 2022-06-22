$(document).ready(function () {
  getParkMap();
  getParkReview();
});

const getParkMap = () => {
  const park_id = window.location.pathname.split("/")[2];

  let lat, long;

  $.ajax({
    type: "GET",
    url: `/api/parks/${park_id}`,
    async: false,
    success: function (response) {
      if (response.result == "success") {
        const park = response.park;
        lat = park["위도"];
        long = park["경도"];

        let map = new naver.maps.Map("park-map", {
          center: new naver.maps.LatLng(lat, long),
          zoom: 17,
          zoomControl: true,
          zoomControlOptions: {
            style: naver.maps.ZoomControlStyle.SMALL,
            position: naver.maps.Position.TOP_RIGHT
          }
        });

        let marker = new naver.maps.Marker({
          position: new naver.maps.LatLng(lat, long),
          map: map
        });
      }
    },
  });
}

const getParkReview = () => {
  let parkid = window.location.pathname.split("/")[2];
  $.ajax({
      type: "GET",
      url: `/api/reviews/${parkid}`,
      data: {},
      success: function (res) {
          console.log(res);
      }
  })
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
  let comment = $("#review-comment").val();
  let rate = $("#review-rate").val();
  let username = getCookieValue('username')
  let userid = decodeURIComponent(username);
  let parkid = window.location.pathname.split("/")[2];
  
  if (!(comment && rate && userid && parkid)) {
    return alert("빈 값을 모두 입력해주세요.");
  }

  $.ajax({
    type: "POST",
    url: "/api/reviews",
    data: {
      userid_give: userid,
      parkid_give: parkid,
      comment_give: comment,
      rate_give: rate,
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