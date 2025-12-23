// Global state
let isLoggedIn = false;

// UNIVERSAL BRIDGE: Detects if we are on Desktop or Web Browser
async function callPython(functionName, args = {}) {
  if (window.pywebview && window.pywebview.api) {
    const func = pywebview.api[functionName];
    // Special case for login/signup which take 2 arguments in Python
    if (functionName === "login" || functionName === "signup") {
      return await func(args.username, args.password);
    }
    return await func();
  } else {
    // WEB BROWSER MODE
    const routeMap = {
      login: "/api/login",
      signup: "/api/signup",
      get_sync_data: "/api/sync",
      roll_item: "/api/roll",
    };

    const method = functionName === "get_sync_data" ? "GET" : "POST";
    const options = {
      method: method,
      headers: { "Content-Type": "application/json" },
    };
    if (method === "POST") options.body = JSON.stringify(args);

    try {
      const response = await fetch(routeMap[functionName], options);
      if (!response.ok) throw new Error("Network response was not ok");
      return await response.json();
    } catch (err) {
      console.error("Web Bridge Error:", err);
      // We only return an error if it's NOT a background sync
      if (functionName !== "get_sync_data") {
        return {
          status: "error",
          message: "Server connection lost. Please try again.",
        };
      }
      return null;
    }
  }
}

window.addEventListener("pywebviewready", () => {
  console.log("Aura Forge Desktop Mode Online");
});

async function handleAuth(type) {
  const u = document.getElementById("user-input").value;
  const p = document.getElementById("pass-input").value;

  // Use the Universal Bridge
  const response = await callPython(type, { username: u, password: p });

  if (response && response.status === "success") {
    isLoggedIn = true;
    document.getElementById("login-overlay").style.display = "none";
    document.getElementById("display-username").innerText = response.username;
    // START THE AUTO-UPDATE LOOP
    setInterval(pollSync, 1000);
  } else {
    alert(response ? response.message : "Authentication Failed");
  }
}

async function pollSync() {
  if (!isLoggedIn) return;

  const data = await callPython("get_sync_data");
  if (data && data.balance !== undefined) {
    document.getElementById("balance-display").innerText =
      `$${data.balance.toFixed(2)}`;
    document.getElementById("display-username").innerText = data.username;
  }
}

async function startRoll() {
  const btn = document.getElementById("roll-btn");
  const display = document.getElementById("roll-result");

  btn.disabled = true;

  // Animation Juice & Reflow
  display.classList.remove("shake-animation");
  void display.offsetWidth;
  display.classList.add("shake-animation");
  display.innerHTML = "FORGING...";

  const response = await callPython("roll_item");
  btn.disabled = false;
  display.classList.remove("shake-animation");

  if (response && response.status === "success") {
    updateRollDisplay(response.item);
  } else {
    alert(response ? response.message : "Roll failed");
    display.innerHTML = "READY TO FORGE";
  }
}

function updateRollDisplay(item) {
  const display = document.getElementById("roll-result");
  display.className = `tier-${item.rarity.toLowerCase()}`;
  display.innerHTML = `<div><small>${item.rarity.toUpperCase()}</small><h2>${item.name}</h2></div>`;

  if (item.rarity === "Mythic" || item.rarity === "Legendary") {
    if (typeof triggerMegaWin === "function") {
      triggerMegaWin(item.rarity);
    }
  }
}
