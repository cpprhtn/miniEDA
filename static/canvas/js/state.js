/// <reference path="../types/state.d.ts" />

/** @type {State} */
const initialState = {
  diagram: window["data"],
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

export function callAllStateChangeListener() {
  Object.keys(stateChangeListenerMap).forEach((key) => {
    stateChangeListenerMap[key].forEach((listener) => listener(state[key]));
  });
}

/**
 * @type {<K extends keyof State>(key: K, listener: StateChangeListener<K>) => void}
 */
export function registerStateChangeListener(key, listener) {
  stateChangeListenerMap[key].push(listener);
}

/** @type {UseStateFn} */
export function useState(key) {
  return [state[key], (value) => (state[key] = value)];
}
