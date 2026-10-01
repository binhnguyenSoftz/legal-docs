import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import { MatTooltipModule } from '@angular/material/tooltip';
import { Conversation, ConversationGroup } from '../../../core/models/chat.models';
import { Icon } from '../../../shared/components/icon/icon';
import { ConversationList } from './conversation-list/conversation-list';
import { ConversationSearch } from './conversation-search/conversation-search';
import { NewConversationButton } from './new-conversation-button/new-conversation-button';

interface FooterLink {
  label: string;
  icon: string;
}

/**
 * Presentational sidebar. `collapsed` renders the icon rail (desktop/tablet);
 * `drawer` renders the mobile variant with a close button.
 */
@Component({
  selector: 'app-chat-sidebar',
  imports: [Icon, MatTooltipModule, NewConversationButton, ConversationSearch, ConversationList],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './chat-sidebar.html',
  styleUrl: './chat-sidebar.scss',
  host: { '[class.collapsed]': 'collapsed()', '[class.drawer]': 'drawer()' },
})
export class ChatSidebar {
  readonly groups = input.required<ConversationGroup[]>();
  readonly activeId = input<string | null>(null);
  readonly query = input('');
  readonly collapsed = input(false);
  readonly drawer = input(false);

  readonly create = output<void>();
  readonly select = output<Conversation>();
  readonly remove = output<Conversation>();
  readonly queryChange = output<string>();
  readonly toggleCollapsed = output<void>();
  readonly close = output<void>();

  protected readonly footerLinks: FooterLink[] = [
    { label: 'Cài đặt', icon: 'settings' },
    { label: 'Trợ giúp', icon: 'help' },
    { label: 'Thông tin hệ thống', icon: 'info' },
  ];
}
