import { A11yModule, CdkTrapFocus } from '@angular/cdk/a11y';
import { BreakpointObserver } from '@angular/cdk/layout';
import { DOCUMENT } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  Injector,
  afterNextRender,
  computed,
  effect,
  inject,
  signal,
  viewChild,
} from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { map } from 'rxjs';
import { ORGANIZATION } from '../../../core/config/organization';
import { POPULAR_QUESTIONS, SUGGESTION_GROUPS } from '../../../core/mocks/mock-replies';
import { AssistantMessage, Conversation, SuggestedQuestion } from '../../../core/models/chat.models';
import { ChatService } from '../../../core/services/chat.service';
import { ConversationService } from '../../../core/services/conversation.service';
import { CurrentUser, GovernmentHeader, NavLink } from '../../../shared/components/government-header/government-header';
import { Icon } from '../../../shared/components/icon/icon';
import { ChatConversation, FeedbackEvent } from '../chat-conversation/chat-conversation';
import { ChatInput, ChatSubmit } from '../chat-input/chat-input';
import { ChatSidebar } from '../chat-sidebar/chat-sidebar';
import { ChatWelcome } from '../chat-welcome/chat-welcome';

const MOBILE = '(max-width: 767px)';
const TABLET = '(max-width: 1199px)';
const SCROLL_BUTTON_THRESHOLD = 320;

@Component({
  selector: 'app-chatbot-page',
  imports: [A11yModule, MatSnackBarModule, Icon, GovernmentHeader, ChatSidebar, ChatWelcome, ChatConversation, ChatInput],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './chatbot-page.html',
  styleUrl: './chatbot-page.scss',
  host: {
    '(document:keydown)': 'onGlobalKeydown($event)',
  },
})
export class ChatbotPage {
  protected readonly conversations = inject(ConversationService);
  protected readonly chat = inject(ChatService);
  private readonly snackBar = inject(MatSnackBar);
  private readonly breakpoints = inject(BreakpointObserver);

  private readonly injector = inject(Injector);
  private readonly document = inject(DOCUMENT);
  private readonly chatInput = viewChild.required(ChatInput);
  private readonly focusTrap = viewChild.required(CdkTrapFocus);
  /** Element that opened the drawer, refocused when it closes. */
  private drawerOpener: HTMLElement | null = null;

  protected readonly organization = ORGANIZATION;
  protected readonly user: CurrentUser = { fullName: 'Nguyễn Minh Anh', identityLevel: 'Định danh điện tử mức 2' };
  protected readonly navLinks: NavLink[] = [
    { label: 'Hỏi đáp bồi thường', href: '#', icon: 'chat', active: true },
    { label: 'Dự án thu hồi đất', href: '#', icon: 'map' },
    { label: 'Văn bản áp dụng', href: '#', icon: 'scale' },
    { label: 'Liên hệ', href: '#', icon: 'help' },
  ];
  protected readonly suggestionGroups = SUGGESTION_GROUPS;
  protected readonly popularQuestions = POPULAR_QUESTIONS;

  protected readonly isMobile = toSignal(this.breakpoints.observe(MOBILE).pipe(map((s) => s.matches)), {
    initialValue: false,
  });
  private readonly isTablet = toSignal(this.breakpoints.observe(TABLET).pipe(map((s) => s.matches)), {
    initialValue: false,
  });

  /** Desktop/tablet rail state; tablet starts collapsed. */
  protected readonly collapsed = signal(false);
  /** Mobile drawer state. */
  protected readonly drawerOpen = signal(false);
  protected readonly showScrollButton = signal(false);

  protected readonly sidebarCollapsed = computed(() => !this.isMobile() && this.collapsed());

  constructor() {
    effect(() => this.collapsed.set(this.isTablet() && !this.isMobile()));
    effect(() => {
      if (!this.isMobile()) this.drawerOpen.set(false);
    });
  }

  protected newConversation(): void {
    this.conversations.startNew();
    this.closeDrawer(false);
    queueMicrotask(() => this.chatInput().focus());
  }

  protected selectConversation(conversation: Conversation): void {
    this.conversations.select(conversation.id);
    this.closeDrawer(false);
  }

  protected removeConversation(conversation: Conversation): void {
    this.conversations.delete(conversation.id);
    this.snackBar
      .open(`Đã xóa "${conversation.title}"`, 'Hoàn tác', { duration: 5000 })
      .onAction()
      .subscribe(() => this.conversations.restore(conversation));
  }

  protected send({ text, attachments }: ChatSubmit): void {
    this.chat.send(text, attachments);
  }

  protected ask(question: SuggestedQuestion): void {
    this.chat.send(question.text);
  }

  protected retry(message: AssistantMessage): void {
    this.chat.retry(message);
  }

  protected feedback({ message, value }: FeedbackEvent): void {
    this.chat.setFeedback(message, value);
    if (message.feedback !== value) {
      this.snackBar.open('Cảm ơn bạn đã đánh giá câu trả lời.', undefined, { duration: 2500 });
    }
  }

  protected toggleSidebar(): void {
    if (!this.isMobile()) {
      this.collapsed.update((v) => !v);
    } else if (this.drawerOpen()) {
      this.closeDrawer();
    } else {
      this.drawerOpener = this.document.activeElement as HTMLElement | null;
      this.drawerOpen.set(true);
      afterNextRender(() => this.focusTrap().focusTrap.focusInitialElement(), { injector: this.injector });
    }
  }

  protected closeDrawer(restoreFocus = true): void {
    if (!this.drawerOpen()) return;
    this.drawerOpen.set(false);
    if (restoreFocus) this.drawerOpener?.focus();
    this.drawerOpener = null;
  }

  protected onScroll(el: HTMLElement): void {
    this.showScrollButton.set(el.scrollHeight - el.scrollTop - el.clientHeight > SCROLL_BUTTON_THRESHOLD);
  }

  protected scrollToBottom(el: HTMLElement): void {
    el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' });
  }

  protected onGlobalKeydown(event: KeyboardEvent): void {
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
      event.preventDefault();
      this.newConversation();
    } else if (event.key === 'Escape' && this.drawerOpen()) {
      this.closeDrawer();
    }
  }
}
