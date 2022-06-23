function login() {
  $.ajax({
    type: "POST",
    url: "/api/login",
    data: {
      id: $("#id").val(),
      pw: $("#pw").val(),
    },
    success: function (response) {
      if (response.result == "success") {
        $.cookie("access_token", response.access_token);
        $.cookie("refresh_token", response.refresh_token);
        $.cookie("user_id", response.user_id);
        $.cookie("username", response.username);
        window.location.href = "/";
      } else {
        alert(response.msg);
      }
    },
  });
}

const form = document.querySelector("form");
form.addEventListener("submit", (e) => {
  e.preventDefault();
  login();
});

document.querySelector("#signup").addEventListener("click", () => {
  window.location.href = "/signup";
});
