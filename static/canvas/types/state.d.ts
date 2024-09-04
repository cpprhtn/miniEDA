/// <reference path="./diagram.d.ts" />

type State = {
  diagram: WorkflowGraph;
  selectedNodeId: string | null;
};

type StateChangeListener<K extends keyof State> = (newState: State[K]) => void;

type StateChangeListenerMap = {
  [K in keyof State]: Array<StateChangeListener<K>>;
};

declare function UseStateFn<K extends keyof State>(
  key: K
): [State[K], (newState: State[K]) => void];
