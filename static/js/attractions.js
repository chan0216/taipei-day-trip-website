let url = new URL(window.location.href);
const fetchAttraction = async () => {
  const result = await fetch(`/api${url.pathname}`);
  const data = await result.json();
  const attra = data.data;
  createElement(attra);
};
function createElement(attra) {
  //創建頁面
  let rightdiv = document.querySelector(".rightdiv");
  let name = document.createElement("h3");
  let category_mrt = document.createElement("p");
  name.textContent = attra.name;
  category_mrt.textContent = `${attra.category} at${attra.mrt}`;
  rightdiv.insertBefore(name, rightdiv.children[0]);
  rightdiv.insertBefore(category_mrt, rightdiv.children[1]);
  let below = document.querySelector(".below");
  let description = document.createElement("p");
  description.textContent = attra.description;
  below.classList.add("below");
  below.insertBefore(description, below.children[0]);
  let address = document.createElement("p");
  address.textContent = attra.address;
  below.insertBefore(address, below.children[2]);
  let transport = document.createElement("p");
  transport.textContent = attra.transport;
  below.insertBefore(transport, below.children[4]);
  //處理img
  let imgurls = attra.images;
  imgurls.forEach((imgurl) => {
    let imgdiv = document.querySelector(".imgdiv");
    let silders = document.querySelector(".silders");
    let img = document.createElement("img");
    let index_span = document.createElement("span");
    index_span.classList.add("dot");
    img.src = imgurl;
    img.classList.add("attras-imgs");
    imgdiv.append(img);
    silders.append(index_span);
  });
}

fetchAttraction().then(() => {
  let current_index = 0;
  const imgs = document.querySelectorAll(".attras-imgs");
  const dots = document.querySelectorAll(".dot");
  let imgCount = imgs.length;
  function showattras() {
    //當前index超過照片總數時歸0
    if (current_index > imgCount - 1) {
      current_index = 0;
    }
    //當前index小於0時，變成最後一頁(照片總數-1)
    if (current_index < 0) {
      current_index = imgCount - 1;
    }
    //所有照片都先display none
    for (i = 0; i < imgs.length; i++) {
      dots[i].classList.remove("active");
      imgs[i].style.display = "none";
    }
    //顯示當前頁面
    dots[current_index].classList.add("active");
    imgs[current_index].style.display = "block";
  }

  function showNext() {
    current_index++;
    showattras();
  }
  function showPrev() {
    current_index--;
    showattras();
  }
  let prev_btn = document.querySelector(".prev");
  prev_btn.addEventListener("click", () => {
    showPrev();
  });
  let next_btn = document.querySelector(".next");
  next_btn.addEventListener("click", () => {
    showNext();
  });
  showattras();
});

//更改費用
let dollar = document.querySelector(".dollar");
let morn_input = document.querySelector("#morning");
let after_input = document.querySelector("#afternoon");
morn_input.addEventListener("change", () => {
  dollar.textContent = "2000";
});
after_input.addEventListener("change", () => {
  dollar.textContent = "2500";
});
