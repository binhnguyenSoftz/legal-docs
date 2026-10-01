import { TestBed } from '@angular/core/testing';
import { Subject } from 'rxjs';
import { AssistantMessage, AssistantReply } from '../models/chat.models';
import { ASSISTANT_GATEWAY, AssistantGateway } from './assistant-gateway';
import { ChatService } from './chat.service';
import { ConversationService } from './conversation.service';

describe('ChatService', () => {
  let reply$: Subject<AssistantReply>;
  let chat: ChatService;
  let conversations: ConversationService;

  beforeEach(() => {
    reply$ = new Subject<AssistantReply>();
    const gateway: AssistantGateway = { ask: () => reply$ };
    TestBed.configureTestingModule({ providers: [{ provide: ASSISTANT_GATEWAY, useValue: gateway }] });
    chat = TestBed.inject(ChatService);
    conversations = TestBed.inject(ConversationService);
  });

  it('starts a conversation on first send and appends the reply', () => {
    chat.send('Hồ sơ bồi thường cần gì?');

    const active = conversations.active()!;
    expect(active.title).toBe('Hồ sơ bồi thường cần gì?');
    expect(chat.isThinking()).toBe(true);

    reply$.next({ status: 'complete', title: 'Hồ sơ bồi thường', blocks: [], sources: [], suggestions: [] });

    expect(chat.isThinking()).toBe(false);
    expect(conversations.active()!.messages.map((m) => m.role)).toEqual(['user', 'assistant']);
    expect(conversations.active()!.title).toBe('Hồ sơ bồi thường');
  });

  it('records an error reply and retries it', () => {
    chat.send('Câu hỏi');
    reply$.error(new Error('offline'));

    const failed = conversations.active()!.messages[1] as AssistantMessage;
    expect(failed.status).toBe('error');

    reply$ = new Subject<AssistantReply>();
    TestBed.inject(ASSISTANT_GATEWAY).ask = () => reply$;
    chat.retry(failed);
    reply$.next({ status: 'no-result', blocks: [], sources: [], suggestions: [] });

    const messages = conversations.active()!.messages;
    expect(messages.length).toBe(2);
    expect((messages[1] as AssistantMessage).status).toBe('no-result');
  });

  it('ignores empty input', () => {
    chat.send('   ');
    expect(conversations.active()).toBeNull();
  });
});
