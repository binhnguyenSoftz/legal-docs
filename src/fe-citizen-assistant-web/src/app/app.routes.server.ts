import { RenderMode, ServerRoute } from '@angular/ssr';

export const serverRoutes: ServerRoute[] = [
  {
    // Rendered per request: history and account info are per user, so build-time prerendering does not fit.
    path: '**',
    renderMode: RenderMode.Server,
  },
];
