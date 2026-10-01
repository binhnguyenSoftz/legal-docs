import { Injectable, computed, signal } from '@angular/core';
import { createMockConversations } from '../mocks/mock-conversations';
import { ChatMessage, Conversation, ConversationGroup } from '../models/chat.models';
import { DAY_MS, startOfVietnamDay } from '../utils/date';
import { createId, normalizeVietnamese } from '../utils/text';

/** Owns conversation history: list, active selection, search and grouping. */
@Injectable({ providedIn: 'root' })
export class ConversationService {
  private readonly _conversations = signal<Conversation[]>(createMockConversations());
  private readonly _activeId = signal<string | null>(null);
  private readonly _query = signal('');

  readonly conversations = this._conversations.asReadonly();
  readonly activeId = this._activeId.asReadonly();
  readonly query = this._query.asReadonly();

  readonly active = computed(
    () => this._conversations().find((c) => c.id === this._activeId()) ?? null,
  );

  readonly groups = computed<ConversationGroup[]>(() => {
    const q = normalizeVietnamese(this._query());
    const items = this._conversations()
      .filter((c) => !q || normalizeVietnamese(c.title).includes(q))
      .sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
    return groupByRecency(items, Date.now());
  });

  setQuery(query: string): void {
    this._query.set(query);
  }

  select(id: string | null): void {
    this._activeId.set(id);
  }

  /** Clears the selection so the welcome screen shows; the conversation is created on first send. */
  startNew(): void {
    this._activeId.set(null);
  }

  create(title: string): Conversation {
    const conversation: Conversation = {
      id: createId('c'),
      title,
      updatedAt: new Date().toISOString(),
      messages: [],
    };
    this._conversations.update((list) => [conversation, ...list]);
    this._activeId.set(conversation.id);
    return conversation;
  }

  appendMessage(conversationId: string, message: ChatMessage): void {
    this.patch(conversationId, (c) => ({
      ...c,
      updatedAt: message.createdAt,
      messages: [...c.messages, message],
    }));
  }

  updateMessage(conversationId: string, messageId: string, change: Partial<ChatMessage>): void {
    this.patch(conversationId, (c) => ({
      ...c,
      messages: c.messages.map((m) => (m.id === messageId ? ({ ...m, ...change } as ChatMessage) : m)),
    }));
  }

  removeMessage(conversationId: string, messageId: string): void {
    this.patch(conversationId, (c) => ({ ...c, messages: c.messages.filter((m) => m.id !== messageId) }));
  }

  rename(conversationId: string, title: string): void {
    this.patch(conversationId, (c) => ({ ...c, title }));
  }

  delete(conversationId: string): void {
    this._conversations.update((list) => list.filter((c) => c.id !== conversationId));
    if (this._activeId() === conversationId) this._activeId.set(null);
  }

  /** Re-inserts a deleted conversation (undo). */
  restore(conversation: Conversation): void {
    if (this._conversations().some((c) => c.id === conversation.id)) return;
    this._conversations.update((list) => [...list, conversation]);
  }

  private patch(id: string, fn: (c: Conversation) => Conversation): void {
    this._conversations.update((list) => list.map((c) => (c.id === id ? fn(c) : c)));
  }
}

function groupByRecency(items: Conversation[], now: number): ConversationGroup[] {
  const startOfToday = startOfVietnamDay(now);
  const buckets: ConversationGroup[] = [
    { label: 'Hôm nay', conversations: [] },
    { label: 'Hôm qua', conversations: [] },
    { label: '7 ngày qua', conversations: [] },
    { label: 'Cũ hơn', conversations: [] },
  ];
  for (const c of items) {
    const t = new Date(c.updatedAt).getTime();
    const index = t >= startOfToday ? 0 : t >= startOfToday - DAY_MS ? 1 : t >= startOfToday - 7 * DAY_MS ? 2 : 3;
    buckets[index].conversations.push(c);
  }
  return buckets.filter((b) => b.conversations.length > 0);
}
