<script>
  export let items;
  export let uid;
  let wait = false;
  import Button from "./ui/Button.svelte";
  import { createEventDispatcher } from "svelte";
  import Spinner from "./ui/Spinner.svelte";
  const dispatch = createEventDispatcher();

  async function conformation(confirmed) {
    wait = true;
    try {
      const response = await fetch(
        "https://phgke4ycy7pvlu4xia4dad47e40kuwrc.lambda-url.eu-central-1.on.aws/",
        {
          method: "POST",
          body: JSON.stringify({ uid, confirmed }),
        }
      );
      if (!confirmed) {
        dispatch("reset");
        return;
      }
      const json = await response.json();
      wait = false;
      if (json.error) {
        console.error(json.error);
      } else {
        dispatch("confirmed", json.body);
      }
    } catch (e) {
      wait = false;
      console.error(e);
    }
  }
</script>

{#if wait}
  <Spinner />
{:else}
  <div>
    <p>Ik zie de volgende items:</p>
    <div class="items">
      <ul>
        {#each items as item}
          <li>{item.description}</li>
          {#if item.explanation}
            <li>-----{item.explanation}</li>
          {/if}
        {/each}
      </ul>
    </div>
    <p>Klopt dit?</p>
    <div class="btns">
      <Button on:click={() => conformation(true)}>Ja</Button>
      <Button style="danger" on:click={() => conformation(false)}>Nee</Button>
    </div>
  </div>
{/if}

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
</style>
