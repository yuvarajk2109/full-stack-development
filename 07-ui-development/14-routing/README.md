# Lab 14 — Routing Fundamentals: Routes, Lazy Loading & Navigation

## Setup

Your own `mission-ui` from Module 13, with `HoldingsSummary` and `PlaceOrder` both currently
shown together in `app.html`.

## Task

1. In `app.routes.ts`, define at least two routes using `loadComponent`:

   ```typescript
   export const routes: Routes = [
     { path: '', redirectTo: 'holdings', pathMatch: 'full' },
     { path: 'holdings', loadComponent: () => import('./holdings-summary/holdings-summary').then((m) => m.HoldingsSummary) },
     { path: 'orders', loadComponent: () => import('./place-order/place-order').then((m) => m.PlaceOrder) },
   ];
   ```

2. Remove the direct `<app-holdings-summary />`/`<app-place-order />` tags from `app.html`
   and their imports from `app.ts` — they're routed now, not embedded.

3. Add a `<nav>` with two `routerLink`s (and `routerLinkActive`) to `app.html`, and import
   `RouterLink`/`RouterLinkActive` into `app.ts`'s `imports` array.

## Verify

1. `ng build`. Confirm your two lazy component names appear under **Lazy chunk files**, not
   in the initial `main.js` bundle.
2. `ng serve`. Loading the bare `/` should redirect you to `/holdings` automatically.
3. Click your "Place Order" link. Confirm the URL changes to `/orders`, the page does **not**
   reload, and the active link's styling moves to match.
4. Open DevTools' Network tab, clear it, then click between your two nav links a few times.
   Confirm each lazy chunk is only ever requested **once** — Angular caches it after the
   first visit, it doesn't re-fetch on every navigation back to a route already visited.

## A Question Worth Sitting With

`pathMatch: 'full'` is set on the `''` route's redirect, not on `'holdings'` or `'orders'`.
What would go wrong — specifically, what would happen when you tried to navigate to
`/orders` — if `pathMatch: 'full'` were removed from the `''` route entirely?

Angular 21 throws
`NG04014` at application startup, a hard runtime error, not a subtle bug. The route
configuration is invalid the moment the app tries to boot, because an ambiguous `redirectTo`
on a prefix-matched empty path has no well-defined meaning the router is willing to guess at.
`pathMatch: 'full'` resolves the ambiguity by saying "only redirect when the URL is *exactly*
empty," leaving `/holdings` and `/orders` alone.

A second question: `loadComponent` fetches a component's code the first time its route is
visited, not when the app first loads. What's the practical trade-off here — name one
concrete situation where lazy loading a route makes the *user's* experience worse, not
better, and explain why.

The most common real case is a route a user visits *immediately* after the app first loads — for example, if `/holdings` (this app's default, redirected-to route) were lazy-loaded instead of the root route eagerly
bundling it. The very first thing most users see would require a *second* network round-trip
after the initial page load completes, adding a visible delay (and a loading flicker) exactly
where a user is least willing to wait — the first thing they see. Angular's `PreloadAllModules`
strategy (or a custom preloading strategy) exists specifically to soften this: it still lazy-
loads for the initial bundle-size win, but starts fetching the other routes' chunks in the
background immediately after the app boots, so by the time a user actually clicks, the chunk
is often already there.
