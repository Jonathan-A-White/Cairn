import { describe, it, expect, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { SettingsScreen } from "./SettingsScreen";
import { readSweepGrind, SWEEP_GRIND_KEY } from "../bridge/sweepGrind";
import { exportSnapshotJson } from "../shared/data/snapshot";
import { resetDb } from "../test/reset";

beforeEach(async () => {
  localStorage.clear();
  await resetDb();
});

describe("Settings: Photo sweeps", () => {
  it("shows Sonnet and Low, and reads them, when nothing is stored", () => {
    render(<SettingsScreen />);
    expect(screen.getByText("Photo sweeps")).toBeInTheDocument();
    expect(
      screen.getByText(
        "Used for each photo sent to the factory. Higher costs more fuel.",
      ),
    ).toBeInTheDocument();
    expect(screen.getByLabelText("Model")).toHaveValue("sonnet");
    expect(screen.getByLabelText("Effort")).toHaveValue("low");
    expect(readSweepGrind()).toEqual({ model: "sonnet", effort: "low" });
  });

  it("keeps Opus and High on the device across a fresh render", async () => {
    const user = userEvent.setup();
    const first = render(<SettingsScreen />);
    await user.selectOptions(screen.getByLabelText("Model"), "opus");
    await user.selectOptions(screen.getByLabelText("Effort"), "high");
    first.unmount();

    render(<SettingsScreen />);
    expect(screen.getByLabelText("Model")).toHaveValue("opus");
    expect(screen.getByLabelText("Effort")).toHaveValue("high");
    expect(readSweepGrind()).toEqual({ model: "opus", effort: "high" });
    expect(localStorage.getItem(SWEEP_GRIND_KEY)).toBe(
      '{"model":"opus","effort":"high"}',
    );
    expect(SWEEP_GRIND_KEY).toBe("cairn.sweep.grind");
  });

  it("offers the three models and the three efforts", () => {
    render(<SettingsScreen />);
    const options = (label: string) =>
      Array.from(
        (screen.getByLabelText(label) as HTMLSelectElement).options,
      ).map((o) => o.textContent);
    expect(options("Model")).toEqual(["Haiku", "Sonnet", "Opus"]);
    expect(options("Effort")).toEqual(["Low", "Medium", "High"]);
  });
});

describe("readSweepGrind", () => {
  it.each([
    ["not JSON", "{{nope"],
    ["a string", '"opus"'],
    ["null", "null"],
    ["unknown values", '{"model":"gpt","effort":"max"}'],
    ["wrong types", '{"model":1,"effort":2}'],
  ])("reads the defaults when the key holds %s", (_name, raw) => {
    localStorage.setItem(SWEEP_GRIND_KEY, raw);
    expect(readSweepGrind()).toEqual({ model: "sonnet", effort: "low" });
  });

  it("keeps a valid half and defaults the other", () => {
    localStorage.setItem(SWEEP_GRIND_KEY, '{"model":"haiku","effort":"x"}');
    expect(readSweepGrind()).toEqual({ model: "haiku", effort: "low" });
  });
});

describe("sweep grind is not in a snapshot", () => {
  it("exports neither the model nor the effort", async () => {
    const user = userEvent.setup();
    render(<SettingsScreen />);
    await user.selectOptions(screen.getByLabelText("Model"), "opus");
    await user.selectOptions(screen.getByLabelText("Effort"), "high");
    const json = await exportSnapshotJson();
    expect(json).not.toContain("opus");
    expect(json).not.toContain("effort");
    expect(json).not.toContain("cairn.sweep.grind");
  });
});

describe("Settings: build stamp", () => {
  it("shows 'v<version> · <UTC time>Z · <commit>' under About", () => {
    render(<SettingsScreen />);
    expect(screen.getByTestId("build-version")).toHaveTextContent(
      /^v\d+\.\d+\.\d+ · \d{4}-\d{2}-\d{2} \d{2}:\d{2}Z · ([0-9a-f]{7,}|dev)$/,
    );
    expect(screen.getByTestId("build-version")).toHaveTextContent(
      `v${__APP_VERSION__}`,
    );
  });
});
