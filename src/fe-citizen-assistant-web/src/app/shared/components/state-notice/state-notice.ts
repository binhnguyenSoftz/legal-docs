import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { Icon } from '../icon/icon';

export type NoticeTone = 'neutral' | 'error' | 'warning';

/** Empty / error / warning panel. Projected content renders as the action row. */
@Component({
  selector: 'app-state-notice',
  imports: [Icon],
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { '[class]': '"tone-" + tone()', '[attr.role]': 'tone() === "error" ? "alert" : "status"' },
  template: `
    <span class="notice__icon"><app-icon [name]="icon()" [size]="22" /></span>
    <div class="notice__body">
      <p class="notice__title">{{ title() }}</p>
      <p class="notice__text">{{ message() }}</p>
      <div class="notice__actions"><ng-content /></div>
    </div>
  `,
  styles: `
    :host {
      display: flex;
      gap: 14px;
      padding: 16px 18px;
      border: 1px solid var(--color-border);
      border-radius: var(--radius-md);
      background: var(--color-surface);
    }
    .notice__icon {
      display: grid;
      flex: none;
      place-items: center;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: var(--color-surface-sunken);
      color: var(--color-text-muted);
    }
    .notice__body { min-width: 0; }
    .notice__title { color: var(--color-text); font-size: 15.5px; font-weight: 600; }
    .notice__text { margin-top: 2px; color: var(--color-text-muted); font-size: 14px; }
    .notice__actions:not(:empty) { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }

    :host(.tone-error) { border-color: var(--color-primary-100); background: var(--color-primary-50); }
    :host(.tone-error) .notice__icon { background: #fff; color: var(--color-primary); }
    :host(.tone-error) .notice__title { color: var(--color-primary-hover); }

    :host(.tone-warning) { border-color: var(--color-warning-border); background: var(--color-warning-50); }
    :host(.tone-warning) .notice__icon { background: #fff; color: var(--color-warning); }
    :host(.tone-warning) .notice__title { color: var(--color-warning); }
  `,
})
export class StateNotice {
  readonly tone = input<NoticeTone>('neutral');
  readonly icon = input('info');
  readonly title = input.required<string>();
  readonly message = input('');
}
