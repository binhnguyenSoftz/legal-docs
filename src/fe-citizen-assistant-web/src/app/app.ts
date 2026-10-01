import { ChangeDetectionStrategy, Component } from '@angular/core';
import { ChatbotPage } from './features/chatbot/chatbot-page/chatbot-page';

@Component({
  selector: 'app-root',
  imports: [ChatbotPage],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: '<app-chatbot-page />',
})
export class App {}
