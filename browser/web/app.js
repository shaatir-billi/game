import {
  Game,
  WIDTH,
  HEIGHT,
  platforms,
  wall,
  hidingSpots,
  barrel,
} from "./game.js";
import policy from "./policy.json";
const canvas = document.querySelector("#game"),
  ctx = canvas.getContext("2d");
const $ = (id) => document.getElementById(id);
const images = {},
  held = new Set(),
  queued = new Set();
let game = new Game(policy),
  screen = "menu",
  last = 0,
  accumulator = 0;
const files = {
  menu: "menu/background.jpeg",
  sky: "map/sky.jpeg",
  ground: "map/ground2.png",
  background: "map/background2.png",
  platform2: "map/platform2.png",
  platform3: "map/platform3.png",
  barrel: "map/Fishbarrel2.png",
  hide: "menu/3.png",
  heart: "menu/heart_32x32.png",
  player: "sprites/player/sprite_sheet.png",
  guard: "sprites/guard/Girl_walk.png",
  shopkeeper: "sprites/shopkeeper/Man_walk.png",
  shopkeeperIdle: "sprites/shopkeeper/Man_idle.png",
  fish: "sprites/fish/fish.png",
  right: "map/pointers/1.png",
  left: "map/pointers/2.png",
  upRight: "map/pointers/3.png",
  upLeft: "map/pointers/4.png",
};
let suspended = false;
let menuTime = 0,
  menuScroll = 0,
  menuAction = "stop",
  nextMenuAction = 0;
const menuCat = { x: 800, y: 750, w: 160, h: 160, facing: 1 };
function show(next) {
  screen = next;
  if (next === "menu") {
    menuTime = 0;
    menuScroll = 0;
    menuAction = "stop";
    nextMenuAction = 60;
    Object.assign(menuCat, { x: 800, y: 750, facing: 1 });
  }
  held.clear();
  queued.clear();
  accumulator = 0;
  for (const id of ["menu", "instructions", "result"])
    $(id).hidden = id !== next;
  if (next === "playing") {
    suspended = false;
    canvas.focus({ preventScroll: true });
  }
}
function start() {
  game.reset();
  show("playing");
}
function quit() {
  show("quit");
}
$("play").onclick = start;
$("again").onclick = start;
$("quit").onclick = quit;
$("help").onclick = () => show("instructions");
$("help-back").onclick = () => show("menu");
$("result-menu").onclick = () =>
  game.state === "lost" ? quit() : show("menu");
const keyMap = {
  KeyA: "left",
  ArrowLeft: "left",
  KeyD: "right",
  ArrowRight: "right",
  KeyW: "jump",
  ArrowUp: "jump",
  Space: "jump",
  KeyE: "hide",
  KeyQ: "fish",
};
addEventListener("keydown", (event) => {
  const action = keyMap[event.code];
  if (action && screen === "playing") {
    event.preventDefault();
    if (action === "hide" || action === "fish") {
      if (!event.repeat) queued.add(action);
    } else {
      held.add(action);
      if (action === "jump" && !event.repeat) queued.add("jump");
    }
  }
});
addEventListener("keyup", (event) => held.delete(keyMap[event.code]));
function pauseForBlur() {
  held.clear();
  queued.clear();
  suspended = true;
}
addEventListener("blur", pauseForBlur);
addEventListener("focus", () => {
  suspended = false;
  accumulator = 0;
  last = performance.now();
});
document.addEventListener("visibilitychange", () => {
  if (document.hidden) pauseForBlur();
  else {
    suspended = false;
    last = performance.now();
  }
});
function image(name, x, y, w, h) {
  if (images[name]) ctx.drawImage(images[name], x, y, w, h);
}
function sprite(name, actor, row = 0, animate = true, time = game.time) {
  const source = images[name];
  if (!source) return;
  const size = name === "player" ? 32 : 48;
  const count = source.width / size,
    frame = animate ? Math.floor(time * 0.15) % count : 0;
  ctx.save();
  ctx.translate(
    actor.x - game.camera + (actor.facing < 0 ? actor.w : 0),
    actor.y,
  );
  if (actor.facing < 0) ctx.scale(-1, 1);
  ctx.drawImage(
    source,
    frame * size,
    row * size,
    size,
    size,
    0,
    0,
    actor.w,
    actor.h,
  );
  ctx.restore();
}
function draw() {
  ctx.imageSmoothingEnabled = false;
  if (screen === "instructions") return;
  if (screen === "quit") {
    ctx.fillStyle = "#000";
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    return;
  }
  if (screen === "menu") {
    image("menu", -menuScroll, 0, WIDTH, HEIGHT);
    image("menu", WIDTH - menuScroll, 0, WIDTH, HEIGHT);
    const camera = game.camera;
    game.camera = 0;
    sprite(
      "player",
      menuCat,
      menuAction === "left" ? 5 : menuAction === "right" ? 4 : 0,
      menuAction !== "stop",
      menuTime,
    );
    game.camera = camera;
    return;
  }
  ctx.fillStyle = "#2774dc";
  ctx.fillRect(0, 0, WIDTH, HEIGHT);
  for (let x = 0; x < 4000; x += WIDTH) {
    image("sky", x - game.camera, 0, WIDTH, HEIGHT);
    image("ground", x - game.camera, 0, WIDTH, HEIGHT);
  }
  if (images.background)
    image(
      "background",
      -game.camera,
      0,
      images.background.width * 3.55,
      images.background.height * 3.55,
    );
  for (const platform of [...platforms, wall])
    image(
      `platform${platform.tile}`,
      platform.x - game.camera,
      platform.y,
      platform.w,
      platform.h,
    );
  for (const guard of game.guards) sprite("guard", guard);
  sprite(
    Math.abs(game.shopkeeper.vx) > 0.1 ? "shopkeeper" : "shopkeeperIdle",
    game.shopkeeper,
  );
  for (const spot of hidingSpots)
    image("hide", spot.x - game.camera, spot.y, spot.w, spot.h);
  image("barrel", barrel.x - game.camera, barrel.y, barrel.w, barrel.h);
  const fish = game.fish;
  if (!game.carrying && images.fish)
    ctx.drawImage(
      images.fish,
      0,
      0,
      260,
      110,
      fish.x - game.camera,
      fish.y,
      fish.w,
      fish.h,
    );
  const p = game.player;
  if (!p.hidden && (!p.invincible || Math.floor(game.time / 12) % 2 === 0))
    sprite("player", p, !p.grounded ? 8 : p.vx ? 5 : 0, !!p.vx || !p.grounded);
  ctx.font = "24px system-ui";
  ctx.fillStyle = "#fff";
  ctx.textAlign = "center";
  if (game.carrying)
    ctx.fillText("Fish picked up", p.x + p.w / 2 - game.camera, p.y + p.h + 12);
  if (p.hidden) {
    const spot = hidingSpots.find((s) => p.x < s.x + s.w && p.x + p.w > s.x);
    if (spot)
      ctx.fillText("Hidden!", spot.x + spot.w / 2 - game.camera, spot.y - 20);
  }
  for (let i = 0; i < p.health; i++) image("heart", 20 + i * 30, 20, 32, 32);
  ctx.font = "20px Game,monospace";
  ctx.fillStyle = "#000";
  ctx.textAlign = "left";
  ctx.fillText(`${p.health} lives left`, 20, 80);
  const pointers = {
    right: [
      [200, 820],
      [1400, 820],
      [2850, 100],
    ],
    upRight: [
      [1800, 820],
      [2050, 170],
      [1450, 250],
    ],
    upLeft: [
      [2200, 660],
      [1000, 250],
    ],
    left: [
      [1750, 530],
      [2810, 100],
    ],
  };
  for (const [name, points] of Object.entries(pointers))
    for (const [x, y] of points) image(name, x - game.camera, y, 40, 50);
}
function frame(now) {
  const elapsed = Math.min(now - last || 0, 100);
  accumulator += elapsed;
  last = now;
  if (screen === "menu" && !suspended) {
    menuTime += (elapsed * 60) / 1000;
    menuScroll = (menuScroll + (elapsed * 120) / 1000) % WIDTH;
    if (menuTime >= nextMenuAction) {
      menuAction = ["left", "right", "stop", "stop"][
        Math.floor(Math.random() * 4)
      ];
      nextMenuAction = menuTime + 60;
    }
    const dx = menuAction === "left" ? -2 : menuAction === "right" ? 2 : 0;
    menuCat.x = Math.max(
      0,
      Math.min(WIDTH - menuCat.w, menuCat.x + (dx * elapsed * 60) / 1000),
    );
    if (dx) menuCat.facing = Math.sign(dx);
  }
  if (screen === "playing" && !suspended) {
    while (accumulator >= 1000 / 60) {
      game.tick({
        left: held.has("left"),
        right: held.has("right"),
        jump: held.has("jump") || queued.has("jump"),
        hide: queued.has("hide"),
        fish: queued.has("fish"),
      });
      queued.clear();
      accumulator -= 1000 / 60;
      if (game.state !== "playing") {
        const lost = game.state === "lost";
        $("result").classList.toggle("lost", lost);
        $("result-title").textContent = lost ? "Game Over" : "Game Finished!";
        $("again").textContent = lost ? "TRY AGAIN" : "Play Again";
        $("result-menu").textContent = lost ? "QUIT" : "Main Menu";
        show("result");
        break;
      }
    }
    canvas.setAttribute(
      "aria-label",
      `Shaatir Billi game. ${game.player.health} lives.`,
    );
  } else accumulator = 0;
  draw();
  requestAnimationFrame(frame);
}
async function load() {
  try {
    await Promise.all(
      Object.entries(files).map(
        ([name, path]) =>
          new Promise((resolve, reject) => {
            const asset = new Image();
            asset.onload = () => {
              images[name] = asset;
              resolve();
            };
            asset.onerror = () => reject(new Error(`Asset failed: ${path}`));
            asset.src = `/assets/${path}`;
          }),
      ),
    );
    $("load").hidden = true;
    $("play").disabled = false;
    show("menu");
    requestAnimationFrame(frame);
  } catch (error) {
    $("load").textContent = "Load failed. Reload to try again.";
    console.error(error);
  }
}
load();
