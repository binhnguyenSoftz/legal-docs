import { TestBed } from '@angular/core/testing';
import { firstValueFrom } from 'rxjs';
import { POPULAR_QUESTIONS, SUGGESTION_GROUPS } from '../mocks/mock-replies';
import { MockAssistantGateway } from './assistant-gateway';

describe('MockAssistantGateway', () => {
  let gateway: MockAssistantGateway;
  const ask = (question: string) =>
    firstValueFrom(gateway.ask({ conversationId: 'c', question, history: [], attachmentNames: [] }));
  const titleOf = async (question: string) => (await ask(question)).title;

  beforeEach(() => {
    gateway = TestBed.inject(MockAssistantGateway);
    gateway.latency = { min: 0, max: 0 };
  });

  it('maps every suggestion shown on the welcome screen to the intended answer', async () => {
    const expected = [
      'Hồ sơ nhận bồi thường khi người đứng tên đã mất',
      'Cách tính tiền bồi thường',
      'Điều kiện tái định cư',
      'Tiến độ chi trả bồi thường',
    ];
    expect(await Promise.all(SUGGESTION_GROUPS.map((g) => titleOf(g.question.text)))).toEqual(expected);
    expect(await Promise.all(POPULAR_QUESTIONS.map((q) => titleOf(q.text)))).toEqual([
      'Hồ sơ nhận bồi thường khi người đứng tên đã mất',
      'Đất mua bằng giấy tay',
      'Thưởng bàn giao mặt bằng',
    ]);
  });

  it('prefers the specific intent when several keywords match', async () => {
    expect(await titleOf('Không đồng ý với mức bồi thường thì khiếu nại ở đâu?')).toBe('Khiếu nại về bồi thường');
    expect(await titleOf('Chưa có nhà tái định cư thì được hỗ trợ tạm cư không?')).toBe('Hỗ trợ tạm cư');
    expect(await titleOf('Nhà không có giấy phép xây dựng có được bồi thường không?')).toBe('Nhà xây không phép');
  });

  it('redirects topics outside land-recovery compensation', async () => {
    expect(await titleOf('Đăng ký khai sinh cho con')).toBe('Ngoài phạm vi hỗ trợ');
    expect(await titleOf('Xin giấy phép xây dựng nhà ở')).toBe('Ngoài phạm vi hỗ trợ');
  });

  it('matches whole syllables only and falls back to no-result', async () => {
    // "tình" and "tính" both normalize to "tinh"; the status intent is ordered before the calculation one.
    expect(await titleOf('Tình trạng hồ sơ bồi thường của tôi')).toBe('Tiến độ chi trả bồi thường');
    expect((await ask('Thời tiết hôm nay thế nào')).status).toBe('no-result');
  });
});
