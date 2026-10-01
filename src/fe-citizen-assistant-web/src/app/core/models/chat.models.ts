/**
 * Domain models for the citizen assistant.
 *
 * Message content is structured (blocks) instead of raw HTML/markdown so the
 * UI can render tables, procedure cards and citations without `innerHTML`.
 * Inline text inside blocks supports a tiny markup, see `InlineMarkupPipe`:
 *   **bold**, ==highlight==, [label](https://url), [^1] (citation to sources[0]).
 */

export type MessageRole = 'user' | 'assistant';

/** Outcome of an assistant turn; drives which state UI is shown. */
export type AssistantStatus =
  | 'complete'
  | 'no-result'
  | 'no-official-source'
  | 'error';

export type SourceKind = 'legal-document' | 'portal' | 'guide';

export interface SourceReference {
  id: string;
  kind: SourceKind;
  title: string;
  /** Issuing body or website owner, e.g. "Cổng thông tin điện tử Chính phủ". */
  publisher: string;
  url: string;
  /** Display domain, e.g. "dichvucong.gov.vn". */
  domain: string;
  /** ISO date (yyyy-mm-dd). */
  updatedAt?: string;
  /** Document number, e.g. "60/2014/QH13". */
  documentNumber?: string;
  /** Short quoted passage shown when the card is expanded. */
  excerpt?: string;
  official: boolean;
}

export type ServiceLevel = 'full-online' | 'partial-online' | 'in-person';

export interface AdministrativeProcedure {
  id: string;
  /** Procedure code on the public service portal, when known. */
  code?: string;
  name: string;
  field: string;
  processingTime: string;
  applicant: string;
  serviceLevel: ServiceLevel;
  fee: string;
  authority: string;
  requiredDocuments: string[];
  legalBasis: string[];
  detailUrl: string;
  /** Online submission link; omitted for procedures done in person. */
  submitUrl?: string;
}

export type CalloutTone = 'info' | 'success' | 'warning';

export type ContentBlock =
  | { type: 'paragraph'; text: string }
  | { type: 'heading'; text: string }
  | { type: 'list'; ordered: boolean; items: string[] }
  | { type: 'table'; caption?: string; headers: string[]; rows: string[][] }
  | { type: 'callout'; tone: CalloutTone; title?: string; text: string }
  | { type: 'procedure'; procedure: AdministrativeProcedure };

export interface Attachment {
  id: string;
  name: string;
  size: number;
  mimeType: string;
  kind: 'file' | 'document';
}

interface BaseMessage {
  id: string;
  role: MessageRole;
  /** ISO timestamp. */
  createdAt: string;
}

export interface UserMessage extends BaseMessage {
  role: 'user';
  text: string;
  attachments: Attachment[];
}

export interface AssistantMessage extends BaseMessage {
  role: 'assistant';
  status: AssistantStatus;
  blocks: ContentBlock[];
  sources: SourceReference[];
  suggestions: SuggestedQuestion[];
  /** Id of the user message this reply answers; used for "retry". */
  replyTo?: string;
  feedback?: 'up' | 'down';
}

export type ChatMessage = UserMessage | AssistantMessage;

export interface Conversation {
  id: string;
  title: string;
  /** ISO timestamp of the last activity, used for history grouping. */
  updatedAt: string;
  messages: ChatMessage[];
}

export type SuggestionCategory = 'dossier' | 'calculation' | 'resettlement' | 'payment';

export interface SuggestedQuestion {
  id: string;
  text: string;
  category?: SuggestionCategory;
}

export interface SuggestionGroup {
  category: SuggestionCategory;
  title: string;
  description: string;
  icon: string;
  question: SuggestedQuestion;
}

/** Reply produced by the assistant backend (or the mock). */
export interface AssistantReply {
  status: Exclude<AssistantStatus, 'error'>;
  blocks: ContentBlock[];
  sources: SourceReference[];
  suggestions: SuggestedQuestion[];
  /** Suggested conversation title when this is the first turn. */
  title?: string;
}

export interface ConversationGroup {
  label: string;
  conversations: Conversation[];
}
