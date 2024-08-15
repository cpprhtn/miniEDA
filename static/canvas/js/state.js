/// <reference path="../types/state.d.ts" />

/** @type {State} */
const initialState = {
  diagram: data,
  selectedNode: null,
};

/** @type {StateChangeListenerMap} */
const stateChangeListenerMap = {
  diagram: [],
  selectedNode: [],
};

const state = new Proxy(initialState, {
  /** @param { keyof State } key */
  set: (target, key, value) => {
    stateChangeListenerMap[key]?.forEach((listener) => listener(value));
    target[key] = value;
    return true;
  },
});

/**
 * @param {keyof State} key
 * @param {StateChangeListener} listener
 * @returns {void}
 */
export function registerStateChangeListener(key, listener) {
  stateChangeListenerMap[key].push(listener);
}

/** @type {UseStateFn} */
export function useState(key) {
  return [state[key], (value) => (state[key] = value)];
}
