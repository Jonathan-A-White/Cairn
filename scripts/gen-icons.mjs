// Generates the PNG app icons (a cairn etched onto a circuit board: stacked
// stones as neon pads, wired by a trace bus) without any image library, by
// drawing into an RGBA buffer and encoding a PNG with Node's built-in zlib.
// Run: node scripts/gen-icons.mjs
import { deflateSync } from "node:zlib";
import { writeFileSync, mkdirSync } from "node:fs";

const BG = [5, 7, 10]; // #05070a substrate
const GRID = [46, 224, 106]; // grid etch, laid down at low alpha
const TRACE = [28, 127, 69]; // #1c7f45 resting trace
const NEON = [46, 224, 106]; // #2ee06a stone outline
const SOLDER = [125, 255, 176]; // #7dffb0 pad highlight

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

// --- Geometry, in a 64-unit design space ---

// Stones, bottom to top. Each is drawn as a ring (an etched pad outline)
// rather than a filled stone, with a via at its centre.
const STONES = [
  { cy: 48, rx: 16, ry: 6 },
  { cy: 38, rx: 12, ry: 5 },
  { cy: 29, rx: 9, ry: 4.5 },
  { cy: 21, rx: 6, ry: 3.5 },
  { cy: 15, rx: 3.5, ry: 2.5 },
];
const CX = 32;
const RING_W = 0.9; // ring thickness in design units
const TRACE_W = 0.8;

const inEllipseRing = (x, y, s) => {
  const outer = Math.hypot((x - CX) / s.rx, (y - s.cy) / s.ry);
  const inner = Math.hypot(
    (x - CX) / (s.rx - RING_W),
    (y - s.cy) / (s.ry - RING_W),
  );
  return outer <= 1 && inner > 1;
};

const inDisc = (x, y, cx, cy, r) => Math.hypot(x - cx, y - cy) <= r;

const inVSeg = (x, y, cx, y0, y1) =>
  Math.abs(x - cx) <= TRACE_W / 2 && y >= y0 && y <= y1;

const inHSeg = (x, y, cy, x0, x1) =>
  Math.abs(y - cy) <= TRACE_W / 2 && x >= Math.min(x0, x1) && x <= Math.max(x0, x1);

/** The bus rising through the stack, plus a lead off each stone to a via. */
function inTrace(x, y) {
  if (inVSeg(x, y, CX, 15, 50)) return true;
  // Alternating leads: right, left, right, left — each ending at a via pad.
  const leads = [
    { cy: 48, to: 56 },
    { cy: 38, to: 10 },
    { cy: 29, to: 52 },
    { cy: 21, to: 16 },
  ];
  return leads.some((l) => inHSeg(x, y, l.cy, CX, l.to));
}

function inVia(x, y) {
  const vias = [
    { x: 56, y: 48 },
    { x: 10, y: 38 },
    { x: 52, y: 29 },
    { x: 16, y: 21 },
  ];
  return vias.some((v) => inDisc(x, y, v.x, v.y, 1.9));
}

/** The etched routing grid behind everything, on an 8-unit pitch. */
function inGrid(x, y) {
  const near = (v) => Math.abs(v - Math.round(v / 8) * 8) <= 0.22;
  return near(x) || near(y);
}

function draw(size) {
  const px = Buffer.alloc(size * size * 4);
  const SS = 3; // supersampling factor, for antialiased curves
  const u = 64 / size; // pixels → design units

  for (let py = 0; py < size; py++) {
    for (let pxi = 0; pxi < size; pxi++) {
      // Accumulate coverage per layer across the subsample grid.
      let grid = 0,
        trace = 0,
        ring = 0,
        via = 0;
      for (let sy = 0; sy < SS; sy++) {
        for (let sx = 0; sx < SS; sx++) {
          const x = (pxi + (sx + 0.5) / SS) * u;
          const y = (py + (sy + 0.5) / SS) * u;
          if (inGrid(x, y)) grid++;
          if (inTrace(x, y)) trace++;
          if (STONES.some((s) => inEllipseRing(x, y, s))) ring++;
          if (inVia(x, y)) via++;
        }
      }
      const n = SS * SS;
      // Composite back-to-front onto the substrate.
      let [r, g, b] = BG;
      const over = (c, a) => {
        r = r + (c[0] - r) * a;
        g = g + (c[1] - g) * a;
        b = b + (c[2] - b) * a;
      };
      over(GRID, (grid / n) * 0.1);
      over(TRACE, trace / n);
      over(NEON, ring / n);
      over(SOLDER, via / n);

      const i = (py * size + pxi) * 4;
      px[i] = Math.round(r);
      px[i + 1] = Math.round(g);
      px[i + 2] = Math.round(b);
      px[i + 3] = 255;
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
