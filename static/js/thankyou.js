let url = window.location.href;
let wrongOrder = document.createElement("p");
let main = document.querySelector("main");
let footer = document.querySelector(".footer");
let order_numbr = url.split("=")[1];
fetch(`/api/order/${order_numbr}`)
  .then((response) => {
    return response.json();
  })
  .then((res) => {
    if (res["error"]) {
      document.body.style.display = "none";
      window.location.href = "/";
    }
    if (res["data"] == null) {
      main.innerHTML = "";
      wrongOrder.classList.add("wrongOrder");
      footer.style.height = "70%";
      wrongOrder.textContent = res["message"];
      main.append(wrongOrder);
      return;
    }
    if (res["data"]["status"] == 0) {
      let infoTime =
        res["data"]["trip"]["time"] == "afternoon" ? "下半天" : "上半天";
      let ordercontainer_imgdiv = document.querySelector(
        ".ordercontainer_imgdiv"
      );
      //放置圖片
      let orderImg = document.createElement("img");
      orderImg.src = res["data"]["trip"]["attraction"]["image"];
      orderImg.classList.add("orderImg");
      ordercontainer_imgdiv.append(orderImg);
      //放置文字
      let orderSuccess = document.createElement("h2");
      orderSuccess.textContent = "感謝您的訂購";
      let ordercontainer_text = document.querySelector(".ordercontainer_text");
      let orderName = document.createElement("h3");
      orderName.textContent = `台北一日遊：${res["data"]["trip"]["attraction"]["name"]}`;
      let orderNumber = document.createElement("p");
      orderNumber.textContent = `訂單編號：${res["data"]["number"]}`;
      let orderDate = document.createElement("p");
      orderDate.textContent = `預定日期：${res["data"]["trip"]["date"]}`;
      let orderTime = document.createElement("p");
      orderTime.textContent = `預定時間：${infoTime}`;
      ordercontainer_text.append(
        orderSuccess,
        orderName,
        orderNumber,
        orderDate,
        orderTime
      );
    } else {
      main.innerHTML = "";
      wrongOrder.classList.add("wrongOrder");
      footer.style.height = "70%";
      wrongOrder.textContent = "付款失敗";
      main.append(wrongOrder);
    }
  });
