import {
  ChangeDetectionStrategy,
  Component,
  ElementRef,
  afterRenderEffect,
  computed,
  input,
  output,
  viewChild,
} from '@angular/core';
import {
  AssistantMessage as AssistantMessageModel,
  Conversation,
  SuggestedQuestion as SuggestedQuestionModel,
} from '../../../core/models/chat.models';
import { AssistantMessage } from '../chat-message/assistant-message/assistant-message';
import { UserMessage } from '../chat-message/user-message/user-message';
import { TypingIndicator } from './typing-indicator/typing-indicator';

export interface FeedbackEvent {
  message: AssistantMessageModel;
  value: 'up' | 'down';
}

@Component({
  selector: 'app-chat-conversation',
  imports: [UserMessage, AssistantMessage, TypingIndicator],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './chat-conversation.html',
  styleUrl: './chat-conversation.scss',
})
export class ChatConversation {
  readonly conversation = input.required<Conversation>();
  readonly thinking = input(false);
  readonly busy = input(false);

  readonly ask = output<SuggestedQuestionModel>();
  readonly retry = output<AssistantMessageModel>();
  readonly feedback = output<FeedbackEvent>();

  private readonly log = viewChild.required<ElementRef<HTMLElement>>('log');
  private lastConversationId?: string;
  private lastMessageCount = 0;

  protected readonly lastAssistantId = computed(() => {
    const messages = this.conversation().messages;
    for (let i = messages.length - 1; i >= 0; i--) if (messages[i].role === 'assistant') return messages[i].id;
    return null;
  });

  constructor() {
    // Keep the newest content in view: the question + thinking indicator at the bottom,
    // or the top of a new answer so long replies are read from the beginning.
    afterRenderEffect(() => {
      const { id, messages } = this.conversation();
      const thinking = this.thinking();
      const switched = id !== this.lastConversationId;
      if (!switched && messages.length === this.lastMessageCount && !thinking) return;
      this.lastConversationId = id;
      this.lastMessageCount = messages.length;

      const behavior: ScrollBehavior = switched ? 'instant' : 'smooth';
      const items = this.log().nativeElement.querySelectorAll<HTMLElement>('[data-message]');
      const last = items[items.length - 1];
      if (!thinking && messages.at(-1)?.role === 'assistant' && last) {
        last.scrollIntoView({ block: 'start', behavior });
      } else {
        this.log().nativeElement.lastElementChild?.scrollIntoView({ block: 'end', behavior });
      }
    });
  }

  protected asAssistant(message: Conversation['messages'][number]): AssistantMessageModel {
    return message as AssistantMessageModel;
  }
}
