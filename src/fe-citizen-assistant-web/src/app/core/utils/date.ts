/**
 * Dates are evaluated in Vietnam time (UTC+7, no DST) regardless of where the code runs,
 * so server-side rendering and the browser agree on "today" and on displayed times.
 */
export const VN_TIMEZONE_OFFSET = '+0700';

const VN_OFFSET_MS = 7 * 60 * 60 * 1000;
export const DAY_MS = 24 * 60 * 60 * 1000;

/** Timestamp (ms) of 00:00 Vietnam time on the day containing `time`. */
export function startOfVietnamDay(time: number): number {
  return Math.floor((time + VN_OFFSET_MS) / DAY_MS) * DAY_MS - VN_OFFSET_MS;
}
