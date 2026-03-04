/**
 * Parser for SKILL.md files
 * Extracts YAML frontmatter and markdown content
 */

/**
 * Parse a SKILL.md file into frontmatter and body
 * @param {string} content - The full content of the SKILL.md file
 * @returns {Object} - { frontmatter: string, body: string, parsed: object }
 */
export function parseSkillFile(content) {
  const lines = content.split('\n');

  if (!lines[0].startsWith('---')) {
    return {
      frontmatter: '',
      body: content,
      parsed: {},
      valid: false,
      error: 'SKILL.md must start with --- (YAML frontmatter delimiter)'
    };
  }

  let endIndex = -1;
  for (let i = 1; i < lines.length; i++) {
    if (lines[i].startsWith('---')) {
      endIndex = i;
      break;
    }
  }

  if (endIndex === -1) {
    return {
      frontmatter: '',
      body: content,
      parsed: {},
      valid: false,
      error: 'SKILL.md must close frontmatter with --- delimiter'
    };
  }

  const frontmatterLines = lines.slice(1, endIndex);
  const frontmatter = frontmatterLines.join('\n');
  const bodyLines = lines.slice(endIndex + 1);
  const body = bodyLines.join('\n').trim();
  const parsed = parseYaml(frontmatter);

  return { frontmatter, body, parsed, valid: true, error: null };
}

/**
 * Parse YAML frontmatter into a plain JS object.
 *
 * Handles the subset used in SKILL.md:
 *   - Scalar values (string, quoted string)
 *   - Nested objects (indentation-based)
 *   - Simple arrays (- value) and object arrays (- key: val ...)
 *   - Block scalars (|) — collected but not deeply processed
 */
function parseYaml(yaml) {
  const lines = yaml.split('\n');

  // Each stack frame: { obj, indent }
  // obj: the current object or array we're writing into
  // indent: the indentation level that OPENS this block
  const stack = [{ obj: {}, indent: -1 }];

  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();
    i++;

    if (!trimmed || trimmed.startsWith('#')) continue;

    const indent = line.search(/\S/); // index of first non-whitespace

    // Pop stack frames that are at a deeper or equal indent than current line
    while (stack.length > 1 && stack[stack.length - 1].indent >= indent) {
      stack.pop();
    }

    const current = stack[stack.length - 1].obj;

    // ── Array item ─────────────────────────────────────────────────────────
    if (trimmed.startsWith('- ')) {
      const itemContent = trimmed.slice(2).trim();

      // Find the array to push into (nearest array in the stack chain)
      let arr = null;
      for (let s = stack.length - 1; s >= 0; s--) {
        if (Array.isArray(stack[s].obj)) { arr = stack[s].obj; break; }
      }
      if (!arr) continue;

      const colonPos = itemContent.indexOf(':');
      if (colonPos === -1) {
        // Simple scalar item: - value
        arr.push(itemContent);
      } else {
        // Object item: - key: value
        const itemObj = {};
        arr.push(itemObj);
        // Parse the first key-value from the same line
        const firstKey = itemContent.slice(0, colonPos).trim();
        const firstVal = itemContent.slice(colonPos + 1).trim();
        if (firstVal && firstVal !== '|' && firstVal !== '>') {
          itemObj[firstKey] = stripQuotes(firstVal);
        }
        // Push the item object so subsequent same-block keys go into it.
        // Use the dash line's own indent — properties at indent+2 will
        // be added to itemObj because indent+2 > indent (won't trigger pop).
        stack.push({ obj: itemObj, indent: indent });
      }
      continue;
    }

    // ── Key: value ─────────────────────────────────────────────────────────
    const colonPos = trimmed.indexOf(':');
    if (colonPos === -1) continue;

    const key = trimmed.slice(0, colonPos).trim();
    const rawVal = trimmed.slice(colonPos + 1).trim();

    if (!rawVal || rawVal === '|' || rawVal === '>') {
      // Block scalar or nested block — peek at next non-empty line
      // to determine if it's an array or object
      let nextNonEmpty = null;
      let nextNonEmptyIndent = 0;
      for (let j = i; j < lines.length; j++) {
        const nextLine = lines[j];
        if (nextLine.trim()) {
          nextNonEmpty = nextLine.trim();
          nextNonEmptyIndent = nextLine.search(/\S/);
          break;
        }
      }

      if (rawVal === '|' || rawVal === '>') {
        // Collect block scalar lines
        let block = '';
        while (i < lines.length) {
          const bLine = lines[i];
          const bIndent = bLine.search(/\S/);
          if (bLine.trim() && bIndent <= indent) break;
          block += bLine + '\n';
          i++;
        }
        current[key] = block.trim();
      } else if (nextNonEmpty && nextNonEmpty.startsWith('- ')) {
        // Array
        const arr = [];
        current[key] = arr;
        stack.push({ obj: arr, indent });
      } else if (nextNonEmptyIndent > indent) {
        // Nested object
        const obj = {};
        current[key] = obj;
        stack.push({ obj, indent });
      }
    } else {
      // Scalar value on same line
      current[key] = stripQuotes(rawVal);
    }
  }

  return stack[0].obj;
}

function stripQuotes(val) {
  if (!val) return val;
  if ((val.startsWith('"') && val.endsWith('"')) ||
      (val.startsWith("'") && val.endsWith("'"))) {
    return val.slice(1, -1);
  }
  return val;
}

/**
 * Extract metadata structure from parsed SKILL
 */
export function extractMetadata(parsed) {
  return {
    name: parsed.name || '',
    description: parsed.description || '',
    metadata: parsed.metadata || {},
    emoji: parsed.metadata?.openclaw?.emoji || '',
    requires: parsed.metadata?.openclaw?.requires || {},
    install: parsed.metadata?.openclaw?.install || []
  };
}
