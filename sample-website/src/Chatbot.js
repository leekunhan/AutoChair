import React, { useState } from "react";
import "./Chatbot.css";

function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");

  const handleToggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (userInput.trim() === "") return;

    const newUserMessage = { sender: "user", text: userInput };
    setMessages((prev) => [...prev, newUserMessage]);
    
    // 立即清空輸入框
    setUserInput("");

    try {
      const res = await fetch("http://localhost:8000/search_chair", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userInput: userInput }),
      });
      const data = await res.json();

      const botTextMessage = {
        sender: "bot",
        text: `🔍 <strong>我幫你找到的椅子:</strong> ${data.chair}<br/>
               ⚖️ <strong>最大承重:</strong> ${data.max_weight} kg<br/>
               🔗 <a href="${data.url}" target="_blank">點擊查看</a>`,
      };
      setMessages((prev) => [...prev, botTextMessage]);

      if (data.image_path) {
        let imageUrl = data.image_path.startsWith("http") ? data.image_path
                      : `http://localhost:8000${data.image_path.replace("./chair_image", "/chair_image")}`;

        const botImageMessage = {
          sender: "bot",
          type: "image",
          url: imageUrl,
          caption: `推薦椅子: ${data.chair}`,
        };
        setMessages((prev) => [...prev, botImageMessage]);
      }
    } catch (err) {
      console.error("API Error:", err);
      setMessages((prev) => [...prev, { sender: "bot", text: "伺服器錯誤，請稍後再試。" }]);
    }
  };

  return (
    <>
      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <span>推薦機器人</span>
            <button onClick={handleToggleChat} className="close-button">X</button>
          </div>

          <div className="chatbot-body">
            <div className="chatbot-messages">
              {messages.map((msg, idx) => (
                msg.type === "image" ? (
                  <div key={idx} className="chatbot-message bot-message">
                    <p>{msg.caption}</p>
                    <img src={msg.url} alt="Chair" style={{ maxWidth: "200px", borderRadius: "8px" }} />
                  </div>
                ) : (
                  <div key={idx} className={`chatbot-message ${msg.sender === "user" ? "user-message" : "bot-message"}`}
                       dangerouslySetInnerHTML={{ __html: msg.text }} />
                )
              ))}
            </div>

            <form className="chatbot-input-area" onSubmit={handleSend}>
              <input type="text" placeholder="輸入訊息..." value={userInput} onChange={(e) => setUserInput(e.target.value)}
                     className="chatbot-input" />
              <button type="submit" className="chatbot-send-btn">送出</button>
            </form>
          </div>
        </div>
      )}

      <button onClick={handleToggleChat} className="chatbot-button">
        {isOpen ? "關閉機器人" : "開啟機器人"}
      </button>
    </>
  );
}

export default Chatbot;
