import { cp, mkdir, rm } from "node:fs/promises";
await rm("public/assets", { recursive: true, force: true });
await mkdir("public/assets", { recursive: true });
const files = [
  "fonts/main.ttf",
  "menu/background.jpeg",
  "menu/3.png",
  "menu/heart_32x32.png",
  "menu/play_button_rect.png",
  "map/how_to_ply.jpg",
  "map/sky.jpeg",
  "map/ground2.png",
  "map/background2.png",
  "map/Fishbarrel2.png",
  "map/platform2.png",
  "map/platform3.png",
  "map/pointers",
  "sprites/player/sprite_sheet.png",
  "sprites/guard/Girl_walk.png",
  "sprites/shopkeeper/Man_walk.png",
  "sprites/shopkeeper/Man_idle.png",
  "sprites/fish/fish.png",
];
for (const path of files) {
  await mkdir(`public/assets/${path.split("/").slice(0, -1).join("/")}`, {
    recursive: true,
  });
  await cp(`../assets/${path}`, `public/assets/${path}`, { recursive: true });
}
