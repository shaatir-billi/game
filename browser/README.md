# Browser game

Play at [shaatirbilli.mhadi.dev](https://shaatirbilli.mhadi.dev). Use Node.js 22 or newer.

Run these commands from this folder:

```sh
npm ci
npm run dev
```

Open http://127.0.0.1:5175. Use A and D to move, W to jump, E to hide or take the fish, and Q to take or drop the fish. Take the fish to the barrel at the top left. Quit stops the game. Reload the page to open the menu.

```sh
npm run build
npm run deploy
```

The browser uses the assets in `../assets/` and actor weights from `../marl_model.zip`. Run `python3 scripts/export-policy.py` to export the weights. The Python game runs from the repository root.
