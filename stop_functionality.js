// ═══════════════════════════════════════════════════════════════════
// 🛑 STOP FUNCTIONALITY - JavaScript complet
// ═══════════════════════════════════════════════════════════════════
// Copiază tot acest cod și adaugă-l ÎNAINTE de </script> în HTML
// ═══════════════════════════════════════════════════════════════════

const appStatusCache = new Map();
const STATUS_CHECK_INTERVAL = 5000; // 5 secunde - verificare automată

// ═══════════════════════════════════════════════════════════════════
// FUNCȚII CORE
// ═══════════════════════════════════════════════════════════════════

/**
 * Verifică status-ul unei aplicații (rulează sau nu)
 */
async function checkAppStatus(appKey) {
  try {
    const res = await fetch(`${SERVER}/status?app=${encodeURIComponent(appKey)}`, {
      cache: "no-store",
      method: "GET"
    });
    
    if (!res.ok) {
      console.warn(`Status check failed for ${appKey}: ${res.status}`);
      return { running: false };
    }
    
    const data = await res.json();
    return data;
  } catch (err) {
    console.error(`Status check error for ${appKey}:`, err);
    return { running: false };
  }
}

/**
 * Oprește (kill) o aplicație
 */
async function killApp(appKey, cardElement) {
  playSound("click");
  
  // Visual feedback - animație de loading
  cardElement.classList.add("launching");
  
  toast("⏳ Opresc aplicația...", "warn");
  
  try {
    const res = await fetch(`${SERVER}/kill?app=${encodeURIComponent(appKey)}`, {
      cache: "no-store",
      method: "GET"
    });
    
    const data = await res.json();
    
    if (data.ok) {
      // SUCCESS!
      playSound("success");
      toast(`🛑 ${appKey} oprit cu succes!`, "ok");
      
      // Update status imediat
      cardElement.classList.remove("running");
      appStatusCache.set(appKey, false);
      
      // Refresh status după 1 secundă pentru siguranță
      setTimeout(() => updateCardStatus(appKey, cardElement), 1000);
    } else {
      // EROARE de la server
      playSound("error");
      const errorMsg = data.error || 'Nu s-a putut opri aplicația';
      toast(`❌ Eroare: ${errorMsg}`, "error");
      console.error(`Kill failed for ${appKey}:`, data);
    }
  } catch (err) {
    // EROARE de comunicare
    playSound("error");
    toast(`❌ Eroare comunicare: ${err.message}`, "error");
    console.error(`Kill request error for ${appKey}:`, err);
  } finally {
    // Remove loading animation
    setTimeout(() => cardElement.classList.remove("launching"), 500);
  }
}

/**
 * Update status vizual pentru un card
 */
async function updateCardStatus(appKey, cardElement) {
  const status = await checkAppStatus(appKey);
  const wasRunning = appStatusCache.get(appKey);
  const isRunning = status.running;
  
  // Update cache
  appStatusCache.set(appKey, isRunning);
  
  // Update UI
  if (isRunning) {
    cardElement.classList.add("running");
  } else {
    cardElement.classList.remove("running");
  }
  
  // Log changes pentru debugging
  if (wasRunning !== isRunning) {
    const statusIcon = isRunning ? '🟢 RUNNING' : '🔴 STOPPED';
    console.log(`[Status Change] ${appKey}: ${statusIcon}`);
  }
}

/**
 * Verifică status pentru toate cardurile vizibile
 */
async function updateAllStatuses() {
  const cards = $$(".app-card").filter(c => c.style.display !== "none");
  
  // Pentru performance, verificăm doar primele 10 carduri vizibile
  // (dacă ai multe apps, nu vrei să verifici toate simultan)
  const visibleCards = cards.slice(0, 10);
  
  console.log(`[Status Monitor] Checking ${visibleCards.length} visible apps...`);
  
  for (const card of visibleCards) {
    const appKey = card.getAttribute("data-app");
    if (appKey) {
      await updateCardStatus(appKey, card);
    }
  }
}

/**
 * Setup event listeners pentru butoanele STOP
 */
function setupStopButtons() {
  const stopButtons = $$(".stop-btn");
  
  console.log(`[Stop Buttons] Setting up ${stopButtons.length} stop buttons...`);
  
  stopButtons.forEach(btn => {
    btn.addEventListener("click", (e) => {
      // IMPORTANT: Stop propagation ca să nu lansăm app-ul când dam click pe STOP!
      e.stopPropagation();
      
      const card = btn.closest(".app-card");
      const appKey = card.getAttribute("data-app");
      
      if (!appKey) {
        toast("⚠️ App key lipsește!", "error");
        console.error("Stop button clicked but no app key found");
        return;
      }
      
      // Apps importante - cere confirmare înainte de kill
      const confirmKillApps = ["code", "solidworks", "word", "excel", "cura", "easyeda"];
      
      if (confirmKillApps.includes(appKey)) {
        const appName = card.querySelector(".app-name")?.textContent || appKey;
        if (!confirm(`Sigur vrei să închizi ${appName}?\n\nLucrarea nesalvată se va pierde!`)) {
          playSound("click");
          return;
        }
      }
      
      // Kill app
      killApp(appKey, card);
    });
  });
  
  console.log(`[Stop Buttons] ✅ Setup complete`);
}

/**
 * Pornește monitorizarea automată de status
 */
function startStatusMonitoring() {
  // Check inițial după 2 secunde (după ce s-a încărcat totul)
  setTimeout(() => {
    console.log(`[Status Monitor] Starting initial check...`);
    updateAllStatuses();
  }, 2000);
  
  // Check periodic
  setInterval(() => {
    updateAllStatuses();
  }, STATUS_CHECK_INTERVAL);
  
  console.log(`[Status Monitor] ✅ Started (interval: ${STATUS_CHECK_INTERVAL / 1000}s)`);
}

// ═══════════════════════════════════════════════════════════════════
// INIT - ADAUGĂ ACESTEA ÎN FUNCȚIA init() EXISTENTĂ
// ═══════════════════════════════════════════════════════════════════

/*
Găsește funcția init() și adaugă la sfârșit:

function init(){
  loadPrefs();
  if(effectsEnabled){
    createParticles();
    createStars();
  }
  filter();
  startPingLoop();
  checkServerHealth();
  setLastLaunch("—");
  setTimeout(()=>searchInput.focus(), 100);
  toast("✨ Ready! V=view, E=effects, M=mute", "ok");
  
  // ⭐ NOU - STOP functionality
  setupStopButtons();
  startStatusMonitoring();
}
*/

// ═══════════════════════════════════════════════════════════════════
// FUNCȚII HELPER (OPTIONAL - pentru debugging)
// ═══════════════════════════════════════════════════════════════════

/**
 * Verifică manual status-ul unei aplicații (pentru debugging în console)
 * Folosire: await debugCheckStatus("code")
 */
async function debugCheckStatus(appKey) {
  console.log(`[Debug] Checking status for: ${appKey}`);
  const status = await checkAppStatus(appKey);
  console.log(`[Debug] Result:`, status);
  return status;
}

/**
 * Oprește manual o aplicație (pentru debugging în console)
 * Folosire: await debugKillApp("notepad")
 */
async function debugKillApp(appKey) {
  console.log(`[Debug] Killing: ${appKey}`);
  const card = $(`.app-card[data-app="${appKey}"]`);
  if (!card) {
    console.error(`[Debug] Card not found for: ${appKey}`);
    return;
  }
  await killApp(appKey, card);
}

/**
 * Force refresh all statuses (pentru debugging)
 * Folosire: debugRefreshAll()
 */
function debugRefreshAll() {
  console.log(`[Debug] Force refreshing all statuses...`);
  updateAllStatuses();
}

// ═══════════════════════════════════════════════════════════════════
// GATA! COPY-PASTE TOT CODUL DE MAI SUS ÎN HTML!
// ═══════════════════════════════════════════════════════════════════
