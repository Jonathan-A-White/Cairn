/**
 * A tiny typed publish/subscribe bus. Each context creates its own instance
 * over its own event map (contracts/events.ts), so events stay scoped per
 * context and never leak across boundaries.
 */
export class EventBus<Events extends Record<string, unknown>> {
  private listeners: {
    [K in keyof Events]?: Set<(payload: Events[K]) => void>;
  } = {};

  on<K extends keyof Events>(
    type: K,
    handler: (payload: Events[K]) => void,
  ): () => void {
    (this.listeners[type] ??= new Set()).add(handler);
    return () => this.listeners[type]?.delete(handler);
  }

  emit<K extends keyof Events>(type: K, payload: Events[K]): void {
    this.listeners[type]?.forEach((h) => h(payload));
  }
}
