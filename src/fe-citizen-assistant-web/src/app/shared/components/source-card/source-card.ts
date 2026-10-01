import { DatePipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, computed, input, signal } from '@angular/core';
import { SourceReference } from '../../../core/models/chat.models';
import { Icon } from '../icon/icon';

/** Compact citation row: title, number, publisher, update date, expandable excerpt, open link. */
@Component({
  selector: 'app-source-card',
  imports: [Icon, DatePipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './source-card.html',
  styleUrl: './source-card.scss',
})
export class SourceCard {
  readonly source = input.required<SourceReference>();
  readonly index = input<number>();

  protected readonly expanded = signal(false);
  protected readonly actionLabel = computed(() =>
    this.source().kind === 'legal-document' ? 'Xem' : 'Mở',
  );
  protected readonly excerptId = computed(() => `excerpt-${this.source().id}`);

  protected toggle(): void {
    this.expanded.update((v) => !v);
  }
}
