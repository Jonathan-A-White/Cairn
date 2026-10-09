import type { ReactNode } from "react";
import { Card, Screen } from "./ui";
import {
  CREDIT_GROUPS,
  CREDITS,
  NEWTON_QUOTE,
  WHY_WE_CREDIT,
} from "./credits";

function ExtLink({ href, children }: { href: string; children: ReactNode }) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="text-cairn-neon underline"
    >
      {children}
    </a>
  );
}

/** Why we credit, then everything Cairn is built on (src/app/credits.ts). */
export function AboutScreen() {
  return (
    <Screen title="About">
      <Card className="mb-4">
        <blockquote data-testid="about-quote">
          <p className="text-lg text-cairn-ink">“{NEWTON_QUOTE.text}”</p>
          <footer className="mt-2 text-sm text-cairn-dim">
            <ExtLink href={NEWTON_QUOTE.url}>{NEWTON_QUOTE.author}</ExtLink>,{" "}
            {NEWTON_QUOTE.source}
          </footer>
        </blockquote>
        <p data-testid="about-why" className="mt-3 text-sm text-cairn-dim">
          {WHY_WE_CREDIT}
        </p>
        <p className="mt-2 text-sm text-cairn-dim">
          Cairn is a cairn for the home. Offline-first; your data stays on this
          device.
        </p>
      </Card>

      <div data-testid="about-credits">
        {CREDIT_GROUPS.map((group) => (
          <section key={group.id} className="mb-4">
            <h2 className="mb-2 font-semibold">{group.title}</h2>
            <ul className="space-y-3">
              {CREDITS.filter((c) => c.group === group.id).map((c) => (
                <li key={c.id} data-testid={`credit-${c.id}`}>
                  <Card>
                    <p className="font-semibold">
                      <ExtLink href={c.url}>{c.name}</ExtLink>
                    </p>
                    <p className="mt-1 break-words text-sm text-cairn-dim">
                      {c.use}
                    </p>
                    <p className="mt-1 break-words text-sm text-cairn-dim">
                      Licence:{" "}
                      <ExtLink href={c.licence.url}>{c.licence.name}</ExtLink>
                    </p>
                    <p className="mt-1 break-words text-sm text-cairn-dim">
                      Changes: {c.changes}
                    </p>
                  </Card>
                </li>
              ))}
            </ul>
          </section>
        ))}
        <p className="text-sm text-cairn-dim">
          Cairn borrows no fonts or icons: the text uses your phone's own
          monospace font and the app icons are drawn by our own script.
        </p>
      </div>
    </Screen>
  );
}
