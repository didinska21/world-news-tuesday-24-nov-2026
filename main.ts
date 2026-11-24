// Entry point for the "Sum up 24 November's world news in one image"
// entry. The deliverable is the drawn front page, entry.png, which
// sits next to this file; running the entry copies it, byte for
// byte, to /output/entry.png.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
mkdirSync("/output", { recursive: true });
copyFileSync(join(here, "entry.png"), "/output/entry.png");
