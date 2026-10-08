import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  applyUpdate,
  getUpdateState,
  startAppUpdates,
  UPDATE_CHECK_EVERY_MS,
  type AppUpdates,
  type UpdateContainer,
  type UpdateRegistration,
} from "./appUpdate";

type Listener = () => void;

function fakeWorker() {
  const listeners = new Set<Listener>();
  return {
    state: "installed" as ServiceWorkerState,
    postMessage: vi.fn(),
    addEventListener: (_t: "statechange", l: Listener) => void listeners.add(l),
  };
}

function fakeRegistration(waiting: ReturnType<typeof fakeWorker> | null) {
  const listeners = new Set<Listener>();
  const reg = {
    waiting,
    installing: null,
    update: vi.fn(() => Promise.resolve()),
    addEventListener: (_t: "updatefound", l: Listener) => void listeners.add(l),
    removeEventListener: (_t: "updatefound", l: Listener) =>
      void listeners.delete(l),
    fire: () => listeners.forEach((l) => l()),
  };
  return reg;
}

function fakeContainer(controller: unknown = {}) {
  const listeners = new Set<Listener>();
  return {
    controller,
    addEventListener: (_t: "controllerchange", l: Listener) =>
      void listeners.add(l),
    removeEventListener: (_t: "controllerchange", l: Listener) =>
      void listeners.delete(l),
    fire: () => listeners.forEach((l) => l()),
  } satisfies UpdateContainer & { fire: () => void };
}

function setVisibility(value: DocumentVisibilityState) {
  Object.defineProperty(document, "visibilityState", {
    configurable: true,
    get: () => value,
  });
  document.dispatchEvent(new Event("visibilitychange"));
}

let running: AppUpdates | undefined;
beforeEach(() => vi.useFakeTimers());
afterEach(() => {
  running?.stop();
  running = undefined;
  vi.useRealTimers();
  setVisibility("visible");
});

describe("app updates", () => {
  it("is quiet when no worker is waiting", () => {
    const reg = fakeRegistration(null);
    running = startAppUpdates({
      container: fakeContainer(),
      registration: reg as unknown as UpdateRegistration,
      reload: vi.fn(),
    });
    expect(getUpdateState()).toBe("none");
  });

  it("says ready when a worker is waiting behind the one in control, and does nothing until the tap", () => {
    const worker = fakeWorker();
    const reload = vi.fn();
    running = startAppUpdates({
      container: fakeContainer(),
      registration: fakeRegistration(worker) as unknown as UpdateRegistration,
      reload,
    });
    expect(getUpdateState()).toBe("ready");
    expect(worker.postMessage).not.toHaveBeenCalled();
    expect(reload).not.toHaveBeenCalled();
  });

  it("does not announce the first worker ever (nothing is in control yet)", () => {
    running = startAppUpdates({
      container: fakeContainer(null),
      registration: fakeRegistration(fakeWorker()) as unknown as UpdateRegistration,
      reload: vi.fn(),
    });
    expect(getUpdateState()).toBe("none");
  });

  it("posts SKIP_WAITING on the tap and reloads once on controllerchange", () => {
    const worker = fakeWorker();
    const container = fakeContainer();
    const reload = vi.fn();
    running = startAppUpdates({
      container,
      registration: fakeRegistration(worker) as unknown as UpdateRegistration,
      reload,
    });
    applyUpdate();
    expect(worker.postMessage).toHaveBeenCalledWith({ type: "SKIP_WAITING" });
    expect(getUpdateState()).toBe("updating");
    container.fire();
    container.fire();
    expect(reload).toHaveBeenCalledTimes(1);
  });

  it("never reloads on a controllerchange he did not ask for", () => {
    const container = fakeContainer();
    const reload = vi.fn();
    running = startAppUpdates({
      container,
      registration: fakeRegistration(fakeWorker()) as unknown as UpdateRegistration,
      reload,
    });
    container.fire();
    expect(reload).not.toHaveBeenCalled();
  });

  it("asks for a new build on start, on return to visible and every 30 minutes", () => {
    const reg = fakeRegistration(null);
    running = startAppUpdates({
      container: fakeContainer(),
      registration: reg as unknown as UpdateRegistration,
      reload: vi.fn(),
    });
    expect(reg.update).toHaveBeenCalledTimes(1);

    setVisibility("hidden");
    expect(reg.update).toHaveBeenCalledTimes(1);
    setVisibility("visible");
    expect(reg.update).toHaveBeenCalledTimes(2);

    vi.advanceTimersByTime(UPDATE_CHECK_EVERY_MS);
    expect(reg.update).toHaveBeenCalledTimes(3);
    vi.advanceTimersByTime(UPDATE_CHECK_EVERY_MS);
    expect(reg.update).toHaveBeenCalledTimes(4);
  });

  it("survives a failed check (offline)", async () => {
    const reg = fakeRegistration(null);
    reg.update.mockRejectedValue(new Error("offline"));
    running = startAppUpdates({
      container: fakeContainer(),
      registration: reg as unknown as UpdateRegistration,
      reload: vi.fn(),
    });
    await vi.advanceTimersByTimeAsync(UPDATE_CHECK_EVERY_MS);
    expect(reg.update).toHaveBeenCalledTimes(2);
  });
});
