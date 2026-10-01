import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import { SuggestedQuestion as SuggestedQuestionModel } from '../../../core/models/chat.models';
import { Icon } from '../icon/icon';

/** Follow-up question chip. */
@Component({
  selector: 'app-suggested-question',
  imports: [Icon],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <button type="button" class="chip" [disabled]="disabled()" (click)="pick.emit(question())">
      <app-icon name="arrow-right" [size]="14" class="chip__icon" />
      <span>{{ question().text }}</span>
    </button>
  `,
  styles: `
    :host { display: block; min-width: 0; }
    .chip {
      display: flex;
      align-items: center;
      gap: 8px;
      width: 100%;
      padding: 8px 14px;
      border: 1px solid var(--color-border);
      border-radius: var(--radius-md);
      background: var(--color-surface);
      color: var(--color-navy);
      font: inherit;
      font-size: 14px;
      text-align: left;
      cursor: pointer;
      transition: border-color var(--duration-fast) ease, background-color var(--duration-fast) ease,
        transform var(--duration-fast) ease;
    }
    .chip:hover:not(:disabled) {
      border-color: var(--color-primary);
      background: var(--color-surface);
    }
    .chip:hover:not(:disabled) .chip__icon { color: var(--color-primary); }
    .chip:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
    .chip:disabled { opacity: 0.55; cursor: not-allowed; }
    .chip__icon { color: var(--color-text-subtle); transition: transform var(--duration-fast) ease, color var(--duration-fast) ease; }
    span { overflow-wrap: anywhere; }
  `,
})
export class SuggestedQuestion {
  readonly question = input.required<SuggestedQuestionModel>();
  readonly disabled = input(false);
  readonly pick = output<SuggestedQuestionModel>();
}
