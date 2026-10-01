import { Injectable, signal } from '@angular/core';

/** Minimal typing for the (still prefixed) Web Speech API. */
interface SpeechRecognitionLike {
  lang: string;
  interimResults: boolean;
  continuous: boolean;
  onresult: ((event: { results: ArrayLike<ArrayLike<{ transcript: string }> & { isFinal: boolean }> }) => void) | null;
  onerror: ((event: { error: string }) => void) | null;
  onend: (() => void) | null;
  start(): void;
  stop(): void;
}

type SpeechRecognitionCtor = new () => SpeechRecognitionLike;

/** Vietnamese speech-to-text via the browser's Web Speech API, when available. */
@Injectable({ providedIn: 'root' })
export class VoiceInputService {
  private readonly ctor: SpeechRecognitionCtor | undefined =
    typeof window === 'undefined'
      ? undefined
      : ((window as unknown as Record<string, SpeechRecognitionCtor | undefined>)['SpeechRecognition'] ??
        (window as unknown as Record<string, SpeechRecognitionCtor | undefined>)['webkitSpeechRecognition']);
  private recognition?: SpeechRecognitionLike;

  readonly supported = !!this.ctor;
  readonly listening = signal(false);
  readonly error = signal<string | null>(null);

  /** Starts listening; `onText` receives the running transcript (interim + final). */
  start(onText: (text: string) => void): void {
    if (!this.ctor || this.listening()) return;
    const recognition = new this.ctor();
    recognition.lang = 'vi-VN';
    recognition.interimResults = true;
    recognition.continuous = false;
    recognition.onresult = (event) => onText(Array.from(event.results, (r) => r[0].transcript).join(' '));
    recognition.onerror = (event) =>
      this.error.set(
        event.error === 'not-allowed'
          ? 'Bạn chưa cho phép sử dụng micro.'
          : 'Không nhận diện được giọng nói. Vui lòng thử lại.',
      );
    recognition.onend = () => this.listening.set(false);

    this.error.set(null);
    this.recognition = recognition;
    this.listening.set(true);
    recognition.start();
  }

  stop(): void {
    this.recognition?.stop();
    this.listening.set(false);
  }
}
