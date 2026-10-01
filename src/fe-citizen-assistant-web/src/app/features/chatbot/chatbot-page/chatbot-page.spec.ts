import { TestBed } from '@angular/core/testing';
import { ChatbotPage } from './chatbot-page';

describe('ChatbotPage', () => {
  it('renders the header, history and welcome screen', async () => {
    const fixture = TestBed.createComponent(ChatbotPage);
    await fixture.whenStable();
    const el = fixture.nativeElement as HTMLElement;

    expect(el.querySelector('.brand__name')?.textContent).toContain('Phòng Kinh tế, Hạ tầng và Đô thị');
    expect(el.querySelector('.brand__parent')?.textContent).toContain('UBND phường Bình Đông');
    expect(el.querySelector('#welcome-title')?.textContent).toContain('tôi có thể hỗ trợ gì cho bạn?');
    expect(el.querySelectorAll('.topic').length).toBe(4);
    expect(el.textContent).toContain('Hồ sơ khi người đứng tên đã mất');
    expect(el.querySelector('.hero__lead')?.textContent).toContain('bồi thường, hỗ trợ');
  });
});
