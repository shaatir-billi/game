async (page) => {
  await page.clock.install();
  await page.goto("https://shaatirbilli.mhadi.dev/?verify");
  await page.locator("#play").click();
  const state = () => page.evaluate(() => window.__gameState);
  const logs = [];
  async function move(target) {
    for (let attempt = 0; attempt < 10; attempt++) {
      const s = await state();
      if (s.state === "won") break;
      const gap = target - s.player.x;
      if (Math.abs(gap) < 5) break;
      const key = gap < 0 ? "a" : "d";
      await page.keyboard.down(key);
      await page.clock.runFor(
        Math.max(16, (Math.floor(Math.abs(gap) / 5) * 1000) / 60),
      );
      await page.keyboard.up(key);
      await page.clock.runFor(18);
    }
    const s = await state();
    logs.push([
      "move",
      target,
      s.player.x,
      s.player.y,
      s.player.health,
      s.carrying,
    ]);
  }
  async function jump(direction, fish = false) {
    const key = direction === "left" ? "a" : "d";
    await page.keyboard.down(key);
    if (fish) await page.keyboard.press("q");
    await page.keyboard.down("w");
    await page.clock.runFor(36);
    await page.keyboard.up("w");
    for (let i = 0; i < 100; i++) {
      const s = await state();
      if (s.player.grounded || s.state !== "playing") break;
      await page.clock.runFor(16);
    }
    await page.keyboard.up(key);
    await page.clock.runFor(18);
    const s = await state();
    logs.push([
      "jump",
      direction,
      s.player.x,
      s.player.y,
      s.player.health,
      s.carrying,
    ]);
  }
  await move(2010);
  await jump("right");
  await move(2130);
  await jump("left");
  await move(1410);
  await page.keyboard.press("e");
  await page.clock.runFor(40);
  const hidden = await state();
  if (!hidden.player.hidden) throw new Error("Hide failed");
  await page.keyboard.down("d");
  await page.keyboard.down("w");
  await page.clock.runFor(5000);
  await page.keyboard.up("d");
  await page.keyboard.up("w");
  const safe = await state();
  if (
    safe.player.x !== hidden.player.x ||
    safe.player.health !== hidden.player.health
  )
    throw new Error("Hidden player moved or took damage");
  await page.keyboard.press("e");
  await page.clock.runFor(40);
  if ((await state()).player.hidden) throw new Error("Unhide failed");
  for(let i=0;i<90 && (await state()).state==='playing';i++) await page.clock.runFor(1000);
  const lost = await state();
  if (lost.state !== "lost")
    throw new Error("Guard contact did not reach game over");
  await page.locator("#again").click();
  await page.clock.runFor(40);
  const restarted = await state();
  if (
    restarted.player.health !== 5 ||
    restarted.player.x !== 100 ||
    restarted.state !== "playing"
  )
    throw new Error("Restart failed");
  return {
    hidden: { x: hidden.player.x, health: hidden.player.health },
    safe: { x: safe.player.x, health: safe.player.health },
    lost: lost.state,
    restarted: {
      x: restarted.player.x,
      health: restarted.player.health,
      state: restarted.state,
    },
  };
}
