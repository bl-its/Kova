import { describe, expect, it } from 'vitest';
import { parseDocument } from '../parser/markdownToSlides';

describe('raw HTML rendering', () => {
  it('preserves inline HTML inside Markdown paragraphs', () => {
    const doc = parseDocument('## Demo\n\nText <span style="color:red">red</span>.');
    const paragraph = doc.slides[0].elements[0];
    expect(paragraph.type).toBe('paragraph');
    if (paragraph.type === 'paragraph') {
      expect(paragraph.html).toContain('<span style="color:red">red</span>');
      expect(paragraph.rawHtml).toBeUndefined();
    }
  });

  it('preserves block HTML and keeps a plain-text projection', () => {
    const doc = parseDocument('## Demo\n\n<div style="display:grid"><strong>Hello</strong></div>');
    const paragraph = doc.slides[0].elements[0];
    expect(paragraph.type).toBe('paragraph');
    if (paragraph.type === 'paragraph') {
      expect(paragraph.rawHtml).toBe(true);
      expect(paragraph.html).toContain('display:grid');
      expect(paragraph.text).toBe('Hello');
    }
  });

  it('drops style contents from the PPTX plain-text projection', () => {
    const doc = parseDocument('## Demo\n\n<style>.demo { color: red; }</style>');
    const paragraph = doc.slides[0].elements[0];
    expect(paragraph.type).toBe('paragraph');
    if (paragraph.type === 'paragraph') {
      expect(paragraph.rawHtml).toBe(true);
      expect(paragraph.html).toContain('<style>');
      expect(paragraph.text).toBe('');
    }
  });
});
