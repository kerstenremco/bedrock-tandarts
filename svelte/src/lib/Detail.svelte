<script>
  export let items;
  import Button from "./ui/Button.svelte";
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();
</script>

<div>
  <p>Ik zal proberen je factuur uit te leggen:</p>
  <div class="items">
    <ul>
      {#each items as item}
        <li>{item.description}<br /><span>{item.explanation}</span></li>
      {/each}
    </ul>
  </div>
  <div class="btns">
    <Button on:click={() => dispatch("chat")}>Chatten</Button>
  </div>
</div>

<style>
  div:first-child {
    height: 100%;
    display: flex;
    flex-direction: column;
  }
  .items {
    overflow-y: scroll;
    flex: 1;
  }
  p {
    font-size: 16px;
    text-align: center;
    margin: 10px 0;
  }
  .btns {
    display: flex;
    justify-content: center;
    gap: 10px;
  }
  li {
    font-weight: bold;
    margin-bottom: 15px;
  }
  li span {
    font-weight: normal;
  }
</style>
