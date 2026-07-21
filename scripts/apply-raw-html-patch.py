from pathlib import Path


def replace(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    if old not in text:
        raise SystemExit(f'Expected text not found in {path}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8')

replace(
    'src/engine/types.ts',
    "| { type: 'paragraph'; text: string; html: string }",
    "| { type: 'paragraph'; text: string; html: string; rawHtml?: boolean }",
)

replace(
    'src/engine/parser/markdownToSlides.ts',
    """          } else if (v === '<hr>' || v === '<hr/>' || v === '<hr />') {
            elements.push({ type: 'paragraph', text: '', html: '<hr>' });
          }
""",
    """          } else if (v === '<hr>' || v === '<hr/>' || v === '<hr />') {
            elements.push({ type: 'paragraph', text: '', html: '<hr>' });
          } else {
            // Preserve trusted raw block HTML. The plain-text projection keeps
            // auto-layout and PPTX export working without a separate HTML model.
            elements.push({ type: 'paragraph', text: stripHtml(v), html: v, rawHtml: true });
          }
""",
)

replace(
    'src/engine/parser/markdownToSlides.ts',
    """      case 'break':       return '<br>';
      case 'inlineMath': {
""",
    """      case 'break':       return '<br>';
      case 'html':        return node.value as string;
      case 'inlineMath': {
""",
)

replace(
    'src/components/preview/elements.tsx',
    """    case 'paragraph':
      return <p className=\"sl-para\" dangerouslySetInnerHTML={{ __html: el.html }} />;
""",
    """    case 'paragraph':
      return el.rawHtml
        ? <div className=\"sl-para sl-raw-html\" dangerouslySetInnerHTML={{ __html: el.html }} />
        : <p className=\"sl-para\" dangerouslySetInnerHTML={{ __html: el.html }} />;
""",
)

Path('src/engine/__tests__/rawHtml.test.ts').write_text("""import { describe, expect, it } from 'vitest';
import { parseDocument } from '../parser/markdownToSlides';

describe('raw HTML rendering', () => {
  it('preserves inline HTML inside Markdown paragraphs', () => {
    const doc = parseDocument('## Demo\\n\\nText <span style=\"color:red\">red</span>.');
    const paragraph = doc.slides[0].elements[0];
    expect(paragraph.type).toBe('paragraph');
    if (paragraph.type === 'paragraph') {
      expect(paragraph.html).toContain('<span style=\"color:red\">red</span>');
      expect(paragraph.rawHtml).toBeUndefined();
    }
  });

  it('preserves block HTML and keeps a plain-text projection', () => {
    const doc = parseDocument('## Demo\\n\\n<div style=\"display:grid\"><strong>Hello</strong></div>');
    const paragraph = doc.slides[0].elements[0];
    expect(paragraph.type).toBe('paragraph');
    if (paragraph.type === 'paragraph') {
      expect(paragraph.rawHtml).toBe(true);
      expect(paragraph.html).toContain('display:grid');
      expect(paragraph.text).toBe('Hello');
    }
  });
});
""", encoding='utf-8')
