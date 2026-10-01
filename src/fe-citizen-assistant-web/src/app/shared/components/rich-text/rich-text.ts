import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';
import { SourceReference } from '../../../core/models/chat.models';
import { parseInlineMarkup } from './inline-markup';

/** Renders one line of assistant inline markup with citations linked to `sources`. */
@Component({
  selector: 'app-rich-text',
  changeDetection: ChangeDetectionStrategy.OnPush,
  // Kept on few lines on purpose: whitespace between tokens would render as spaces before punctuation.
  template: `@for (token of tokens(); track $index) {@switch (token.kind) {@case ('bold') {<strong>{{ token.value }}</strong>}@case ('highlight') {<mark>{{ token.value }}</mark>}@case ('link') {<a [href]="token.href" target="_blank" rel="noopener noreferrer">{{ token.value }}</a>}@case ('cite') {@let source = sources()[token.index - 1];@if (source) {<a class="cite" [href]="source.url" target="_blank" rel="noopener noreferrer" [attr.aria-label]="'Nguồn ' + token.index + ': ' + source.title" [title]="source.title">{{ token.index }}</a>}}@default {{{ token.value }}}}}`,
  styles: `
    strong { font-weight: 600; color: var(--color-text); }
    mark {
      padding: 0 4px;
      border-radius: 4px;
      background: var(--color-gold-soft);
      color: inherit;
      box-decoration-break: clone;
      -webkit-box-decoration-break: clone;
    }
    a { color: var(--color-info); text-underline-offset: 2px; }
    a:hover { color: var(--color-navy); }
    .cite {
      display: inline-grid;
      place-items: center;
      min-width: 18px;
      height: 18px;
      margin: 0 2px;
      padding: 0 4px;
      border-radius: 9px;
      background: var(--color-navy-50);
      border: 1px solid var(--color-navy-100);
      color: var(--color-navy);
      font-size: 11px;
      font-weight: 600;
      line-height: 1;
      text-decoration: none;
      vertical-align: 2px;
      transition: background-color var(--duration-fast) ease;
    }
    .cite:hover { background: var(--color-navy); color: #fff; }
  `,
})
export class RichText {
  readonly text = input.required<string>();
  readonly sources = input<SourceReference[]>([]);
  protected readonly tokens = computed(() => parseInlineMarkup(this.text()));
}
