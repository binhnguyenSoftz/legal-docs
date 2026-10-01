import { DestroyRef, Injectable, computed, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Subscription } from 'rxjs';
import { AssistantMessage, Attachment, UserMessage } from '../models/chat.models';
import { createId } from '../utils/text';
import { ASSISTANT_GATEWAY } from './assistant-gateway';
import { ConversationService } from './conversation.service';

const TITLE_MAX = 48;

/** Orchestrates a chat turn: append the question, call the assistant, append the reply or an error. */
@Injectable({ providedIn: 'root' })
export class ChatService {
  private readonly gateway = inject(ASSISTANT_GATEWAY);
  private readonly conversations = inject(ConversationService);
  private readonly destroyRef = inject(DestroyRef);

  /** Conversation id currently waiting for a reply. */
  private readonly _pendingFor = signal<string | null>(null);
  private inFlight?: Subscription;

  readonly isThinking = computed(
    () => this._pendingFor() !== null && this._pendingFor() === this.conversations.activeId(),
  );
  readonly isBusy = computed(() => this._pendingFor() !== null);

  send(text: string, attachments: Attachment[] = []): void {
    const question = text.trim();
    if ((!question && attachments.length === 0) || this.isBusy()) return;

    const conversation =
      this.conversations.active() ?? this.conversations.create(toTitle(question || attachments[0].name));

    const userMessage: UserMessage = {
      id: createId('m'),
      role: 'user',
      text: question,
      attachments,
      createdAt: new Date().toISOString(),
    };
    this.conversations.appendMessage(conversation.id, userMessage);
    this.request(conversation.id, userMessage);
  }

  /** Re-asks the question an errored reply belongs to, replacing the error message. */
  retry(failed: AssistantMessage): void {
    const conversation = this.conversations.active();
    if (!conversation || this.isBusy()) return;
    const question = conversation.messages.find((m) => m.id === failed.replyTo);
    if (!question || question.role !== 'user') return;
    this.conversations.removeMessage(conversation.id, failed.id);
    this.request(conversation.id, question);
  }

  cancel(): void {
    this.inFlight?.unsubscribe();
    this._pendingFor.set(null);
  }

  setFeedback(message: AssistantMessage, feedback: 'up' | 'down'): void {
    const conversation = this.conversations.active();
    if (!conversation) return;
    const next = message.feedback === feedback ? undefined : feedback;
    this.conversations.updateMessage(conversation.id, message.id, { feedback: next });
  }

  private request(conversationId: string, question: UserMessage): void {
    const history = this.conversations.conversations().find((c) => c.id === conversationId)?.messages ?? [];
    this._pendingFor.set(conversationId);

    this.inFlight = this.gateway
      .ask({
        conversationId,
        question: question.text,
        history,
        attachmentNames: question.attachments.map((a) => a.name),
      })
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (reply) => {
          if (reply.title && history.length === 1) this.conversations.rename(conversationId, reply.title);
          this.conversations.appendMessage(conversationId, {
            id: createId('m'),
            role: 'assistant',
            status: reply.status,
            blocks: reply.blocks,
            sources: reply.sources,
            suggestions: reply.suggestions,
            replyTo: question.id,
            createdAt: new Date().toISOString(),
          });
          this._pendingFor.set(null);
        },
        error: () => {
          this.conversations.appendMessage(conversationId, {
            id: createId('m'),
            role: 'assistant',
            status: 'error',
            blocks: [],
            sources: [],
            suggestions: [],
            replyTo: question.id,
            createdAt: new Date().toISOString(),
          });
          this._pendingFor.set(null);
        },
      });
  }
}

function toTitle(text: string): string {
  const firstLine = text.split('\n')[0].trim();
  return firstLine.length > TITLE_MAX ? `${firstLine.slice(0, TITLE_MAX - 1).trimEnd()}…` : firstLine;
}
