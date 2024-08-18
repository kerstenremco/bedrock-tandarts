<script>
  import Items from "./lib/Items.svelte";
  import Upload from "./lib/Upload.svelte";
  import Chat from "./lib/Chat.svelte";
  import logo from "./assets/bot.jpg";
  import Detail from "./lib/Detail.svelte";
  let screen = "upload";
  let uid;
  let items;
  $: introNeededClass =
    screen === "upload" || screen === "result"
      ? "intro-needed"
      : "intro-not-needed";
  function handleReset() {
    screen = "upload";
  }
  function handleUploaded(e) {
    items = e.detail;
    screen = "result";
  }
  function handleConfirmed(e) {
    items = e.detail;
    screen = "detail";
  }
  function handleStartChat() {
    screen = "chat";
  }
</script>

<main>
  <div id="screen">
    <div class="intro {introNeededClass}">
      <p>
        Hi, mijn naam is DentiBot!
        <span
          >Ik ben hier om vragen over je tandartsfactuur te beantwoorden.</span
        >
      </p>
      <img alt="DenitBot" height="300" src={logo} />
    </div>
    <div class="content">
      {#if screen === "upload"}
        <Upload on:uploaded={handleUploaded} on:uid={(e) => (uid = e.detail)} />
      {:else if screen === "result"}
        <Items
          {items}
          {uid}
          on:confirmed={handleConfirmed}
          on:reset={handleReset}
        />
      {:else if screen === "detail"}
        <Detail {items} on:chat={handleStartChat} />
      {:else if screen === "chat"}
        <Chat {uid} />
      {/if}
    </div>
  </div>
</main>

<style>
  main {
    background-color: lightblue;
    display: flex;
    width: 100vw;
    height: 100vh;
    justify-content: center;
    align-items: center;
  }
  #screen {
    background-color: white;
    width: 50%;
    min-width: 800px;
    max-width: 920px;
    height: 50%;
    min-height: 520px;
    border-radius: 2%;

    display: flex;
    align-items: stretch;
    padding: 20px;
  }
  @media (max-width: 1020px) {
    main {
      height: calc(100vh - 80px);
    }
    #screen {
      flex-direction: column;
      height: 100%;
      width: 100%;
      min-width: auto;
      max-width: auto;
      border-radius: 0;
    }
    .intro {
      flex-basis: auto;
    }
    .intro.intro-not-needed {
      display: none;
    }
    #screen > div:last-child {
      flex-basis: 0%;
      flex-grow: 1;
      align-items: stretch;
    }
    img {
      height: 140px;
    }
  }
  .intro,
  .content {
    overflow: hidden;
    flex-basis: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .intro > p {
    font-size: 22px;
    margin: 20px 0 10px 0;
    text-align: center;
  }
  .intro > p > span {
    font-size: 18px;
    display: inline-block;
    margin-top: 10px;
  }
</style>
