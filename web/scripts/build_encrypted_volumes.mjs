import { readFile, writeFile, mkdir, rm } from 'node:fs/promises';
import { webcrypto } from 'node:crypto';
import path from 'node:path';

// Build-time key shared with app.js. This is obfuscation for static hosting, not DRM.
const KEY_HEX = '5f907a1d7ff6e8cc7a20c9200a7b043ff8bdcc525431298eedb011179dc0d579';
const key = await webcrypto.subtle.importKey('raw', Buffer.from(KEY_HEX, 'hex'), 'AES-GCM', false, ['encrypt']);
const sourceRoot = process.argv[2] || 'source-volumes';
const manifestPath = 'data.js';
const manifestSource = await readFile(manifestPath, 'utf8');
const manifest = JSON.parse(manifestSource.slice(manifestSource.indexOf('=') + 1).trim().replace(/;$/, ''));

for (const [number, entry] of Object.entries(manifest)) {
  const sourcePath = path.join(sourceRoot, `${entry.slug}.js`);
  const source = await readFile(sourcePath, 'utf8');
  const jsonText = source.slice(source.lastIndexOf('=') + 1).trim().replace(/;$/, '');
  const volume = JSON.parse(jsonText);
  const directory = `encrypted/${entry.slug}`;
  await rm(directory, { recursive: true, force: true });
  await mkdir(directory, { recursive: true });

  const chapters = [];
  for (const chapter of volume.chapters) {
    const payload = Buffer.from(JSON.stringify(chapter));
    const iv = webcrypto.getRandomValues(new Uint8Array(12));
    const encrypted = await webcrypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, payload);
    const filename = `${chapter.id}.js`;
    const chunkKey = `${number}/${chapter.id}`;
    const encryptedPayload = JSON.stringify({
      iv: Buffer.from(iv).toString('base64'),
      data: Buffer.from(encrypted).toString('base64'),
    });
    await writeFile(path.join(directory, filename), `window.MUSOKU_ENCRYPTED_CHUNKS = window.MUSOKU_ENCRYPTED_CHUNKS || {}; window.MUSOKU_ENCRYPTED_CHUNKS[${JSON.stringify(chunkKey)}] = ${encryptedPayload};\n`);
    chapters.push({
      ...chapter,
      scenes: chapter.scenes.map(({ id, location, cast }) => ({ id, location, cast })),
      chunk: `${directory}/${filename}`,
    });
  }

  const metadata = {
    meta: volume.meta,
    stats: volume.stats,
    chapters,
    speakers: volume.speakers,
    images: volume.images,
  };
  await writeFile(path.join(directory, 'meta.js'), `window.MUSOKU_VOLUME_DATA = window.MUSOKU_VOLUME_DATA || {}; window.MUSOKU_VOLUME_DATA[${JSON.stringify(number)}] = ${JSON.stringify(metadata)};\n`);
  entry.file = `${directory}/meta.js`;
  entry.encrypted = true;
}

await writeFile(manifestPath, `window.MUSOKU_MANIFEST = ${JSON.stringify(manifest)};\n`);
