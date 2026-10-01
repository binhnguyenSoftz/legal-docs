import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { ContentBlock, SourceReference } from '../../../../core/models/chat.models';
import { Icon } from '../../../../shared/components/icon/icon';
import { ProcedureCard } from '../../../../shared/components/procedure-card/procedure-card';
import { RichText } from '../../../../shared/components/rich-text/rich-text';

const CALLOUT_ICONS = { info: 'info', success: 'check', warning: 'warning' } as const;

/** Renders the structured blocks of an assistant answer. */
@Component({
  selector: 'app-message-content',
  imports: [RichText, ProcedureCard, Icon],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './message-content.html',
  styleUrl: './message-content.scss',
})
export class MessageContent {
  readonly blocks = input.required<ContentBlock[]>();
  readonly sources = input<SourceReference[]>([]);
  protected readonly calloutIcons = CALLOUT_ICONS;
}
