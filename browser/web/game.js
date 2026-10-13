export const WIDTH = 1600,
  HEIGHT = 900,
  MAP_WIDTH = 4000,
  GROUND = 850;
export const platforms = [
  [2000, 820, 100, 20, 2],
  [2100, 770, 100, 20, 2],
  [2200, 710, 100, 20, 2],
  [1200, 500, 100, 20, 2],
  [1200, 500, 100, 20, 2],
  [3600, 750, 100, 20, 3],
  [2300, 600, 200, 20, 2],
  [1600, 220, 200, 20, 2],
  [1900, 220, 200, 20, 2],
  [2700, 300, 200, 20, 3],
  [2580, 750, 200, 20, 3],
  [1000, 650, 250, 20, 2],
  [2100, 450, 250, 20, 2],
  [3500, 300, 250, 20, 3],
  [2630, 570, 250, 20, 3],
  [3350, 560, 250, 20, 3],
  [1350, 580, 800, 20, 2],
  [700, 450, 400, 20, 2],
  [1000, 300, 500, 20, 2],
  [0, 210, 900, 20, 2],
  [2230, 150, 1200, 20, 2],
  [2900, 650, 600, 20, 3],
  [3000, 390, 400, 20, 3],
].map(([x, y, w, h, tile]) => ({ x, y, w, h, tile }));
export const wall = { x: 2500, y: 300, w: 10, h: 550, tile: 2 };
export const hidingSpots = [16, 21, 5].map((index, i) => ({
  x: platforms[index].x + [80, 50, 50][i],
  y: platforms[index].y - 50,
  w: 50,
  h: 50,
}));
export const barrel = { x: 0, y: 150, w: 56, h: 60 };
export const fishStart = { x: 3200, y: 803, w: 65, h: 27 };
const clamp = (value, min, max) => Math.max(min, Math.min(max, value));
export const overlaps = (a, b) =>
  a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
const distance = (a, b) => Math.abs(a[0] - b[0]) + Math.abs(a[1] - b[1]);
function moveActor(actor, dx) {
  const oldX = actor.x;
  actor.x = clamp(actor.x + dx, 0, MAP_WIDTH - actor.w);
  if (overlaps(actor, wall))
    actor.x = oldX + actor.w <= wall.x ? wall.x - actor.w : wall.x + wall.w;
  const bottom = actor.y + actor.h;
  actor.vy = Math.min(actor.vy + 1.2, 15);
  actor.y += actor.vy;
  actor.grounded = false;
  let floor = GROUND;
  if (
    actor.vy >= 0 &&
    actor.x < wall.x + wall.w &&
    actor.x + actor.w > wall.x &&
    bottom <= wall.y + 0.01 &&
    actor.y + actor.h >= wall.y
  )
    floor = wall.y;
  if (actor.vy >= 0)
    for (const platform of platforms) {
      if (
        actor.x + actor.w / 2 >= platform.x &&
        actor.x + actor.w / 2 <= platform.x + platform.w &&
        bottom <= platform.y + 0.01 &&
        actor.y + actor.h >= platform.y
      )
        floor = Math.min(floor, platform.y);
    }
  if (actor.y + actor.h >= floor && actor.vy >= 0) {
    actor.y = floor - actor.h;
    actor.vy = 0;
    actor.grounded = true;
  }
}
const hitbox = (actor) => ({
  x: actor.x + actor.w / 4,
  y: actor.y + actor.h / 4,
  w: actor.w / 2,
  h: (actor.h * 3) / 4,
});

export function policyLogits(policy, observation) {
  let values = observation;
  for (let i = 0; i < policy.layers.length; i++) {
    const layer = policy.layers[i];
    values = layer.weight.map((row, j) => {
      const value = row.reduce(
        (sum, w, k) => sum + w * values[k],
        layer.bias[j],
      );
      return i < 2 ? Math.tanh(value) : value;
    });
  }
  return values;
}
export function policyActions(policy, observation, random = Math.random) {
  const logits = policyLogits(policy, observation);
  return [
    [0, 3],
    [3, 5],
    [5, 7],
  ].map(([start, end]) => {
    const group = logits.slice(start, end),
      max = Math.max(...group);
    const weights = group.map((v) => Math.exp(v - max));
    let draw = random() * weights.reduce((a, b) => a + b, 0);
    for (let i = 0; i < weights.length; i++) {
      draw -= weights[i];
      if (draw <= 0) return i;
    }
    return weights.length - 1;
  });
}

const surfaces = [
  { x: 0, y: GROUND, w: wall.x },
  { x: wall.x + wall.w, y: GROUND, w: MAP_WIDTH - wall.x - wall.w },
  ...platforms,
];
function surfaceUnder(actor) {
  const center = actor.x + actor.w / 2,
    feet = actor.y + actor.h;
  let best = -1;
  surfaces.forEach((surface, i) => {
    if (
      center >= surface.x - 1 &&
      center <= surface.x + surface.w + 1 &&
      surface.y >= feet - 1 &&
      (best < 0 || surface.y < surfaces[best].y)
    )
      best = i;
  });
  return best;
}
const dropExits = (surface) =>
  [surface.x - 2, surface.x + surface.w + 2].filter(
    (x) =>
      x >= 72 &&
      x <= MAP_WIDTH - 72 &&
      !overlaps({ x: x - 72, y: surface.y - 144, w: 144, h: 144 }, wall),
  );
const surfacePlans = surfaces.map(() => new Map());
const surfaceEdges = surfaces.map((a, i) =>
  surfaces.flatMap((b, j) => {
    if (i === j || a.y - b.y > 190.8) return [];
    const left = Math.max(a.x, b.x),
      right = Math.min(a.x + a.w, b.x + b.w),
      drop = b.y > a.y && left <= right;
    const launches = drop
      ? dropExits(a)
      : left <= right
        ? [(left + right) / 2, left, right]
        : [b.x > a.x ? a.x + a.w : a.x];
    for (const launch of launches) {
      if (launch < 72 || launch > MAP_WIDTH - 72) continue;
      const landing = clamp(launch, b.x, b.x + b.w),
        speed = drop ? 3.5 : 4.25;
      const actor = {
        x: launch - 72,
        y: a.y - 144 + (drop ? 1.2 : 0),
        w: 144,
        h: 144,
        vy: drop ? 1.2 : -22,
        grounded: false,
      };
      if (overlaps(actor, wall)) continue;
      for (let time = 0; time < 150; time++) {
        const dx = landing - actor.x - 72;
        moveActor(actor, Math.sign(dx) * Math.min(Math.abs(dx), speed));
        if (actor.grounded) {
          if (
            Math.abs(actor.y + 144 - b.y) < 1 &&
            actor.x + 72 >= b.x &&
            actor.x + 72 <= b.x + b.w
          ) {
            surfacePlans[i].set(j, { launch, landing, drop, speed });
            return [j];
          }
          break;
        }
      }
    }
    return [];
  }),
);
function surfacePath(actor, target) {
  const start = surfaceUnder(actor),
    goal = surfaceUnder(target);
  if (start < 0 || goal < 0) return [];
  const point = (index) => [
    surfaces[index].x + surfaces[index].w / 2,
    surfaces[index].y,
  ];
  const open = new Set([start]),
    cost = new Map([[start, 0]]),
    previous = new Map();
  while (open.size) {
    const current = [...open].reduce((best, index) =>
      cost.get(index) + distance(point(index), point(goal)) <
      cost.get(best) + distance(point(best), point(goal))
        ? index
        : best,
    );
    if (current === goal) {
      const path = [goal];
      let node = goal;
      while (previous.has(node)) {
        node = previous.get(node);
        path.unshift(node);
      }
      return path;
    }
    open.delete(current);
    for (const next of surfaceEdges[current]) {
      const score = cost.get(current) + distance(point(current), point(next));
      if (score < (cost.get(next) ?? Infinity)) {
        cost.set(next, score);
        previous.set(next, current);
        open.add(next);
      }
    }
  }
  return [];
}

export class Game {
  constructor(policy, random = Math.random) {
    this.policy = policy;
    this.random = random;
    this.reset();
  }
  reset() {
    this.player = {
      x: 100,
      y: 690,
      w: 160,
      h: 160,
      vx: 0,
      vy: 0,
      grounded: true,
      hidden: false,
      health: 5,
      invincible: 0,
      facing: 1,
    };
    this.guards = [16, 21].map((index) => ({
      x: platforms[index].x + 30,
      y: platforms[index].y - 144,
      w: 144,
      h: 144,
      direction: 1,
      facing: 1,
      platform: index,
    }));
    this.shopkeeper = {
      x: 2710,
      y: 706,
      w: 144,
      h: 144,
      direction: 1,
      facing: 1,
      speed: 3.5,
      vx: 0,
      vy: 0,
      grounded: true,
      path: [],
      targetSurface: -1,
      dropFrom: -1,
    };
    this.fish = { ...fishStart };
    this.carrying = false;
    this.time = 0;
    this.camera = 0;
    this.state = "playing";
    this.lastFish = -Infinity;
    this.lastHide = -Infinity;
    this.actions = [1, 0, 0];
    this.lastAI = -Infinity;
  }
  useFish() {
    if (
      this.state !== "playing" ||
      this.player.hidden ||
      this.time - this.lastFish < 30
    )
      return;
    if (this.carrying) {
      this.carrying = false;
      this.fish = {
        ...fishStart,
        x: this.player.x + this.player.w / 2,
        y: this.player.y + this.player.h - 27,
      };
      this.lastFish = this.time;
    } else if (overlaps(this.player, this.fish)) {
      this.carrying = true;
      this.lastFish = this.time;
    }
  }
  hide() {
    if (this.state !== "playing" || this.time - this.lastHide < 30) return;
    if (this.player.hidden) {
      this.player.hidden = false;
      this.lastHide = this.time;
    } else if (
      this.player.grounded &&
      hidingSpots.some((spot) => overlaps(this.player, spot))
    ) {
      this.player.hidden = true;
      this.player.vx = 0;
      this.lastHide = this.time;
    }
  }
  damage() {
    const p = this.player;
    if (p.hidden || p.invincible > 0) return;
    p.health--;
    p.invincible = 240;
    if (p.health <= 0) this.state = "lost";
  }
  tick(input = {}) {
    if (this.state !== "playing") return;
    this.time++;
    const p = this.player;
    p.invincible = Math.max(0, p.invincible - 1);
    if (input.fish) this.useFish();
    if (input.hide) {
      if (p.hidden || hidingSpots.some((spot) => overlaps(p, spot)))
        this.hide();
      else this.useFish();
    }
    if (!p.hidden) {
      if (input.left) p.vx = -5;
      else if (input.right) p.vx = 5;
      else if (p.grounded) p.vx = 0;
      if (input.jump && p.grounded) {
        p.vy = -22;
        p.grounded = false;
      }
      if (p.vx) p.facing = Math.sign(p.vx);
      moveActor(p, p.vx);
    }
    if (this.policy && this.time - this.lastAI >= 6) {
      this.actions = policyActions(
        this.policy,
        [
          p.x,
          p.y,
          this.shopkeeper.x,
          this.shopkeeper.y,
          ...this.guards.flatMap((g) => [g.x, g.y]),
        ],
        this.random,
      );
      this.lastAI = this.time;
    }
    this.moveShopkeeper();
    for (let i = 0; i < this.guards.length; i++) {
      const guard = this.guards[i],
        platform = platforms[guard.platform];
      if (
        this.time % 30 === 0 &&
        this.actions[i + 1] === 1 &&
        !p.hidden &&
        Math.abs(p.y - guard.y) < 100 &&
        Math.abs(p.x - guard.x) > 60
      )
        guard.direction = Math.sign(p.x - guard.x) || guard.direction;
      guard.x += guard.direction * 2;
      if (guard.x + guard.w >= platform.x + platform.w - 30) {
        guard.x = platform.x + platform.w - guard.w - 30;
        guard.direction = -1;
      }
      if (guard.x <= platform.x + 30) {
        guard.x = platform.x + 30;
        guard.direction = 1;
      }
      guard.facing = guard.direction;
      if (overlaps(hitbox(p), hitbox(guard)) && p.y + p.h > guard.y + 10)
        this.damage();
    }
    if (
      this.carrying &&
      !p.hidden &&
      overlaps(hitbox(p), hitbox(this.shopkeeper))
    ) {
      this.carrying = false;
      this.fish = { ...fishStart };
      Object.assign(this.shopkeeper, {
        x: 2710,
        y: 706,
        vx: 0,
        vy: 0,
        grounded: true,
        path: [],
      });
    }
    if (this.carrying && overlaps(p, barrel)) this.state = "won";
    this.camera = clamp(p.x + p.w / 2 - WIDTH / 2, 0, MAP_WIDTH - WIDTH);
  }
  moveShopkeeper() {
    const s = this.shopkeeper,
      p = this.player;
    let targetSpeed =
      3.5 + 0.75 * (1 - clamp(Math.hypot(s.x - p.x, s.y - p.y) / 1600, 0, 1));
    if (this.actions[0] === 0) targetSpeed = 4.25;
    if (this.actions[0] === 2) targetSpeed = 3.5;
    s.speed += clamp(targetSpeed - s.speed, -0.025, 0.025);
    let desiredVelocity = 0,
      stopAt = null;
    if (this.carrying && !p.hidden) {
      const center = s.x + s.w / 2,
        current = surfaceUnder(s);
      if (s.grounded && s.dropFrom === current) {
        desiredVelocity = Math.sign(s.dropX - center) * s.speed;
      } else if (s.grounded) {
        s.dropFrom = -1;
        s.path = surfacePath(s, p);
        if (s.path.length > 1) {
          const plan = surfacePlans[current].get(s.path[1]);
          s.targetSurface = s.path[1];
          s.landingX = plan.landing;
          s.flightSpeed = plan.speed;
          const dx = plan.launch - center;
          if (plan.drop) {
            s.dropFrom = current;
            s.dropX = plan.launch;
            desiredVelocity = Math.sign(dx) * s.speed;
          } else if (Math.abs(dx) > 1) {
            desiredVelocity = Math.sign(dx) * s.speed;
            stopAt = plan.launch;
          } else {
            s.vy = -22;
            s.grounded = false;
            desiredVelocity = Math.sign(plan.landing - center) * plan.speed;
            if (Math.abs(plan.landing - center) > 1) s.vx = desiredVelocity;
          }
        } else {
          s.targetSurface = -1;
          desiredVelocity =
            Math.abs(p.x - s.x) > 8 ? Math.sign(p.x - s.x) * s.speed : 0;
        }
      } else if (s.targetSurface >= 0) {
        s.dropFrom = -1;
        const dx = s.landingX - center;
        desiredVelocity =
          Math.abs(dx) > 1 ? Math.sign(dx) * (s.flightSpeed ?? s.speed) : 0;
        stopAt = s.landingX;
      }
    } else if (!this.carrying) {
      s.path = [];
      s.targetSurface = -1;
      s.dropFrom = -1;
      if (s.grounded && s.y + s.h < GROUND - 8) {
        const floor = surfaces[surfaceUnder(s)];
        if (floor)
          desiredVelocity = s.x + s.w / 2 < floor.x + floor.w / 2 ? -2 : 2;
      } else {
        if (s.x + s.w >= MAP_WIDTH - 4) s.direction = -1;
        if (s.x <= 2656) s.direction = 1;
        desiredVelocity = s.direction * 2;
      }
    } else {
      s.path = [];
      s.targetSurface = -1;
      s.dropFrom = -1;
    }
    s.vx += clamp(desiredVelocity - s.vx, -0.15, 0.15);
    if (Math.abs(s.vx) < 0.01) s.vx = 0;
    let dx = s.vx;
    if (
      stopAt !== null &&
      Math.sign(stopAt - s.x - s.w / 2) === Math.sign(dx) &&
      Math.abs(dx) > Math.abs(stopAt - s.x - s.w / 2)
    ) {
      dx = stopAt - s.x - s.w / 2;
    }
    if (
      !s.grounded &&
      stopAt !== null &&
      Math.abs(stopAt - s.x - s.w / 2) < 1
    ) {
      dx = stopAt - s.x - s.w / 2;
      s.vx = 0;
    }
    if (Math.abs(dx) > 0.1) s.facing = Math.sign(dx);
    moveActor(s, dx);
  }
}
