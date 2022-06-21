function signup() {
  $.ajax({
    type: "POST",
    url: "/api/signup",
    data: {
      id: $("#id").val(),
      pw: $("#pw").val(),
      username: $("#username").val(),
    },
    success: function (response) {
      if (response.result == "success") {
        alert("회원가입이 완료되었습니다.");
        window.location.href = "/login";
      } else {
        alert(response.msg);
      }
    },
  });
}

const form = document.querySelector("form");
form.addEventListener("submit", (e) => {
  e.preventDefault();
  signup();
});
