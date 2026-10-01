import { DATE_PIPE_DEFAULT_OPTIONS, registerLocaleData } from '@angular/common';
import localeVi from '@angular/common/locales/vi';
import { ApplicationConfig, LOCALE_ID, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { VN_TIMEZONE_OFFSET } from './core/utils/date';

registerLocaleData(localeVi);

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    { provide: LOCALE_ID, useValue: 'vi' },
    provideClientHydration(withEventReplay()),
    // Same timezone on server and browser, otherwise SSR and hydration render different times.
    { provide: DATE_PIPE_DEFAULT_OPTIONS, useValue: { timezone: VN_TIMEZONE_OFFSET } },
    // To use a real backend, provide ASSISTANT_GATEWAY here, e.g.
    // { provide: ASSISTANT_GATEWAY, useExisting: HttpAssistantGateway },
  ],
};
