import { afterEach, describe, expect, it, vi } from "vitest";
import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { UpdateBanner } from "./UpdateBanner";
import {
  startAppUpdates,
  type AppUpdates,
  type UpdateRegistration,
} from "./appUpdate";

let running: AppUpdates | undefined;
afterEach(() => {
  act(() => running?.stop());
  running = undefined;
});

function waitingRegistration() {
  const worker = {
    state: "installed" as ServiceWorkerState,
    postMessage: vi.fn(),
    addEventListener: vi.fn(),
  };
  const reg = {
    waiting: worker,
    installing: null,
    update: vi.fn(() => Promise.resolve()),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  };
  return { worker, reg: reg as unknown as UpdateRegistration };
}

describe("UpdateBanner", () => {
  it("shows nothing when no build is waiting", () => {
    render(<UpdateBanner />);
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("says 'Update ready, tap to reload'; the tap sends SKIP_WAITING and says 'Updating…'", async () => {
    const { worker, reg } = waitingRegistration();
    const user = userEvent.setup();
    render(<UpdateBanner />);
    act(() => {
      running = startAppUpdates({
        container: {
          controller: {},
          addEventListener: vi.fn(),
          removeEventListener: vi.fn(),
        },
        registration: reg,
        reload: vi.fn(),
      });
    });
    const banner = await screen.findByRole("button", {
      name: "Update ready, tap to reload",
    });
    expect(worker.postMessage).not.toHaveBeenCalled();
    await user.click(banner);
    expect(worker.postMessage).toHaveBeenCalledWith({ type: "SKIP_WAITING" });
    expect(
      screen.getByRole("button", { name: "Updating…" }),
    ).toBeDisabled();
  });
});
