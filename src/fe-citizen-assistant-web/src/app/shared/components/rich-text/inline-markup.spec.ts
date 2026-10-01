import { parseInlineMarkup, stripInlineMarkup } from './inline-markup';

describe('parseInlineMarkup', () => {
  it('splits bold, highlight, links and citations', () => {
    expect(parseInlineMarkup('Cần **tờ khai**, ==60 ngày== [^1] tại [Cổng DVC](https://dichvucong.gov.vn).')).toEqual([
      { kind: 'text', value: 'Cần ' },
      { kind: 'bold', value: 'tờ khai' },
      { kind: 'text', value: ', ' },
      { kind: 'highlight', value: '60 ngày' },
      { kind: 'text', value: ' ' },
      { kind: 'cite', index: 1 },
      { kind: 'text', value: ' tại ' },
      { kind: 'link', value: 'Cổng DVC', href: 'https://dichvucong.gov.vn' },
      { kind: 'text', value: '.' },
    ]);
  });

  it('leaves non-http links as plain text', () => {
    expect(parseInlineMarkup('[x](javascript:alert(1))')).toEqual([{ kind: 'text', value: '[x](javascript:alert(1))' }]);
  });

  it('strips markup for copying', () => {
    expect(stripInlineMarkup('**A** ==B== [C](https://c.vn) [^2]')).toBe('A B C [2]');
  });
});
