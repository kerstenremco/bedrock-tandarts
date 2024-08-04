let itemsStore;
let state = 1;
const endpoint = "x";
const history = [];
let waiting = false;

document.addEventListener("DOMContentLoaded", function (event) {
  const button = document.getElementById("button");
  const buttonSec = document.getElementById("buttonSec");
  const chat = document.getElementById("chat");
  const file = document.getElementById("file");
  const skeleton = document.getElementById("skeleton");
  const myMessage = document.getElementById("myMessage");
  const win = document.getElementById("win");

  buttonSec.addEventListener("click", function () {
    state = 1;
    chat.innerHTML = "";
    file.classList.remove("hidden");
    buttonSec.classList.add("hidden");
    buttonEditor(true, "Uploaden", "primary");
  });

  button.addEventListener("click", async function () {
    if (state == 1) handleUpload();
    if (state == 3) handleAccept();
  });

  myMessage.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      if (waiting) return;
      chat.innerHTML += getBubble(myMessage.value, "question");
      win.scrollTo(0, 999999);
      askQuestion();
    }
  });

  async function handleUpload() {
    state = 2;
    file.classList.add("hidden");
    skeleton.classList.remove("hidden");
    buttonEditor(false);
    // loading.classList.remove("hidden");
    const image = await imageToBase64();
    fetch(endpoint, { method: "POST", body: JSON.stringify({ image }) }).then(
      (response) => {
        response.json().then((data) => {
          if (!data.items) {
            alert(
              "Kan factuur niet lezen. Zorg ervoor dat de foto duidelijk is."
            );
            state = 1;
            skeleton.classList.add("hidden");
            chat.innerHTML = "";
            file.classList.remove("hidden");
            buttonSec.classList.add("hidden");
            buttonEditor(true, "Uploaden", "primary");
            return;
          }
          state = 3;
          const items = data.items;
          itemsStore = items;
          const it = itemsStore.map((item) => `<li>${item}</li>`).join("");
          skeleton.classList.add("hidden");
          chat.innerHTML += getBubble(
            `Ik zie de volgende items: <ul>${it}</ul>`
          );
          chat.innerHTML += getBubble("Klopt dit?");
          win.scrollTo(0, 999999);
          buttonEditor(true, "Ja", "success");
          buttonSec.classList.remove("hidden");
        });
      }
    );
  }

  function handleAccept() {
    state = 4;
    buttonSec.classList.add("hidden");
    buttonEditor(false);
    chat.innerHTML += getBubble("Wat wil je weten?");
    win.scrollTo(0, 999999);
    myMessage.classList.remove("hidden");
  }

  function getBubble(text, type = "response") {
    let el = `<div class="chat chat-start"><div class="chat-bubble">TEXT</div></div>`;
    if (type == "question") el = el.replace("chat-start", "chat-end");
    return el.replace(/TEXT/g, text);
  }

  function buttonEditor(show, text, color = "primary") {
    if (!show) return button.classList.add("hidden");
    button.innerHTML = text;
    button.classList.forEach((element) => {
      if (element.includes("btn-")) button.classList.remove(element);
    });
    button.classList.add(`btn-${color}`);
    button.classList.remove("hidden");
  }

  function askQuestion() {
    const question = myMessage.value;
    myMessage.value = "";
    waiting = true;
    fetch(endpoint, {
      method: "POST",
      body: JSON.stringify({ items: itemsStore, question, history }),
    }).then((response) => {
      response.json().then((data) => {
        waiting = false;
        const items = data.items;
        chat.innerHTML += getBubble(data.answer, "answer");
        history.push(["user", question], ["assistant", data.answer]);
      });
    });
  }

  async function imageToBase64() {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      const f = file["files"][0];
      reader.readAsDataURL(f);
      reader.onload = function () {
        base64String = reader.result.replace("data:", "").replace(/^.+,/, "");
        resolve(base64String);
      };
      reader.onerror = function (error) {
        reject(error);
      };
    });
  }
});
