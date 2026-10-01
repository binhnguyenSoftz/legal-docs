import {
  ChangeDetectionStrategy,
  Component,
  ElementRef,
  computed,
  inject,
  input,
  output,
  signal,
  viewChild,
} from '@angular/core';
import { MatTooltipModule } from '@angular/material/tooltip';
import { Attachment } from '../../../core/models/chat.models';
import { VoiceInputService } from '../../../core/services/voice-input.service';
import { createId, formatFileSize } from '../../../core/utils/text';
import { Icon } from '../../../shared/components/icon/icon';

export interface ChatSubmit {
  text: string;
  attachments: Attachment[];
}

const MAX_LENGTH = 2000;
const MAX_FILES = 5;
const MAX_FILE_SIZE = 10 * 1024 * 1024;
const MAX_TEXTAREA_HEIGHT = 200;

@Component({
  selector: 'app-chat-input',
  imports: [Icon, MatTooltipModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './chat-input.html',
  styleUrl: './chat-input.scss',
})
export class ChatInput {
  protected readonly voice = inject(VoiceInputService);

  readonly busy = input(false);
  readonly submitted = output<ChatSubmit>();
  readonly stopped = output<void>();

  private readonly textarea = viewChild.required<ElementRef<HTMLTextAreaElement>>('textarea');

  protected readonly maxLength = MAX_LENGTH;
  protected readonly text = signal('');
  protected readonly attachments = signal<Attachment[]>([]);
  protected readonly fileError = signal<string | null>(null);
  protected readonly focused = signal(false);

  protected readonly canSend = computed(
    () => !this.busy() && (this.text().trim().length > 0 || this.attachments().length > 0),
  );
  protected readonly nearLimit = computed(() => this.text().length > MAX_LENGTH * 0.8);
  protected readonly size = formatFileSize;

  focus(): void {
    this.textarea().nativeElement.focus();
  }

  protected onInput(value: string): void {
    this.text.set(value);
    this.autosize();
  }

  protected onKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
      event.preventDefault();
      this.submit();
    }
  }

  protected submit(): void {
    if (!this.canSend()) return;
    if (this.voice.listening()) this.voice.stop();
    this.submitted.emit({ text: this.text().trim(), attachments: this.attachments() });
    this.setText('');
    this.attachments.set([]);
    this.fileError.set(null);
  }

  protected toggleVoice(): void {
    if (this.voice.listening()) {
      this.voice.stop();
      return;
    }
    const prefix = this.text().trim();
    this.voice.start((spoken) => {
      this.setText(prefix ? `${prefix} ${spoken}` : spoken);
    });
  }

  protected onFiles(input: HTMLInputElement, kind: Attachment['kind']): void {
    const files = Array.from(input.files ?? []);
    input.value = '';
    const current = this.attachments();
    const accepted: Attachment[] = [];
    let error: string | null = null;

    for (const file of files) {
      if (current.length + accepted.length >= MAX_FILES) {
        error = `Chỉ được đính kèm tối đa ${MAX_FILES} tệp.`;
        break;
      }
      if (file.size > MAX_FILE_SIZE) {
        error = `Tệp "${file.name}" vượt quá dung lượng ${formatFileSize(MAX_FILE_SIZE)}.`;
        continue;
      }
      accepted.push({ id: createId('f'), name: file.name, size: file.size, mimeType: file.type, kind });
    }

    this.attachments.set([...current, ...accepted]);
    this.fileError.set(error);
  }

  protected removeAttachment(id: string): void {
    this.attachments.update((list) => list.filter((a) => a.id !== id));
    this.fileError.set(null);
  }

  /**
   * Writes both the signal and the element: with zoneless change detection a quick
   * input + submit can leave the [value] binding unchanged ('' -> '') and the DOM stale.
   */
  private setText(value: string): void {
    this.text.set(value);
    this.textarea().nativeElement.value = value;
    this.autosize();
  }

  private autosize(): void {
    const el = this.textarea().nativeElement;
    el.style.height = 'auto';
    el.style.height = `${Math.min(el.scrollHeight, MAX_TEXTAREA_HEIGHT)}px`;
  }
}
