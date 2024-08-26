export class InputController {
  constructor() {
    /** @type {string | null} */
    this.id = null;
  }

  /**
   * @param {string} id
   */
  attach(id) {
    this.id = id;
  }

  /**
   * @returns {HTMLInputElement}
   */
  get() {
    if (!this.id) {
      throw new Error("InputController is not attached to any element.");
    }

    const input = document.getElementById(this.id);
    if (!input) {
      throw new Error(`Element with id ${this.id} is not found.`);
    }

    return /** @type {HTMLInputElement} */ (input);
  }
}
