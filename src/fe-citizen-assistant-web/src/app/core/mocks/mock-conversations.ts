import { AssistantReply, ChatMessage, Conversation } from '../models/chat.models';
import { startOfVietnamDay } from '../utils/date';
import { CALCULATION_REPLY, DOSSIER_REPLY, MOCK_INTENTS } from './mock-replies';

const HOUR = 60 * 60 * 1000;
const DAY = 24 * HOUR;

function exchange(id: string, question: string, reply: AssistantReply, at: number): ChatMessage[] {
  return [
    { id: `${id}-u`, role: 'user', text: question, attachments: [], createdAt: new Date(at).toISOString() },
    {
      id: `${id}-a`,
      role: 'assistant',
      status: reply.status,
      blocks: reply.blocks,
      sources: reply.sources,
      suggestions: reply.suggestions,
      replyTo: `${id}-u`,
      createdAt: new Date(at + 4000).toISOString(),
    },
  ];
}

function replyFor(title: string): AssistantReply {
  return MOCK_INTENTS.find((i) => i.reply.title === title)!.reply;
}

/** History seeded relative to `now` so the "Hôm nay / Hôm qua" groups always render. */
export function createMockConversations(now = Date.now()): Conversation[] {
  const startOfToday = startOfVietnamDay(now);
  // Today's items stay within today even right after midnight.
  const today = (minutesAgo: number) => Math.max(now - minutesAgo * 60_000, startOfToday + 1000) - 4000;
  const seed: [string, string, string, AssistantReply, number][] = [
    ['c-1', 'Hồ sơ khi người đứng tên đã mất', 'Ba tôi đứng tên sổ nhà nhưng đã mất, nhà nằm trong dự án bị thu hồi. Gia đình cần chuẩn bị giấy tờ gì để nhận bồi thường?', DOSSIER_REPLY, today(20)],
    ['c-2', 'Cách tính tiền bồi thường đất', 'Nhà tôi bị thu hồi 68,5 m², tiền bồi thường đất được tính thế nào?', CALCULATION_REPLY, today(90) - 1000],
    ['c-3', 'Thưởng bàn giao mặt bằng sớm', 'Nếu gia đình bàn giao mặt bằng sớm thì được thưởng bao nhiêu?', replyFor('Thưởng bàn giao mặt bằng'), startOfToday - 6 * HOUR],
    ['c-4', 'Điều kiện tái định cư', 'Nhà bị thu hồi hết, gia đình không còn chỗ ở khác thì có được tái định cư không?', replyFor('Điều kiện tái định cư'), startOfToday - 10 * HOUR],
    ['c-5', 'Đất mua bằng giấy tay', 'Đất nhà tôi mua bằng giấy tay từ năm 1990, có được bồi thường không?', replyFor('Đất mua bằng giấy tay'), startOfToday - 3 * DAY],
    ['c-6', 'Khiếu nại mức bồi thường', 'Tôi không đồng ý với mức bồi thường thì khiếu nại ở đâu?', replyFor('Khiếu nại về bồi thường'), startOfToday - 5 * DAY],
  ];

  return seed.map(([id, title, question, reply, at]) => ({
    id,
    title,
    updatedAt: new Date(at + 4000).toISOString(),
    messages: exchange(id, question, reply, at),
  }));
}
