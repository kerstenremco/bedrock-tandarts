<script>
  export let style = "default";
</script>

<button on:click class={style}><slot /></button>

<style>
  button {
    border: none;
    border-radius: 10px;
    padding: 5px 40px;
    font-size: 20px;
  }
  button:hover {
    cursor: pointer;
  }
  button.default {
    color: #151717;
    background-color: #58f1dd;
  }
  button.default:hover {
    background-color: #35bcaa;
  }
  button.danger {
    background-color: rgb(213, 97, 97);
    color: rgb(246, 230, 230);
  }
  button.danger:hover {
    background-color: rgb(188, 53, 53);
  }
</style>
