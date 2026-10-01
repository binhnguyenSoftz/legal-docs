import { startOfVietnamDay } from './date';

describe('startOfVietnamDay', () => {
  it('uses UTC+7 midnight regardless of the runtime timezone', () => {
    // 2026-10-01 18:30 UTC is 2026-10-02 01:30 in Vietnam.
    expect(new Date(startOfVietnamDay(Date.UTC(2026, 9, 1, 18, 30))).toISOString()).toBe('2026-10-01T17:00:00.000Z');
    // 2026-10-01 10:00 UTC is still 2026-10-01 in Vietnam.
    expect(new Date(startOfVietnamDay(Date.UTC(2026, 9, 1, 10, 0))).toISOString()).toBe('2026-09-30T17:00:00.000Z');
  });
});
