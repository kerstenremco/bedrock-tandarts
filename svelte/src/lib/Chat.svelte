<script>
  let loading = false;
  let input;
  export let uid;
  import { BubbleChatUploadIcon } from "hugeicons-svelte";
  import Pulse from "./ui/Pulse.svelte";
  let messages = [
    {
      type: "assistant",
      message: "Hoe kan ik je helpen met je factuur?",
    },
  ];
  function scrollChatBox() {
    setTimeout(() => {
      document.getElementById("chat").scrollTop =
        document.getElementById("chat").scrollHeight;
    }, 10);
  }
  async function handleMessage() {
    const message = input.value.trim();
    if (!message) return;
    loading = true;
    messages = [...messages, { type: "user", message }];
    input.value = "";

    try {
      scrollChatBox();
      const r = await fetch(
        "https://phgke4ycy7pvlu4xia4dad47e40kuwrc.lambda-url.eu-central-1.on.aws",
        {
          method: "POST",
          body: JSON.stringify({ uid, question: message }),
        }
      );
      const j = await r.json();
      if (j.error) {
        throw new Error(j.error);
      } else {
        messages = [...messages, { type: "assistant", message: j.body }];
      }
    } catch (e) {
      messages = [
        ...messages,
        {
          type: "assistant",
          message: "Er ging iets mis... Wil je de vraag nogmaals stellen?",
        },
      ];
      console.error(e);
    } finally {
      loading = false;
      scrollChatBox();
      console.log(input);
      input.focus();
    }
  }
</script>

<div class="chat-screen">
  <div class="chat" id="chat">
    {#each messages as { type, message }, i}
      <div class="{type} messages">
        <div class="message last">
          {message}
        </div>
      </div>
    {/each}
    {#if loading}
      <div class="assistant messages">
        <div class="message last loader"><Pulse /></div>
      </div>
    {/if}
  </div>
  <div id="input">
    <input
      type="text"
      id="question"
      placeholder="Typ hier je bericht"
      disabled={loading}
      bind:this={input}
      on:keydown={(e) => e.key === "Enter" && handleMessage()}
    />
    <span id="send"><BubbleChatUploadIcon color="#f1f4f3" size="20" /></span>
  </div>
</div>

<style>
  #send {
    background-color: #35bcaa;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    padding: 5px;
  }
  #send:hover {
    cursor: pointer;
    background-color: #2c9183;
  }
  #input {
    width: 100%;
    display: flex;
    gap: 10px;
    align-items: center;
  }
  #question {
    flex: 1;
    border-radius: 10px;
    padding: 7px;
    border: 2px solid #ccd8d7;
  }
  #question:focus {
    outline: none;
    border-color: #35bcaa;
  }
  .loader {
    min-width: 100px;
  }

  .chat-screen {
    display: flex;
    height: 100%;
    flex-direction: column;
  }
  .chat {
    display: flex;
    flex-direction: column;
    flex: 1;
    overflow-y: scroll;
    overflow-x: hidden;
    padding-right: 10px;
    margin-bottom: 20px;
  }

  @media (max-width: 1020px) {
    .chat::-webkit-scrollbar {
      width: 0px;
    }
  }

  .chat::-webkit-scrollbar-track {
    background-color: #e4e4e4;
    border-radius: 100px;
  }

  .chat::-webkit-scrollbar-thumb {
    border-radius: 100px;
    border: 2px solid transparent;
    background-clip: content-box;
    background-color: #35bcaa;
  }

  .messages {
    margin-top: 30px;
    display: flex;
    flex-direction: column;
  }

  .message {
    border-radius: 20px;
    padding: 8px 15px;
    margin-top: 5px;
    margin-bottom: 5px;
    display: inline-block;
  }

  .assistant {
    align-items: flex-start;
  }

  .assistant .message {
    margin-right: 25%;
    background-color: #eee;
    position: relative;
  }

  .assistant .message.last:before {
    content: "";
    position: absolute;
    z-index: 0;
    bottom: 0;
    left: -7px;
    height: 20px;
    width: 20px;
    background: #eee;
    border-bottom-right-radius: 15px;
  }
  .assistant .message.last:after {
    content: "";
    position: absolute;
    z-index: 1;
    bottom: 0;
    left: -10px;
    width: 10px;
    height: 20px;
    background: white;
    border-bottom-right-radius: 10px;
  }

  .user {
    align-items: flex-end;
  }

  .user .message {
    color: white;
    margin-left: 25%;
    background: linear-gradient(to bottom, #35bcaa 0%, #35bcaa 100%);
    background-attachment: fixed;
    position: relative;
  }

  .user .message.last:before {
    content: "";
    position: absolute;
    z-index: 0;
    bottom: 0;
    right: -8px;
    height: 20px;
    width: 20px;
    background: linear-gradient(to bottom, #35bcaa 0%, #35bcaa 100%);
    background-attachment: fixed;
    border-bottom-left-radius: 15px;
  }

  .user .message.last:after {
    content: "";
    position: absolute;
    z-index: 1;
    bottom: 0;
    right: -10px;
    width: 10px;
    height: 20px;
    background: white;
    border-bottom-left-radius: 10px;
  }
</style>
