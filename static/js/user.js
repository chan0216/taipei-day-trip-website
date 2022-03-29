let loginPopup = document.querySelector(".loginPopup");
let signupPopup = document.querySelector(".signupPopup");
let loginPopupsignup = document.querySelector(".loginPopup-signup");
let signupPopuplogin = document.querySelector(".signup-Popuplogin");
let signupForm = document.querySelector(".signupForm");
let loginform = document.querySelector(".loginform");
//顯示登入畫面
document.querySelector(".signin_text").addEventListener("click", () => {
  loginPopup.style.display = "block";
});
//顯示註冊畫面
document.querySelector(".signup_text").addEventListener("click", () => {
  signupPopup.style.display = "block";
});
//關閉登入畫面
document.querySelector("#loginCloseButton").addEventListener("click", () => {
  loginPopup.style.display = "none";
});
//關閉註冊畫面
document.querySelector("#signupCloseButton ").addEventListener("click", () => {
  signupPopup.style.display = "none";
});
//從登入畫面點擊到註冊畫面
loginPopupsignup.addEventListener("click", () => {
  loginPopup.style.display = "none";
  signupPopup.style.display = "block";
});
//從註冊畫面點擊到登入畫面
signupPopuplogin.addEventListener("click", () => {
  signupPopup.style.display = "none";
  loginPopup.style.display = "block";
});
//會員註冊
let URL = "/api/user";
signupForm.addEventListener("submit", (e) => {
  e.preventDefault();
  let signup_note = document.querySelector(".signup_note");
  let signup_name = document.querySelector("#signup-name");
  let signup_email = document.querySelector("#signup-email");
  let signup_password = document.querySelector("#signup-password");
  fetch(URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: signup_name.value,
      email: signup_email.value,
      password: signup_password.value,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data["error"]) {
        signup_note.textContent = data["message"];
        signup_note.classList.add("warming");
        signupForm.style.height = "350px";
        return;
      }
      signup_note.textContent = "註冊成功";
      signup_note.classList.remove("warming");
      signup_note.classList.add("hint");
      signupForm.style.height = "350px";
      signup_name.value = "";
      signup_email.value = "";
      signup_password.value = "";
    });
});
//會員登入
loginform.addEventListener("submit", (e) => {
  e.preventDefault();
  let login_email = document.querySelector("#login_email");
  let login_pwd = document.querySelector("#login_pwd");
  fetch(URL, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email: login_email.value,
      password: login_pwd.value,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data["error"]) {
        document.querySelector(".login_note").textContent = data["message"];
        document.querySelector(".login_note").classList.add("warming");
        loginform.style.height = "295px";
      } else {
        location.reload();
      }
    });
});
//取得當前登入使用者的資料
document.addEventListener("DOMContentLoaded", (e) => {
  fetch(URL, {
    method: "GET",
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data["data"] == null) {
        document.querySelector(".signin").style.display = "block";
      } else {
        document.body.classList.add("isSignIn");
        document.querySelector(".signin").style.display = "none";
        let signout = document.createElement("p");
        signout.textContent = "登出系統";
        signout.style.color = "#666666";
        signout.style.cursor = "pointer";
        signout.setAttribute("onclick", "deleteUser();");
        let memberdiv = document.querySelector(".memberdiv");
        memberdiv.append(signout);
      }
      if (location.href.split("/")[3] == "booking") {
        getSchedule(data["data"]);
      }
    });
});

function deleteUser() {
  fetch(URL, { method: "DELETE" })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data["ok"]) {
        location.reload();
      }
    });
}

function openPopup() {
  if (document.body.classList.contains("isSignIn")) {
    location.href = "/booking ";
  } else {
    loginPopup.style.display = "block";
  }
}
