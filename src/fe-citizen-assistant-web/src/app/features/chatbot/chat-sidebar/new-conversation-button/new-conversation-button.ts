import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import { MatTooltipModule } from '@angular/material/tooltip';
import { Icon } from '../../../../shared/components/icon/icon';

@Component({
  selector: 'app-new-conversation-button',
  imports: [Icon, MatTooltipModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <button type="button" class="new" [class.new--compact]="compact()" (click)="create.emit()"
            [attr.aria-label]="compact() ? 'Cuộc trò chuyện mới' : null"
            [matTooltip]="compact() ? 'Cuộc trò chuyện mới (Ctrl K)' : ''" matTooltipPosition="right">
      <span class="new__plus"><app-icon name="plus" [size]="18" [stroke]="2.4" /></span>
      @if (!compact()) {
        <span class="new__label">Cuộc trò chuyện mới</span>
      }
    </button>
  `,
  styles: `
    :host { display: block; }
    .new {
      display: flex;
      align-items: center;
      gap: 10px;
      width: 100%;
      height: 42px;
      padding: 0 14px 0 10px;
      border: 1px solid transparent;
      border-radius: var(--radius-md);
      background: var(--color-primary);
      color: #fff;
      font: inherit;
      font-size: 14.5px;
      font-weight: 600;
      cursor: pointer;
      transition: background-color var(--duration-fast) ease;
    }
    .new:hover { background: var(--color-primary-hover); }
    .new:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
    .new--compact { justify-content: center; width: 42px; padding: 0; }
    .new__plus {
      display: grid;
      place-items: center;
    }
    .new__label { flex: 1; text-align: left; white-space: nowrap; }
  `,
})
export class NewConversationButton {
  readonly compact = input(false);
  readonly create = output<void>();
}
