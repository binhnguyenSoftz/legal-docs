import { ChangeDetectionStrategy, Component, input } from '@angular/core';

/** Assistant mark: a gold lotus on a navy tile, with a red base line. */
@Component({
  selector: 'app-assistant-avatar',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { 'aria-hidden': 'true', '[style.--avatar-size.px]': 'size()' },
  template: `
    <svg viewBox="0 0 48 48" focusable="false">
      <rect width="48" height="48" rx="10" fill="#12304A" />
      <g fill="#D4B04A">
        <path d="M24 11c3.6 4.2 4.6 9.6 0 17.5-4.6-7.9-3.6-13.3 0-17.5z" />
        <path d="M13.5 17.5c4.8 1.4 8.8 5 9.6 11.6-6.1-1.8-9.4-6-9.6-11.6z" opacity="0.92" />
        <path d="M34.5 17.5c-4.8 1.4-8.8 5-9.6 11.6 6.1-1.8 9.4-6 9.6-11.6z" opacity="0.92" />
        <path d="M10 26c4.6-.6 9.5 1 13 5.2-5.2 1-10.2-.7-13-5.2z" opacity="0.75" />
        <path d="M38 26c-4.6-.6-9.5 1-13 5.2 5.2 1 10.2-.7 13-5.2z" opacity="0.75" />
      </g>
      <rect x="15" y="35" width="18" height="2.4" rx="1.2" fill="#e53935" />
    </svg>
  `,
  styles: `
    :host { display: inline-flex; flex: none; width: var(--avatar-size, 36px); height: var(--avatar-size, 36px); }
    svg { width: 100%; height: 100%; border-radius: 20%; }
  `,
})
export class AssistantAvatar {
  readonly size = input(36);
}
