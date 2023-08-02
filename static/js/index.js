const footer = document.querySelector("footer");
const main = document.querySelector("main");
const gridbox = document.querySelector(".gridbox");
let keyword = "";
let page = 0;
let isfetching = false;
let isComposing = false;

//創建景點頁面
class Createelement {
  constructor(name, images, mrt, category, id) {
    this.name = name;
    this.images = images;
    this.mrt = mrt;
    this.category = category;
    this.id = id;
  }

  create() {
    let div = document.createElement("div");
    div.className = "div";
    div.setAttribute("onclick", "selectid(this.id)");
    div.setAttribute("id", this.id);
    //處理img
    let img = document.createElement("img");
    img.src = this.images;
    //處理景點name
    let namep = document.createElement("p");
    let namediv = document.createElement("div");
    namediv.className = "namediv";
    namep.textContent = this.name;
    //處理mrt和category
    let mrtp = document.createElement("p");
    let categoryp = document.createElement("p");
    let mrtdiv = document.createElement("div");
    mrtp.textContent = this.mrt;
    categoryp.textContent = this.category;
    mrtdiv.className = "mrtdiv";
    //合併元素
    mrtdiv.append(mrtp, categoryp);
    namediv.append(namep, mrtdiv);
    div.append(img, namediv, mrtdiv);
    gridbox.append(div);
    main.append(gridbox);
  }
}
//fetch 景點
function fetchattras() {
  if (page == null) {
    observer.unobserve(footer);
    return;
  }
  let apiurl = keyword
    ? `/api/attractions?page=${page}&keyword=${keyword}`
    : `/api/attractions?page=${page}`;
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
          return;
        }
        let attras = data.data;
        for (let attra of attras) {
          let showpage = new Createelement(
            attra.name,
            attra.images[0],
            attra.mrt,
            attra.category,
            attra.id
          );
          showpage.create();
        }
        //還有頁面，重新打開觀察
        page = data["nextPage"];
        observer.observe(footer);
        isfetching = false;
      })
      .catch((e) => {
        isfetching = false;
        alert("error");
      });
  }
}
let searchinput = document.querySelector("#search_attrs");
document.getElementById("Button").addEventListener("click", () => {
  //關鍵字搜尋前，先把觀察關掉
  observer.unobserve(footer);
  gridbox.innerHTML = "";
  keyword = document.querySelector("#search_attrs").value;
  page = 0;
  fetchattras();
});
let options = {
  rootMargin: "0px",
  threshold: 0.1,
};

let callback = (entry) => {
  if (entry[0].isIntersecting) {
    if (page !== null) {
      fetchattras();
    }
  }
};
const observer = new IntersectionObserver(callback, options);
observer.observe(footer);
//enter可提交表單
searchinput.addEventListener("compositionstart", () => {
  isComposing = true;
});

searchinput.addEventListener("compositionend", () => {
  isComposing = false;
});

searchinput.addEventListener("keydown", function (event) {
  if (event.keyCode === 13 && !isComposing) {
    event.preventDefault();
    document.querySelector("#Button").click();
  }
});

function selectid(checkid) {
  window.location.href = `/attraction/${checkid}`;
}
