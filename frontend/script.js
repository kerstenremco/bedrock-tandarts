let itemsStore;
const endpoint =
  "https://rc6xprmcsuz3zejzlddcjrnsuu0kgrwy.lambda-url.us-east-1.on.aws/";

document.addEventListener("DOMContentLoaded", function (event) {
  const answer = document.getElementById("answer");
  const button = document.getElementById("button");
  const loading = document.getElementById("loading");
  const file = document.getElementById("file");

  button.addEventListener("click", async function () {
    loading.classList.remove("hidden");
    const image = await imageToBase64();
    fetch(endpoint, { method: "POST", body: JSON.stringify({ image }) }).then(
      (response) => {
        response.json().then((data) => {
          const items = data.items;
          itemsStore = items;
          const it = itemsStore.map((item) => `<li>${item}</li>`).join("");
          loading.classList.add("hidden");
          answer.innerHTML += getBubble(
            `Ik zie de volgende items: <ul>${it}</ul>`
          );
          answer.innerHTML += getBubble("Klopt dit?");
          answer.innerHTML += `<div class="badge badge-outline" onclick="getInfo()" id="yes">Ja</div>`;
          answer.innerHTML += `<div class="badge badge-outline" id="no">Nee</div>`;
        });
      }
    );
  });
});

function getBubble(text, type = "response") {
  let el = `<div class="chat chat-start"><div class="chat-bubble">TEXT</div></div>`;
  if (type == "question") el = el.replace("chat-start", "chat-end");
  return el.replace(/TEXT/g, text);
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

function getInfo() {
  document.getElementById("yes").remove();
  document.getElementById("no").remove();
  answer.innerHTML += getBubble("Ja", "question");
  for (let item of itemsStore) {
    fetch(endpoint, { method: "POST", body: JSON.stringify({ item }) }).then(
      (response) => {
        response.json().then((data) => {
          answer.innerHTML += getBubble(data.answer);
        });
      }
    );
  }
}
