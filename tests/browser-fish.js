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
    if (s.shopkeeper.x < s.player.x - 450 && s.shopkeeper.direction === -1)
      break;
    await page.clock.runFor(100);
  }
  await page.keyboard.press("e");
  await page.clock.runFor(40);
  const picked = await state();
  if (!picked.carrying) throw new Error("E pickup failed");
  await page.keyboard.press("q");
  await page.clock.runFor(40);
  if (!(await state()).carrying) throw new Error("Fish cooldown failed");
  await page.clock.runFor(600);
  await page.keyboard.press("q");
  await page.clock.runFor(40);
  const dropped = await state();
  if (dropped.carrying) throw new Error("Drop failed");
  await page.clock.runFor(650);
  const stayed = await state();
  if (stayed.fish.x !== dropped.fish.x || stayed.fish.y !== dropped.fish.y)
    throw new Error("Drop position changed");
  await page.keyboard.press("e");
  await page.clock.runFor(40);
  if (!(await state()).carrying) throw new Error("Dropped fish pickup failed");
  for (let i = 0; i < 100; i++) {
    if (!(await state()).carrying) break;
    await page.clock.runFor(100);
  }
  const caught = await state();
  if (
    caught.carrying ||
    caught.fish.x !== 3200 ||
    caught.player.health !== picked.player.health
  )
    throw new Error("Shopkeeper capture failed");
  return {
    picked: picked.carrying,
    dropped: { x: dropped.fish.x, y: dropped.fish.y },
    stayed: { x: stayed.fish.x, y: stayed.fish.y },
    caught: {
      carrying: caught.carrying,
      fishX: caught.fish.x,
      health: caught.player.health,
    },
  };
}
