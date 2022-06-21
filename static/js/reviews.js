const createReview = (e) => {
  e.preventDefault();
  let comment = $("#review-comment").val();
  let rate = $("#review-rate").val();
  let userid = localStorage.getItem('userid');
  let parkid = window.location.pathname.split("/")[2];
1
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
      window.location.href = "/reviews";
    },
  });
};

const reviewForm = document.querySelector(".review-form");
reviewForm.addEventListener("submit", (e) => createReview(e));

// const getAllParkReview() => {}