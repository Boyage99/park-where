function validate_id() {
  const id = $("#id").val();

  if (id == "") {
    $("#idMsg").text("필수정보입니다.").show();
    return false;
  }

  const regExp = /^(?=.*[a-z])[a-z0-9_-]{5,20}$/;

  if (!regExp.test(id)) {
    $("#idMsg").text("5~20자의 영문 소문자, 숫자와 특수기호(_),(-)만 사용 가능합니다.").show();
    return false;
  }

  $.ajax({
    type: "POST",
    url: "/api/signup/check_dup",
    data: {
      id: id
    },
    success: function (response) {
      if (response.exists) {
        $("#idMsg").text("이미 사용중인 아이디입니다.").show();
        return false;
      } else {
        $("#idMsg").hide();
        return true;
      }
    }
  });
}

function validate_pw() {
  const pw = $("#pw").val();

  if (pw == "") {
    $("#pwMsg").text("필수정보입니다.").show();
    return false;
  }

  const regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,16}$/;

  if (!regExp.test(pw)) {
    $("#pwMsg").text("8~16자 영문 대 소문자, 숫자, 특수문자(!@#$%^&*)를 사용하세요.").show();
    return false;
  }

  $("#pwMsg").hide();

  return true;
}

function validate_pw_check() {
  const pw_check = $("#password_check").val();

  if (pw_check == "") {
    $("#pwCheckMsg").text("필수정보입니다.").show();
    return false;
  }

  const pw = $("#pw").val();

  if (pw != pwCheck) {
    $("#pwCheckMsg").text("비밀번호가 일치하지 않습니다.").show();
    return false;
  }

  $("#pwCheckMsg").hide();

  return true;
}

function validate_name() {
  const name = $("#username").val();

  if (name == "") {
    $("#nameMsg").text("필수정보입니다.").show();
    return false;
  }

  $("#nameMsg").hide();

  return true;
}

function validate_all() {
  const is_validate_id = validate_id();
  const is_validate_pw = validate_pw();
  const is_validate_pw_check = validate_pw_check();
  const is_validate_name = validate_name();

  return is_validate_id && is_validate_pw && is_validate_pw_check && is_validate_name;
}

function signup() {
  if (validate_all()) {
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
}

const form = document.querySelector("form");
form.addEventListener("submit", (e) => {
  e.preventDefault();
  signup();
});
