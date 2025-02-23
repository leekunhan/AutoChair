// App.js
import React from "react";
import "./App.css"; 
// 從 Chatbot.js 匯入
import Chatbot from "./Chatbot"; // <- 注意檔名路徑要正確

// 導覽列元件
function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-logo">MarsRhino 火星犀牛</div>
      <ul className="navbar-links">
        <li>產品</li>
        <li>品牌</li>
        <li>支援</li>
        <li>專業服務</li>
        <li>購買地點</li>
      </ul>
    </nav>
  );
}

// 主內容區元件
function MainContent() {
  return (
    <main className="main-content">
      <section className="about-section">
        <h1>關於 MARSRHINO</h1>
        <h2>MarsRhino 火星犀牛 人體工學椅的專業品牌</h2>
        <p>
          MarsRhino火星犀牛擁有30年研發製造人體工學椅經驗。
          <br />
          致力打造美型與功能兼具的創新產品，並且提供最佳服務品質，就是我們的品牌精神！
        </p>
        <p>
          Mars火星 擁有無限的可能性
          <br />
          Rhino犀牛 代表強壯、毅力與專注
          <br />
          兩者合體象徵我們追求極致、永無止境！
        </p>
      </section>
    </main>
  );
}

// 底部導覽列元件
function Footer() {
  return (
    <footer className="footer">
      <div className="footer-col">
        <h3>產品</h3>
        <ul>
          <li>人體工學椅</li>
          <li>辦公桌</li>
          <li>辦公周邊</li>
        </ul>
      </div>
      <div className="footer-col">
        <h3>品牌</h3>
        <ul>
          <li>關於MARSRHINO</li>
        </ul>
      </div>
      <div className="footer-col">
        <h3>支援</h3>
        <ul>
          <li>聯繫我們</li>
          <li>保固</li>
          <li>常見問題</li>
          <li>下載</li>
        </ul>
      </div>
      <div className="footer-col">
        <h3>專業服務</h3>
        <ul>
          <li>專案諮詢</li>
        </ul>
      </div>
      <div className="footer-col">
        <h3>購買地點</h3>
        <ul>
          <li>購買地點</li>
        </ul>
      </div>
    </footer>
  );
}

function App() {
  return (
    <div className="App">
      <Navbar />
      <MainContent />
      <Footer />
      {/* 右下角聊天機器人(已移除原先定義，改為匯入) */}
      <Chatbot />
    </div>
  );
}

export default App;
