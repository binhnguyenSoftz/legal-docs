import { Injectable, InjectionToken, inject } from '@angular/core';
import { Observable, delay, of, throwError, timer, switchMap } from 'rxjs';
import { MOCK_INTENTS, NO_RESULT_REPLY } from '../mocks/mock-replies';
import { AssistantReply, ChatMessage } from '../models/chat.models';
import { normalizeVietnamese } from '../utils/text';

export interface AssistantRequest {
  conversationId: string;
  question: string;
  history: ChatMessage[];
  attachmentNames: string[];
}

/**
 * Boundary between UI and the assistant backend. Swap `MockAssistantGateway`
 * for an HTTP implementation in `app.config.ts` once the API is available.
 */
export interface AssistantGateway {
  ask(request: AssistantRequest): Observable<AssistantReply>;
}

export const ASSISTANT_GATEWAY = new InjectionToken<AssistantGateway>('ASSISTANT_GATEWAY', {
  providedIn: 'root',
  factory: () => inject(MockAssistantGateway),
});

/** Phrases that force the connection-error state, for demos and QA. */
const ERROR_TRIGGERS = ['mat ket noi', 'loi ket noi'];

@Injectable({ providedIn: 'root' })
export class MockAssistantGateway implements AssistantGateway {
  /** Simulated latency, in ms. */
  latency = { min: 900, max: 1800 };

  ask({ question }: AssistantRequest): Observable<AssistantReply> {
    // Pad with spaces so keywords only match whole syllables ("o ga" must not match "ho so gap").
    const normalized = ` ${normalizeVietnamese(question).replace(/[^a-z0-9]+/g, ' ')} `;
    const has = (keyword: string) => normalized.includes(` ${keyword} `);
    const wait = this.latency.min + Math.random() * (this.latency.max - this.latency.min);

    if (ERROR_TRIGGERS.some(has)) {
      return timer(wait).pipe(switchMap(() => throwError(() => new Error('Network unreachable'))));
    }

    const intent = MOCK_INTENTS.find((i) => i.keywords.some(has));
    return of(intent?.reply ?? NO_RESULT_REPLY).pipe(delay(wait));
  }
}
