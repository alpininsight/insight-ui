// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Tests for the table of contents generator: the generated lists keep their list semantics.
 */

import { describe, it, expect, beforeAll, beforeEach } from 'vitest';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const script = path.join(__dirname, '../../insight_ui/static/insight_ui/js/insight-ui-toc-generator.js');

beforeAll(() => {
  // A classic script: expose its class the way a page would reach it.
  const code = fs.readFileSync(script, 'utf-8');
  eval(`${code}\nwindow.TableOfContents = TableOfContents;`);
});

describe('TableOfContents', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <main id="content">
        <h1>Install</h1>
        <h2>Requirements</h2>
        <h2>Package</h2>
        <h1>Usage</h1>
      </main>
      <div id="toc"></div>
    `;
  });

  it('marks every generated list as a list, so Safari keeps it one without markers', () => {
    new window.TableOfContents({ contentSelector: 'content', tocSelector: 'toc' });

    const lists = document.querySelectorAll('#toc ul');
    expect(lists.length).toBeGreaterThan(1);
    lists.forEach(list => expect(list.getAttribute('role')).toBe('list'));
    expect(document.querySelectorAll('#toc li a')).toHaveLength(4);
  });
});
