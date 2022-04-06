TPDirect.setupSDK(
  123945,
  "app_icwdks3d58xoYoJtjzjOB8HUFTsvLbZfXfYWPrgndGj3onnAb9Sm74xA0YfZ",
  "sandbox"
);

let fields = {
  number: {
    // css selector
    element: "#card-number",
    placeholder: "**** **** **** ****",
  },
  expirationDate: {
    // DOM object
    element: document.getElementById("card-expiration-date"),
    placeholder: "MM / YY",
  },
  ccv: {
    element: "#card-ccv",
    placeholder: "CVV",
  },
};

TPDirect.card.setup({
  fields: fields,
  styles: {
    // Style all elements
    input: {
      color: "gray",
    },
    // Styling ccv field
    "input.ccv": {
      "font-size": "16px",
    },
    // Styling expiration-date field
    "input.expiration-date": {
      "font-size": "16px",
    },
    // Styling card-number field
    "input.card-number": {
      "font-size": "16px",
    },
    // style focus state
    ":focus": {
      color: "black",
    },
    // style valid state
    ".valid": {
      color: "green",
    },
    // style invalid state
    ".invalid": {
      color: "red",
    },
    // Media queries
    // Note that these apply to the iframe, not the root window.
    "@media screen and (max-width: 400px)": {
      input: {
        color: "orange",
      },
    },
  },
});
let cardprompt = document.querySelector(".cardprompt");
function onSubmit(event) {
  // 取得 TapPay Fields 的 status
  let name = document.querySelector("#name").value;
  let email = document.querySelector("#email").value;
  let phone = document.querySelector("#phone").value;
  let prompt = document.querySelector(".prompt");

  let phoneRegexp = "^(09)[0-9]{8}$";
  let emailRegexp = "[a-zA-Z0-9.-_]{1,}@[a-zA-Z.-]{2,}[.]{1}[a-zA-Z]{2,}";
  if (name == "" || email == "" || phone == "") {
    prompt.textContent = "請輸入完整";
  } else if (!phone.match(phoneRegexp)) {
    prompt.textContent = "手機格式不符合";
  } else if (!email.match(emailRegexp)) {
    prompt.textContent = "Email格式不符合";
  } else {
    prompt.textContent = "";
  }
  const tappayStatus = TPDirect.card.getTappayFieldsStatus();
  if (tappayStatus.canGetPrime === false) {
    console.log("can not get prime");
    cardprompt.textContent = "信用卡填寫錯誤";
    return;
  }
  // Get prime
  TPDirect.card.getPrime((result) => {
    if (result.status !== 0) {
      console.log("get prime error " + result.msg);
      cardprompt.textContent = "信用卡填寫錯誤";
      return;
    }
    // console.log("get prime 成功，prime: " + result.card.prime);
    let prime = result.card.prime;
    cardprompt.textContent = "";
    submitPrime(prime);
    // send prime to your server, to pay with Pay by Prime API .
    // Pay By Prime Docs: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-prime-api
  });
}
function submitPrime(prime) {
  let name = document.querySelector("#name").value;
  let email = document.querySelector("#email").value;
  let phone = document.querySelector("#phone").value;
  fetch("/api/orders", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      prime: prime,
      order: {
        price: infos[0],
        trip: {
          attraction: {
            id: infos[1],
            name: infos[2],
            address: infos[3],
            image: infos[4],
          },
          date: infos[5],
          time: infos[6],
        },
        contact: {
          name: name,
          email: email,
          phone: phone,
        },
      },
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data["error"]) {
        cardprompt.textContent = data["message"];
      } else if (data["data"]["payment"]["status"] != 0) {
        cardprompt.textContent =
          data["data"]["payment"]["message"] + "，請再試一次";
      } else {
        window.location.href = `/thankyou?number=${data["data"]["number"]}`;
      }
    });
}
