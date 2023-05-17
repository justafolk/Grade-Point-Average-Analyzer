window.step = 1;

document.addEventListener("DOMContentLoaded", function () {
  document.addEventListener(
    "click",
    function (event) {
      console.log("click");
      console.log(event.target, event.target.matches("#button"));
      var scr1 = document.getElementById("screen1");
      var scr2 = document.getElementById("screen2");
      var scr3 = document.getElementById("screen3");
      var dot1 = document.getElementById("dot1");
      var dot2 = document.getElementById("dot2");
      var dot3 = document.getElementById("dot3");

      // If the clicked element doesn't have the right selector, bail
      if (!event.target.matches("#button")) return;

      event.preventDefault();
      if (step === 1) {
        scr1.classList.remove("is-active");
        dot1.classList.remove("is-active");
        scr2.classList.add("is-active");
        dot2.classList.add("is-active");
        scr3.classList.remove("is-active");
        dot3.classList.remove("is-active");
        window.step = 2;
      } else if (step === 2) {
        scr1.classList.remove("is-active");
        dot1.classList.remove("is-active");
        scr2.classList.remove("is-active");
        dot2.classList.remove("is-active");
        scr3.classList.add("is-active");
        dot3.classList.add("is-active");
        window.step = 3;
      } else if (step === 3) {
        scr1.classList.add("is-active");
        dot1.classList.add("is-active");
        scr2.classList.remove("is-active");
        dot2.classList.remove("is-active");
        scr3.classList.remove("is-active");
        dot3.classList.remove("is-active");
        window.step = 1;
      }
    },
    false
  );
});
