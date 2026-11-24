// Validates every example event against its JSON Schema (draft 2020-12).
const Ajv2020 = require('ajv/dist/2020'); const addFormats = require('ajv-formats');
const fs = require('fs'); const path = require('path');
const dir = process.argv[2] || 'docs/api/events'; const exDir = process.argv[3] || 'docs/api/examples';
const ajv = new Ajv2020({ strict: false, allErrors: true }); addFormats(ajv);
ajv.addSchema(JSON.parse(fs.readFileSync(path.join(dir, 'envelope.schema.json'))));
let fail = 0;
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.schema.json') && f !== 'envelope.schema.json')) {
  const schema = JSON.parse(fs.readFileSync(path.join(dir, f))); const v = ajv.compile(schema);
  const name = f.replace('.schema.json', ''); const ex = JSON.parse(fs.readFileSync(path.join(exDir, name + '.json')));
  const ok = v(ex); console.log((ok ? 'PASS ' : 'FAIL ') + name); if (!ok) { fail++; console.log(v.errors); }
  const bad = JSON.parse(JSON.stringify(ex)); bad.data.disabilityStatus = 'visual';
  const leak = v(bad); console.log((leak ? 'FAIL ' : 'PASS ') + name + ' rejects extra field disabilityStatus'); if (leak) fail++;
}
process.exit(fail ? 1 : 0);
