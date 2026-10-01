import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import { Organization } from '../../../core/config/organization';
import { SuggestedQuestion as SuggestedQuestionModel, SuggestionGroup } from '../../../core/models/chat.models';
import { AssistantAvatar } from '../../../shared/components/assistant-avatar/assistant-avatar';
import { Icon } from '../../../shared/components/icon/icon';

@Component({
  selector: 'app-chat-welcome',
  imports: [Icon, AssistantAvatar],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './chat-welcome.html',
  styleUrl: './chat-welcome.scss',
})
export class ChatWelcome {
  readonly organization = input.required<Organization>();
  readonly userName = input('');
  readonly groups = input.required<SuggestionGroup[]>();
  readonly popular = input<SuggestedQuestionModel[]>([]);
  readonly disabled = input(false);
  readonly ask = output<SuggestedQuestionModel>();
}
