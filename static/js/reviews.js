const createReview = (e) => {
  e.preventDefault();
  let comment = $("#review-comment").val();
  let rate = $("#review-rate").val();
  let userid = "233";
  let parkid = window.location.pathname.split("/")[2];

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
