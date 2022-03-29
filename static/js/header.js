let header = ` <div class="loginPopup">
<form class="loginform">
  <div class="decorator-bar"></div>
  <img
    class="CloseButton"
    id="loginCloseButton"
    src="../static/img/icon_close.png"
    alt=""
  />
  <h3 class="user-h3">登入會員帳號</h3>
  <input
    id="login_email"
    class="user-input"
    type="email"
    placeholder="輸入電子信箱"
    required
  />
  <br />
  <input
    id="login_pwd"
    class="user-input"
    type="password"
    placeholder="輸入密碼"
    required
  />
  <br />
  <button class="user-btn" type="submit">登入帳戶</button>
  <p class="login_note"></p>
  <p><a class="loginPopup-signup">還沒有帳戶？點此註冊</a></p>
</form>
</div>
<div class="signupPopup">
<form class="signupForm" method="post">
  <div class="decorator-bar"></div>

  <img
    class="CloseButton"
    id="signupCloseButton"
    src="../static/img/icon_close.png"
    alt=""
  />
  <h3 class="user-h3">註冊會員帳號</h3>
  <input
    class="user-input"
    id="signup-name"
    type="text"
    placeholder="輸入姓名"
    required
  />
  <input
    class="user-input"
    id="signup-email"
    type="email"
    placeholder="輸入電子郵件"
    required
    
  />
  <input
    class="user-input"
    id="signup-password"
    type="password"
    placeholder="輸入密碼"
   
    required
  />
  <button class="user-btn" type="submit" id="signup-btn">
    註冊新帳戶
  </button>
  <p class="signup_note"></p>
  <div class="signup-Popuplogin"><a>已經有帳戶了？點此登入</a></div>
</form>
</div>
<nav>
<div class="container">
  <p class="logo"><a href="/">台北一日遊</a></p>

  <div class="menu">
    <div class="reservediv">
      <p><a class="text" onclick="openPopup()">預定行程</a></p>
    </div>
    <div class="memberdiv">
      <p class="signin">
        <a class="signin_text">登入<a class="signup_text">/註冊</a></a>
      </p>
    </div>
  </div>
</div>
</nav>`;

document.write(header);
// pattern="[a-zA-Z0-9.-_]{1,}@[a-zA-Z.-]{2,}[.]{1}[a-zA-Z]{2,}"
// pattern="^(?=.*[a-zA-Z])(?=.*[0-9]).{6,}$"
