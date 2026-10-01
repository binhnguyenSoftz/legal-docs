import { DatePipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { UserMessage as UserMessageModel } from '../../../../core/models/chat.models';
import { formatFileSize } from '../../../../core/utils/text';
import { Icon } from '../../../../shared/components/icon/icon';

@Component({
  selector: 'app-user-message',
  imports: [Icon, DatePipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <h3 class="visually-hidden">Bạn đã hỏi</h3>
    <div class="bubble">
      @if (message().attachments.length) {
        <ul class="files" aria-label="Tệp đính kèm">
          @for (file of message().attachments; track file.id) {
            <li class="file">
              <app-icon [name]="file.kind === 'document' ? 'file' : 'paperclip'" [size]="16" />
              <span class="file__name">{{ file.name }}</span>
              <span class="file__size">{{ size(file.size) }}</span>
            </li>
          }
        </ul>
      }
      @if (message().text) {
        <p class="text">{{ message().text }}</p>
      }
    </div>
    <time class="time" [attr.datetime]="message().createdAt">{{ message().createdAt | date: 'HH:mm' }}</time>
  `,
  styles: `
    :host {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 4px;
      margin-left: auto;
      max-width: min(78%, 620px);
      animation: msg-in var(--duration-base) var(--ease-out) both;
    }
    @media (max-width: 767px) { :host { max-width: 90%; } }
    .bubble {
      padding: 10px 16px;
      border: 1px solid #e3e9f1;
      border-radius: 12px;
      background: var(--color-navy-50);
      color: var(--color-text);
    }
    .text { font-size: 15.5px; line-height: 1.6; white-space: pre-wrap; overflow-wrap: anywhere; }
    .files { display: flex; flex-direction: column; gap: 6px; margin: 2px 0 8px; padding: 0; list-style: none; }
    .files:only-child { margin-bottom: 2px; }
    .file {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 6px 10px;
      border-radius: var(--radius-sm);
      background: var(--color-surface);
      color: var(--color-navy);
      font-size: 13px;
    }
    .file__name { min-width: 0; overflow: hidden; font-weight: 500; text-overflow: ellipsis; white-space: nowrap; }
    .file__size { flex: none; color: var(--color-text-subtle); }
    .time { color: var(--color-text-subtle); font-size: 12px; }
    @keyframes msg-in { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
  `,
})
export class UserMessage {
  readonly message = input.required<UserMessageModel>();
  protected readonly size = formatFileSize;
}
