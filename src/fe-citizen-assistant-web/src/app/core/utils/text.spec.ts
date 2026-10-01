import { formatFileSize, normalizeVietnamese } from './text';

describe('text utils', () => {
  it('normalizes Vietnamese diacritics and case', () => {
    expect(normalizeVietnamese('  Đăng ký KHAI SINH ')).toBe('dang ky khai sinh');
  });

  it('formats file sizes', () => {
    expect(formatFileSize(512)).toBe('512 B');
    expect(formatFileSize(2048)).toBe('2 KB');
    expect(formatFileSize(3.5 * 1024 * 1024)).toBe('3.5 MB');
  });
});
