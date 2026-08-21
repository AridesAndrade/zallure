import { cp, mkdir, readdir, readFile, rename, rm, writeFile } from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const dist = path.join(root, 'dist');
const landing = path.join(dist, 'landingpage');

await rm(landing, { recursive: true, force: true });
await mkdir(landing, { recursive: true });

for (const entry of await readdir(dist)) {
  if (entry === 'landingpage') continue;
  await rename(path.join(dist, entry), path.join(landing, entry));
}

const sesa = await readFile(path.join(root, 'SESA', 'index.html'), 'utf8');
const rootPage = sesa.replaceAll('../assets/', 'assets/');
await writeFile(path.join(dist, 'index.html'), rootPage, 'utf8');

const assets = path.join(root, 'assets');
await cp(assets, path.join(dist, 'assets'), { recursive: true, force: true });

console.log('SESA publicado na raiz; landing antiga preservada em /landingpage/.');
