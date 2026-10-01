import { ChangeDetectionStrategy, Component } from '@angular/core';
import { AssistantAvatar } from '../../../../shared/components/assistant-avatar/assistant-avatar';


/** "Thinking" state: avatar, status line and three pulsing dots. */
@Component({
  selector: 'app-typing-indicator',
  imports: [AssistantAvatar],
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { role: 'status', 'aria-live': 'polite' },
  template: `
    <app-assistant-avatar [size]="36" />
    <div class="bubble">
      <span class="label">Trợ lý AI đang tìm kiếm thông tin...</span>
      <span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>
    </div>
  `,
  styles: `
    :host { display: flex; align-items: flex-start; gap: 12px; animation: in 240ms ease-out both; }
    .bubble {
      display: inline-flex;
      align-items: center;
      gap: 12px;
      padding: 10px 16px;
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      background: var(--color-surface);
      box-shadow: var(--shadow-xs);
    }
    .label { color: var(--color-text-muted); font-size: 14px; }
    .dots { display: inline-flex; gap: 5px; }
    .dots i {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--color-navy);
      animation: bounce 1.2s ease-in-out infinite;
    }
    .dots i:nth-child(2) { animation-delay: 0.15s; }
    .dots i:nth-child(3) { animation-delay: 0.3s; }
    @keyframes bounce {
      0%, 60%, 100% { opacity: 0.35; transform: translateY(0); }
      30% { opacity: 1; }
    }
    @keyframes in { from { opacity: 0; } to { opacity: 1; } }
  `,
})
export class TypingIndicator {}
