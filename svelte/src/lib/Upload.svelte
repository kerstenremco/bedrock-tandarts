<script>
  import { CloudUploadIcon } from "hugeicons-svelte";
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();
  import Button from "./ui/Button.svelte";
  import Spinner from "./ui/Spinner.svelte";
  import Message from "./ui/Message.svelte";
  let dragBackground = "transparent";
  let wait = false;
  let message = undefined;

  async function convertImage(image) {
    return new Promise((resolve, reject) => {
      const fileReader = new FileReader();
      fileReader.onload = (x) => {
        resolve(x.target.result.split("base64,")[1]);
      };
      fileReader.readAsDataURL(image);
    });
  }
  async function handleFile(e) {
    let file;
    if (e.type === "change") {
      file = document.getElementById("file").files[0];
    } else if (e.type === "drop") {
      e.preventDefault();
      dragBackground = "transparent";
      file = e.dataTransfer.files[0];
      if (!file.type.includes("image") && file.type !== "application/pdf") {
        message = "Alleen afbeeldingen en PDF bestanden zijn toegestaan!";
        return;
      }
    } else {
      return;
    }
    if (!file) return;
    message = undefined;
    wait = true;
    const base64 = await convertImage(file);
    try {
      const response = await fetch(
        "https://phgke4ycy7pvlu4xia4dad47e40kuwrc.lambda-url.eu-central-1.on.aws/",
        { method: "POST", body: JSON.stringify({ image: base64 }) }
      );
      const json = await response.json();
      wait = false;
      if (json.error) {
        message =
          json.error === "NOT_AN_DENTAL_INVOICE"
            ? "Ik heb je factuur nagekeken, maar dit lijkt geen factuur van een tandarts."
            : json.error === "NOT_AN_INVOICE"
              ? "Volgens mij is dit geen factuur, ik kan hem in ieder geval niet lezen. Probeer een andere afbeelding"
              : "Kan de factuur niet laden. Probeer een andere afbeelding.";
      } else {
        dispatch("uid", json.uid);
        dispatch("uploaded", json.body);
      }
    } catch (e) {
      wait = false;
      message = "Er is iets misgegaan. Probeer het later nog eens.";
    }
  }

  function handleDragEvent(e) {
    e.preventDefault();
    dragBackground = e.type === "dragleave" ? "transparent" : "#ddecf1";
  }
</script>

{#if message}
  <Message>{message}</Message>
{/if}
<div
  id="drop_zone"
  role="input"
  style="background-color: {dragBackground}"
  on:drop={(e) => handleFile(e)}
  on:dragenter={handleDragEvent}
  on:dragleave={handleDragEvent}
  on:dragover={handleDragEvent}
>
  {#if wait}
    <Spinner />
  {:else}
    <CloudUploadIcon size="80" color="#58F1DD" />
    <input
      type="file"
      id="file"
      accept="image/*, .pdf"
      on:change={handleFile}
      hidden
    />
    <p>Drop hier je factuur<br />of</p>
    <Button on:click={() => document.getElementById("file").click()}
      >Upload</Button
    >
  {/if}
</div>

<style>
  #drop_zone {
    height: 100%;
    width: 100%;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  #drop_zone p {
    font-size: 18px;
    margin-top: 10px;
    text-align: center;
    margin-top: 30px;
    margin-bottom: 10px;
  }
</style>
