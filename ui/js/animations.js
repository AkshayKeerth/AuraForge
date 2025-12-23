/**
 * Triggers intense visual feedback for high-tier pulls
 */
function triggerMegaWin(rarity) {
  const body = document.body;
  const display = document.getElementById("roll-result");

  // 1. Flash the entire background
  body.classList.add("glitch-bg");
  setTimeout(() => body.classList.remove("glitch-bg"), 1000);

  // 2. Screen Shake (Intense)
  display.style.animation = "shake 0.2s 5";

  // 3. Play Sound (If you add assets later)
  // let audio = new Audio('ui/assets/sounds/legendary.mp3');
  // audio.play();

  // 4. Log to a "Recent Pulls" feed if you have one
  console.log(
    `%c MEGA WIN: ${rarity} `,
    "background: #222; color: #ff00ff; font-size: 20px",
  );
}

/**
 * Utility for number rolling effect (Optional Juice)
 * Makes numbers count up quickly instead of jumping
 */
function animateValue(obj, start, end, duration) {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    obj.innerHTML = Math.floor(progress * (end - start) + start);
    if (progress < 1) {
      window.requestAnimationFrame(step);
    }
  };
  window.requestAnimationFrame(step);
}
