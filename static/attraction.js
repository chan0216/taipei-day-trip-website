const footer = document.querySelector("footer");
const main = document.querySelector("main");
const gridbox = document.querySelector(".gridbox");
let keyword = "";
let page = 0;
let isfetching = false;

function attraction() {
  let apiurl = "";
  if (keyword === "") {
    apiurl = `/api/attractions?page=${page}`;
  } else {
    apiurl = `/api/attractions?page=${page}&keyword=${keyword}`;
  }
  if (isfetching === false) {
    isfetching = true;
    fetch(apiurl)
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        if (data["error"]) {
          gridbox.innerHTML = `沒有符合${keyword}的景點`;
          isfetching = false;
        } else {
          if (page !== null) {
            observer.observe(footer);
          } else {
            data["data"] === false;
            observer.unobserve(footer);
          }
          if (data["data"]) {
            let attras = data.data;
            for (let attra of attras) {
              // 裝景點的div
              let div = document.createElement("div");
              div.className = "div";
              //處理img
              let img = document.createElement("img");
              img.src = attra.images[0];
              //處理景點name
              let namep = document.createElement("p");
              let namediv = document.createElement("div");
              namediv.className = "namediv";
              namep.textContent = attra.name;
              //處理mrt和category
              let mrtp = document.createElement("p");
              let categoryp = document.createElement("p");
              let mrtdiv = document.createElement("div");
              mrtp.textContent = attra.mrt;
              categoryp.textContent = attra.category;
              mrtdiv.className = "mrtdiv";
              //合併元素
              mrtdiv.append(mrtp, categoryp);
              namediv.append(namep, mrtdiv);
              div.append(img, namediv, mrtdiv);
              gridbox.append(div);
              main.append(gridbox);
            }
          }
          isfetching = false;
          page = data["nextPage"];
        }
      })
      .catch((e) => {
        isfetching = false;
        alert("error");
      });
  }
}

let options = {
  rootMargin: "0px",
  threshold: 0.1,
};

let callback = (entry) => {
  if (entry[0].isIntersecting) {
    if (page !== null) {
      // console.log("這是callback()的");
      attraction();
    } else {
      observer.unobserve(footer);
    }
  }
};
const observer = new IntersectionObserver(callback, options);
observer.observe(footer);

function selectattrs() {
  observer.unobserve(footer);
  keyword = document.querySelector("#search_attrs").value;
  page = 0;
  gridbox.innerHTML = "";
  // console.log("selectattrs");
  attraction();
}
document
  .querySelector("#search_attrs")
  .addEventListener("keyup", function (event) {
    event.preventDefault();
    if (event.keyCode === 13) {
      document.getElementById("Button").click();
      event.target.value = "";
    }
  });
