import { copyFile, mkdir, chmod } from 'node:fs/promises';
import { constants } from 'node:fs';

await Promise.all(['artifacts', '.local', 'runtime'].map((dir) => mkdir(dir, { recursive: true })));
for (const file of ['.env', 'runtime/.env']) {
  try {
    await copyFile(`${file}.example`, file, constants.COPYFILE_EXCL);
    await chmod(file, 0o600);
    console.log(`Created ${file}; credentials stay local.`);
  } catch (error) {
    if (error?.code !== 'EEXIST') throw error;
    console.log(`Kept existing ${file}.`);
  }
}
console.log('Ready. Run npm run check, npm run demo, and npm run doctor.');
