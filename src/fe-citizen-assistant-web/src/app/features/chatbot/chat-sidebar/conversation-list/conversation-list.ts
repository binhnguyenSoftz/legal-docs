import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import { MatMenuModule } from '@angular/material/menu';
import { Conversation, ConversationGroup } from '../../../../core/models/chat.models';
import { Icon } from '../../../../shared/components/icon/icon';

@Component({
  selector: 'app-conversation-list',
  imports: [Icon, MatMenuModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './conversation-list.html',
  styleUrl: './conversation-list.scss',
})
export class ConversationList {
  readonly groups = input.required<ConversationGroup[]>();
  readonly activeId = input<string | null>(null);
  readonly searching = input(false);

  readonly select = output<Conversation>();
  readonly remove = output<Conversation>();
}
