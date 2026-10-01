import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import { Icon } from '../../../../shared/components/icon/icon';

@Component({
  selector: 'app-conversation-search',
  imports: [Icon],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <label class="search">
      <span class="visually-hidden">Tìm kiếm cuộc trò chuyện</span>
      <app-icon name="search" [size]="17" class="search__icon" />
      <input type="search" placeholder="Tìm kiếm cuộc trò chuyện..." autocomplete="off"
             [value]="query()" (input)="queryChange.emit($any($event.target).value)"
             (keydown.escape)="queryChange.emit('')" />
      @if (query()) {
        <button type="button" class="search__clear" aria-label="Xóa từ khóa" (click)="queryChange.emit('')">
          <app-icon name="close" [size]="14" />
        </button>
      }
    </label>
  `,
  styles: `
    :host { display: block; }
    .search {
      position: relative;
      display: flex;
      align-items: center;
      height: 40px;
      border: 1px solid var(--color-border);
      border-radius: var(--radius-sm);
      background: var(--color-surface-sunken);
      transition: border-color var(--duration-fast) ease, background-color var(--duration-fast) ease,
        box-shadow var(--duration-fast) ease;
    }
    .search:hover { border-color: var(--color-border-strong); }
    .search:focus-within {
      border-color: var(--color-navy);
      background: var(--color-surface);
      box-shadow: 0 0 0 3px var(--color-navy-50);
    }
    .search__icon { position: absolute; left: 11px; color: var(--color-text-subtle); pointer-events: none; }
    input {
      flex: 1;
      min-width: 0;
      height: 100%;
      padding: 0 32px 0 36px;
      border: 0;
      background: none;
      color: var(--color-text);
      font: inherit;
      font-size: 14px;
      outline: none;
    }
    input::placeholder { color: var(--color-text-subtle); }
    input::-webkit-search-cancel-button { display: none; }
    .search__clear {
      position: absolute;
      right: 6px;
      display: grid;
      place-items: center;
      width: 24px;
      height: 24px;
      border: 0;
      border-radius: 50%;
      background: var(--color-border);
      color: var(--color-text-muted);
      cursor: pointer;
    }
    .search__clear:hover { background: var(--color-border-strong); color: var(--color-text); }
    .search__clear:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 1px; }
  `,
})
export class ConversationSearch {
  readonly query = input('');
  readonly queryChange = output<string>();
}
