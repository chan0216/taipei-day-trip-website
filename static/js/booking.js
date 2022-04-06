let bookingUrl = "/api/booking";
let infos = [];
//創建booking頁面
function processBooking(info) {
  if (info != null) {
    let main = document.querySelector("main");
    main.style.display = "block";
    let infoTime = info["time"] == "afternoon" ? "下半天" : "上半天";
    let booking__logo = document.querySelector(".booking__logo");
    let container__date = document.querySelector(".container__date");
    let container__time = document.querySelector(".container__time");
    let container__cost = document.querySelector(".container__cost");
    let container__place = document.querySelector(".container__place");
    let confirm__total = document.querySelector(".confirm__total");
    let name = document.createTextNode(info["attraction"]["name"]);
    let date = document.createTextNode(info["date"]);
    let time = document.createTextNode(infoTime);
    let price1 = document.createTextNode(`新台幣 ${info["price"]} 元`);
    let price2 = document.createTextNode(`新台幣 ${info["price"]} 元`);
    let address = document.createTextNode(info["attraction"]["address"]);
    container__date.appendChild(date);
    booking__logo.appendChild(name);
    container__time.appendChild(time);
    container__cost.append(price1);
    confirm__total.appendChild(price2);
    container__place.appendChild(address);
    let bookingImg = document.createElement("img");
    bookingImg.src = info["attraction"]["image"];
    bookingImg.classList.add("bookingImg");
    let section__img = document.querySelector(".section__imgdiv");
    section__img.append(bookingImg);
    infos.push(
      info["price"],
      info["attraction"]["id"],
      info["attraction"]["name"],
      info["attraction"]["address"],
      info["attraction"]["image"],
      info["date"],
      info["time"]
    );
  } else {
    let notplan = document.querySelector(".notplan");
    notplan.style.display = "block";
    let footer = document.querySelector(".footer");
    footer.classList.add("active");
  }
}
//取得資料創建headline
function getSchedule(userData) {
  if (userData == null) {
    location.href = "/";
    return;
  }
  let welcomediv = document.querySelector(".welcomediv");
  let welcomeText = document.createElement("p");
  welcomeText.textContent = `您好，${userData["name"]}，待預訂的行程如下：`;
  welcomediv.appendChild(welcomeText);
  let userName = document.querySelector("#name");
  let userEmail = document.querySelector("#email");
  userName.value = userData["name"];
  userEmail.value = userData["email"];
  fetch(bookingUrl, {
    method: "GET",
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let info = data["data"];
      processBooking(info);
    });
}
//建立預定行程，未登入則跳出登入視窗
function checkSchedule(e) {
  e.preventDefault();
  if (document.body.classList.contains("isSignIn")) {
    let selectDate = document.querySelector("#date");
    let selectTime = document.querySelector('input[name="selecttime"]:checked');
    let price = selectTime.value === "morning" ? 2000 : 2500;
    let attractionId = location.href.split("/")[4];
    fetch(bookingUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        attractionId: attractionId,
        date: selectDate.value,
        time: selectTime.value,
        price: price,
      }),
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        if (data["ok"]) {
          window.location.href = `/booking`;
        }
      });
  } else {
    loginPopup.style.display = "block";
  }
}
//刪除行程
function deleteSchedule() {
  fetch(bookingUrl, {
    method: "DELETE",
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data["ok"]) {
        location.reload();
      }
    });
}
