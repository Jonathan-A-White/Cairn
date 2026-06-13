// Generates the PNG app icons (a cairn: stacked stones on a dark ground)
// without any image library, by drawing into an RGBA buffer and encoding a
// PNG with Node's built-in zlib. Run: node scripts/gen-icons.mjs
import { deflateSync } from "node:zlib";
import { writeFileSync, mkdirSync } from "node:fs";

const BG = [31, 41, 55, 255]; // #1f2937
const STONE_A = [226, 232, 240, 255]; // #e2e8f0
const STONE_B = [203, 213, 225, 255]; // #cbd5e1

function crc32(buf) {
  let c = ~0;
  for (let i = 0; i < buf.length; i++) {
    c ^= buf[i];
    for (let k = 0; k < 8; k++) c = (c >>> 1) ^ (0xedb88320 & -(c & 1));
  }
  return ~c >>> 0;
}

function chunk(type, data) {
  const len = Buffer.alloc(4);
  len.writeUInt32BE(data.length, 0);
  const typeBuf = Buffer.from(type, "ascii");
  const body = Buffer.concat([typeBuf, data]);
  const crc = Buffer.alloc(4);
  crc.writeUInt32BE(crc32(body), 0);
  return Buffer.concat([len, body, crc]);
}

function encodePng(size, pixels) {
  const sig = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(size, 0);
  ihdr.writeUInt32BE(size, 4);
  ihdr[8] = 8; // bit depth
  ihdr[9] = 6; // color type RGBA
  // raw scanlines with filter byte 0
  const stride = size * 4;
  const raw = Buffer.alloc((stride + 1) * size);
  for (let y = 0; y < size; y++) {
    raw[y * (stride + 1)] = 0;
    pixels.copy(raw, y * (stride + 1) + 1, y * stride, y * stride + stride);
  }
  const idat = deflateSync(raw, { level: 9 });
  return Buffer.concat([
    sig,
    chunk("IHDR", ihdr),
    chunk("IDAT", idat),
    chunk("IEND", Buffer.alloc(0)),
  ]);
}

function draw(size) {
  const px = Buffer.alloc(size * size * 4);
  const set = (x, y, c) => {
    if (x < 0 || y < 0 || x >= size || y >= size) return;
    const i = (y * size + x) * 4;
    px[i] = c[0];
    px[i + 1] = c[1];
    px[i + 2] = c[2];
    px[i + 3] = c[3];
  };
  // background
  for (let y = 0; y < size; y++)
    for (let x = 0; x < size; x++) set(x, y, BG);
  // five stacked stones (proportional to a 64-unit design)
  const stones = [
    { cy: 48, rx: 16, ry: 6, c: STONE_B },
    { cy: 38, rx: 12, ry: 5, c: STONE_A },
    { cy: 29, rx: 9, ry: 4.5, c: STONE_B },
    { cy: 21, rx: 6, ry: 3.5, c: STONE_A },
    { cy: 15, rx: 3.5, ry: 2.5, c: STONE_B },
  ];
  const s = size / 64;
  const cx = 32 * s;
  for (const st of stones) {
    const ecy = st.cy * s;
    const erx = st.rx * s;
    const ery = st.ry * s;
    for (let y = Math.floor(ecy - ery); y <= Math.ceil(ecy + ery); y++) {
      for (let x = Math.floor(cx - erx); x <= Math.ceil(cx + erx); x++) {
        const dx = (x - cx) / erx;
        const dy = (y - ecy) / ery;
        if (dx * dx + dy * dy <= 1) set(x, y, st.c);
      }
    }
  }
  return px;
}

mkdirSync(new URL("../public/", import.meta.url), { recursive: true });
for (const size of [192, 512, 180]) {
  const png = encodePng(size, draw(size));
  const name = size === 180 ? "apple-touch-icon.png" : `icon-${size}.png`;
  writeFileSync(new URL(`../public/${name}`, import.meta.url), png);
  console.log(`wrote public/${name} (${png.length} bytes)`);
}
