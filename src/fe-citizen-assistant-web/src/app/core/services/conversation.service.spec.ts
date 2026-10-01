import { TestBed } from '@angular/core/testing';
import { ConversationService } from './conversation.service';

describe('ConversationService', () => {
  let service: ConversationService;

  beforeEach(() => {
    service = TestBed.inject(ConversationService);
  });

  it('groups seeded history by recency', () => {
    expect(service.groups().map((g) => g.label)).toEqual(['Hôm nay', 'Hôm qua', '7 ngày qua']);
  });

  it('filters by title ignoring diacritics', () => {
    service.setQuery('giay tay');
    const titles = service.groups().flatMap((g) => g.conversations.map((c) => c.title));
    expect(titles).toEqual(['Đất mua bằng giấy tay']);
  });

  it('creates, deletes and restores a conversation', () => {
    const created = service.create('Câu hỏi mới');
    expect(service.activeId()).toBe(created.id);

    service.delete(created.id);
    expect(service.activeId()).toBeNull();
    expect(service.conversations().some((c) => c.id === created.id)).toBe(false);

    service.restore(created);
    expect(service.conversations().some((c) => c.id === created.id)).toBe(true);
  });
});
