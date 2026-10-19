/* Live Valorant rank for the lobby page.
   Reads rank.json (written by the GitHub Action) and updates the nav player card
   and the "You're with" card on the loading screen. If rank.json is missing or
   broken, the page keeps its hard-coded rank. */
(async function () {
  const ROMAN = { 1: "I", 2: "II", 3: "III" };
  let r;
  try {
    const res = await fetch("rank.json", { cache: "no-store" });
    if (!res.ok) return;
    r = await res.json();
  } catch (e) { return; }
  if (!r || !r.tier) return;

  const tier = r.tier.replace(/\s(\d)$/, (_, d) => " " + (ROMAN[d] || d)); // "Ascendant 2" -> "Ascendant II"
  const full = tier + (r.rr != null ? ` · ${r.rr} RR` : "");

  const nav = document.querySelector(".me .who .label");
  if (nav) {
    nav.textContent = full;
    nav.classList.add("live");
    nav.title = `${r.tag} · live rank, updated ${new Date(r.updated).toLocaleString()}`;
  }

  // The loading screen rebuilds its team cards on every visit, so patch them each time.
  const team = document.getElementById("team");
  if (team) {
    new MutationObserver(() => {
      const l = team.querySelector(".mate.me2 .label:last-child");
      if (l && l.textContent !== tier) l.textContent = tier;
    }).observe(team, { childList: true });
  }
})();
