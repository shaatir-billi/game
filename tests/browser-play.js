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
  await move(1290);
  await jump("left");
  await jump("left");
  await jump("right");
  await move(1410);
  await jump("right");
  await move(1690);
  await jump("right");
  await move(2010);
  await jump("right");
  await move(3800);
  await page.clock.runFor(2000);
  await move(3150);
  for (let i = 0; i < 200; i++) {
    const s = await state();
    if (s.shopkeeper.x < s.player.x - 220 && s.shopkeeper.direction === -1)
      break;
    await page.clock.runFor(100);
  }
  await jump("right", true);
  await move(3450);
  await jump("right");
  await move(3550);
  await jump("left");
  await move(3370);
  await jump("left");
  await move(2940);
  await jump("left");
  await jump("right");
  await move(2170);
  await jump("left");
  await move(1850);
  await jump("left");
  await move(1610);
  await jump("left");
  await move(930);
  await jump("left");
  await move(0);
  const final = await state();
  if (final.state !== "won")
    throw new Error("Full browser play did not reach the win screen");
  return {
    logs,
    final,
    result: await page.locator("#result-title").innerText(),
  };
}
