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
        $.cookie("token", response.token);
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
