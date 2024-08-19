/// <reference path="../../types/controller-panel.d.ts" />

export class ControllerPanelHtmlBuilder {
  constructor() {
    /** @type {ControllerPanelHtmlElement[]} */
    this.contents = [];
  }

  /**
   * @param {string} value
   * @returns {this}
   */
  title(value) {
    this.contents.push({ type: "title", value });
    return this;
  }

  /**
   * @param {string} label
   * @param {string} value
   * @returns {this}
   */
  text(label, value) {
    this.contents.push({ type: "text", label, value });
    return this;
  }

  /**
   * @returns {string}
   */
  build() {
    return this.contents
      .map((content) => {
        switch (content.type) {
          case "title":
            return `
              <div class="controller-panel-full-element">
                <h2>${content.value}</h2>
              </div>
              `;
          case "text":
            return `
              <div class="controller-panel-kv-element">
                <label>${content.label}</label><span>${content.value}</span>
              </div>
            `;
        }
      })
      .join("\n");
  }

  static builder() {
    return new ControllerPanelHtmlBuilder();
  }
}
