<span></span>

<style>
  span {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: block;
    margin: 10px auto;
    position: relative;
    background: #fff;
    box-shadow:
      -16px 0 #fff,
      16px 0 #fff;
    box-sizing: border-box;
    animation: shadowPulse 2s linear infinite;
  }

  @keyframes shadowPulse {
    33% {
      background: #fff;
      box-shadow:
        -16px 0 #35bcaa,
        16px 0 #fff;
    }
    66% {
      background: #35bcaa;
      box-shadow:
        -16px 0 #fff,
        16px 0 #fff;
    }
    100% {
      background: #fff;
      box-shadow:
        -16px 0 #fff,
        16px 0 #35bcaa;
    }
  }
</style>
