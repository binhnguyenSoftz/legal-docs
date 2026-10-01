import { Clipboard } from '@angular/cdk/clipboard';
import { DOCUMENT, DatePipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, computed, inject, input, output, signal } from '@angular/core';
import { MatTooltipModule } from '@angular/material/tooltip';
import {
  AssistantMessage as AssistantMessageModel,
  ContentBlock,
  SuggestedQuestion as SuggestedQuestionModel,
} from '../../../../core/models/chat.models';
import { AssistantAvatar } from '../../../../shared/components/assistant-avatar/assistant-avatar';
import { Icon } from '../../../../shared/components/icon/icon';
import { stripInlineMarkup } from '../../../../shared/components/rich-text/inline-markup';
import { SourceCard } from '../../../../shared/components/source-card/source-card';
import { StateNotice } from '../../../../shared/components/state-notice/state-notice';
import { SuggestedQuestion } from '../../../../shared/components/suggested-question/suggested-question';
import { MessageContent } from '../message-content/message-content';

const COLLAPSED_SOURCE_COUNT = 3;

@Component({
  selector: 'app-assistant-message',
  imports: [AssistantAvatar, Icon, MessageContent, SourceCard, StateNotice, SuggestedQuestion, DatePipe, MatTooltipModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './assistant-message.html',
  styleUrl: './assistant-message.scss',
})
export class AssistantMessage {
  private readonly clipboard = inject(Clipboard);
  private readonly document = inject(DOCUMENT);

  readonly message = input.required<AssistantMessageModel>();
  /** Only the latest answer shows follow-up suggestions. */
  readonly isLatest = input(false);
  readonly busy = input(false);

  readonly ask = output<SuggestedQuestionModel>();
  readonly retry = output<AssistantMessageModel>();
  readonly feedback = output<'up' | 'down'>();

  protected readonly copied = signal(false);
  protected readonly showAllSources = signal(false);

  protected readonly visibleSources = computed(() => {
    const sources = this.message().sources;
    return this.showAllSources() ? sources : sources.slice(0, COLLAPSED_SOURCE_COUNT);
  });
  protected readonly hiddenSourceCount = computed(
    () => this.message().sources.length - this.visibleSources().length,
  );
  protected readonly hasOfficialSource = computed(() => this.message().sources.some((s) => s.official));

  protected copy(): void {
    if (this.clipboard.copy(this.toPlainText())) {
      this.copied.set(true);
      setTimeout(() => this.copied.set(false), 2000);
    }
  }

  protected download(): void {
    const blob = new Blob([this.toPlainText()], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = this.document.createElement('a');
    a.href = url;
    a.download = `tra-loi-tro-ly-so-${this.message().id}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  }

  private toPlainText(): string {
    const body = this.message().blocks.map(blockToText).filter(Boolean).join('\n\n');
    const sources = this.message().sources.map((s, i) => `[${i + 1}] ${s.title} - ${s.publisher} (${s.url})`);
    return sources.length ? `${body}\n\nNguồn:\n${sources.join('\n')}` : body;
  }
}

function blockToText(block: ContentBlock): string {
  switch (block.type) {
    case 'heading':
      return block.text.toUpperCase();
    case 'paragraph':
      return stripInlineMarkup(block.text);
    case 'list':
      return block.items.map((item, i) => `${block.ordered ? `${i + 1}.` : '-'} ${stripInlineMarkup(item)}`).join('\n');
    case 'table':
      return [block.caption, block.headers.join(' | '), ...block.rows.map((r) => r.map(stripInlineMarkup).join(' | '))]
        .filter(Boolean)
        .join('\n');
    case 'callout':
      return `${block.title ? `${block.title}: ` : ''}${stripInlineMarkup(block.text)}`;
    case 'procedure':
      return `Thủ tục: ${block.procedure.name} (mã ${block.procedure.code}) - ${block.procedure.submitUrl}`;
  }
}
