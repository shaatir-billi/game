import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import {
  Game,
  policyLogits,
  policyActions,
  platforms,
  wall,
  barrel,
  MAP_WIDTH,
} from "../web/game.js";
const policy = JSON.parse(
  readFileSync(new URL("../web/policy.json", import.meta.url)),
);
const fixtures = JSON.parse(
  readFileSync(new URL("./policy-fixtures.json", import.meta.url)),
);
const run = (game, frames, input = {}) => {
  for (let i = 0; i < frames; i++) game.tick(input);
};

test("PPO actor matches Python reference logits and produces valid actions", () => {
  for (const fixture of fixtures) {
    const logits = policyLogits(policy, fixture.observation);
    logits.forEach((value, i) =>
      assert.ok(Math.abs(value - fixture.logits[i]) < 1e-9),
    );
    for (const random of [() => 0, () => 0.5, () => 0.9999]) {
      const [shop, a, b] = policyActions(policy, fixture.observation, random);
      assert.ok(shop >= 0 && shop < 3 && a >= 0 && a < 2 && b >= 0 && b < 2);
    }
  }
});
test("player moves, jumps, lands, and stays inside the map", () => {
  const game = new Game(policy, () => 0.5),
    p = game.player;
  run(game, 10, { right: true });
  assert.equal(p.x, 150);
  game.tick({ jump: true });
  assert.ok(p.y < 690);
  run(game, 60);
  assert.equal(p.y, 690);
  assert.equal(p.grounded, true);
  run(game, 100, { left: true });
  assert.equal(p.x, 0);
  Object.assign(p, { x: MAP_WIDTH - 160, y: 690 });
  run(game, 10, { right: true });
  assert.equal(p.x, MAP_WIDTH - 160);
});
test("platform landing and wall collision use the real jump path", () => {
  const game = new Game(),
    p = game.player;
  Object.assign(p, { x: 1950, y: 690 });
  game.tick({ jump: true });
  run(game, 49);
  assert.equal(p.y + p.h, platforms[0].y);
  Object.assign(p, { x: wall.x - 160, y: 690, vx: 0, vy: 0, grounded: true });
  run(game, 30, { right: true });
  assert.equal(p.x, wall.x - 160);
});
test("fish pickup, persistent drop, cooldown, and shopkeeper recovery", () => {
  const game = new Game(),
    p = game.player;
  Object.assign(p, { x: 3150, y: 690 });
  game.tick({ fish: true });
  assert.equal(game.carrying, true);
  run(game, 31);
  game.tick({ fish: true });
  assert.equal(game.carrying, false);
  const dropped = { ...game.fish };
  run(game, 31);
  assert.deepEqual(game.fish, dropped);
  game.tick({ fish: true });
  assert.equal(game.carrying, true);
  Object.assign(game.shopkeeper, { x: p.x, y: p.y });
  game.tick();
  assert.equal(game.carrying, false);
  assert.equal(game.fish.x, 3200);
});
test("hidden player stays still and safe, then leaves the barrel", () => {
  const game = new Game(),
    p = game.player;
  Object.assign(p, { x: 1400, y: 420 });
  game.tick({ hide: true });
  assert.equal(p.hidden, true);
  const x = p.x;
  run(game, 31, { right: true, jump: true });
  assert.equal(p.x, x);
  assert.equal(p.health, 5);
  game.damage();
  assert.equal(p.health, 5);
  game.tick({ hide: true });
  assert.equal(p.hidden, false);
});
test("guards remove a life once per four seconds and reset restores the game", () => {
  const game = new Game(),
    p = game.player;
  Object.assign(p, { x: 1350, y: 420 });
  game.tick();
  assert.equal(p.health, 4);
  game.tick();
  assert.equal(p.health, 4);
  for (let i = 0; i < 4; i++) {
    p.invincible = 0;
    game.damage();
  }
  assert.equal(game.state, "lost");
  game.reset();
  assert.equal(game.state, "playing");
  assert.equal(game.player.health, 5);
  assert.equal(game.carrying, false);
});
test("barrel completes the game only when the player carries the fish", () => {
  const game = new Game(),
    p = game.player;
  Object.assign(p, { x: barrel.x, y: 50 });
  game.tick();
  assert.equal(game.state, "playing");
  game.carrying = true;
  game.tick();
  assert.equal(game.state, "won");
});
test("enemy speed stays bounded and the shopkeeper reaches the upper left through jumps", () => {
  const game = new Game(policy, () => 0.5),
    p = game.player;
  Object.assign(p, { x: 200, y: 50 });
  game.carrying = true;
  let jumped = false;
  for (let i = 0; i < 4000 && game.carrying; i++) {
    const before = { ...game.shopkeeper };
    game.tick();
    const s = game.shopkeeper;
    assert.ok(s.speed >= 3.5 - 1e-9 && s.speed <= 4.25 + 1e-9);
    if (game.carrying) {
      assert.ok(Math.abs(s.x - before.x) <= 4.25 + 1e-9);
      assert.ok(s.y - before.y >= -22 && s.y - before.y <= 15 + 1e-9);
      if (!s.grounded) jumped = true;
    }
  }
  assert.equal(jumped, true);
  assert.equal(game.carrying, false);
});

test("shopkeeper handles platform edges and centres from six starting surfaces", () => {
  const starts = [
    { x: 300, y: 850 },
    { x: 2782, y: 850 },
    { x: 3000, y: 150 },
    { x: 400, y: 210 },
    { x: 1600, y: 580 },
    { x: 1250, y: 500 },
  ];
  const targets = [
    { x: 200, y: 850, w: 1000 },
    { x: 2600, y: 850, w: 1400 },
    ...platforms,
  ];
  let cases = 0;
  for (const start of starts)
    for (const target of targets)
      for (const offset of [20, target.w / 2, target.w - 20]) {
        const game = new Game(policy, () => 0.5);
        Object.assign(game.player, {
          x: Math.max(0, target.x + offset - 80),
          y: target.y - 160,
          invincible: 10000,
        });
        Object.assign(game.shopkeeper, { x: start.x - 72, y: start.y - 144 });
        game.carrying = true;
        let steps = 0;
        while (game.carrying && game.state === "playing" && steps++ < 6000) {
          const oldGuards = game.guards.map((g) => g.x);
          game.tick();
          game.guards.forEach((guard, index) => {
            const platform = platforms[guard.platform];
            assert.ok(
              guard.x >= platform.x + 30 &&
                guard.x + guard.w <= platform.x + platform.w - 30,
            );
            assert.ok(Math.abs(guard.x - oldGuards[index]) <= 2 + 1e-9);
          });
        }
        assert.ok(
          !game.carrying || game.state === "won",
          `Shopkeeper stuck: start ${start.x},${start.y}; target ${target.x + offset},${target.y}`,
        );
        cases++;
      }
  assert.equal(cases, 450);
});

test("falling above the wall lands on its top without a sideways jump", () => {
  const game = new Game();
  Object.assign(game.player, { x: 2370, y: 120, vy: 10, grounded: false });
  run(game, 10);
  assert.equal(game.player.x, 2370);
  assert.equal(game.player.y + game.player.h, wall.y);
});

test("cat stands at platform edges and centres", () => {
  for (const platform of platforms)
    for (const offset of [20, platform.w / 2, platform.w - 20]) {
      const game = new Game();
      const x = Math.max(
        0,
        Math.min(MAP_WIDTH - 160, platform.x + offset - 80),
      );
      if (x < wall.x + wall.w && x + 160 > wall.x && platform.y > wall.y)
        continue;
      Object.assign(game.player, { x, y: platform.y - 160, invincible: 10000 });
      run(game, 20);
      assert.equal(game.player.y + game.player.h, platform.y);
      assert.equal(game.player.grounded, true);
      assert.equal(game.player.x, x);
    }
});
