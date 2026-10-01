export type InlineToken =
  | { kind: 'text'; value: string }
  | { kind: 'bold'; value: string }
  | { kind: 'highlight'; value: string }
  | { kind: 'link'; value: string; href: string }
  | { kind: 'cite'; index: number };

const PATTERN = /(\*\*[^*]+\*\*|==[^=]+==|\[[^\]]+\]\(https?:\/\/[^)\s]+\)|\[\^\d+\])/g;

/**
 * Parses the assistant's inline markup into tokens:
 * `**bold**`, `==highlight==`, `[label](https://url)`, `[^n]` (1-based citation).
 * Only http(s) links are recognised; everything else stays plain text.
 */
export function parseInlineMarkup(source: string): InlineToken[] {
  const tokens: InlineToken[] = [];
  let last = 0;
  for (const match of source.matchAll(PATTERN)) {
    const raw = match[0];
    const at = match.index ?? 0;
    if (at > last) tokens.push({ kind: 'text', value: source.slice(last, at) });

    if (raw.startsWith('**')) {
      tokens.push({ kind: 'bold', value: raw.slice(2, -2) });
    } else if (raw.startsWith('==')) {
      tokens.push({ kind: 'highlight', value: raw.slice(2, -2) });
    } else if (raw.startsWith('[^')) {
      tokens.push({ kind: 'cite', index: Number(raw.slice(2, -1)) });
    } else {
      const split = raw.indexOf('](');
      tokens.push({ kind: 'link', value: raw.slice(1, split), href: raw.slice(split + 2, -1) });
    }
    last = at + raw.length;
  }
  if (last < source.length) tokens.push({ kind: 'text', value: source.slice(last) });
  return tokens;
}

/** Plain-text rendering, used for copy-to-clipboard. */
export function stripInlineMarkup(source: string): string {
  return parseInlineMarkup(source)
    .map((t) => (t.kind === 'cite' ? `[${t.index}]` : t.value))
    .join('');
}
