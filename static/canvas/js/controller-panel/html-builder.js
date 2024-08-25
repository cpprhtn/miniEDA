/// <reference path="../../types/controller-panel.d.ts" />

import { createId } from "../util.js";
import { InputController } from "./input-controller.js";

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
   * @param {string} label
   * @param {string[]} options
   * @param {InputController} controller
   * @returns {this}
   */
  select(label, options, controller) {
    const newId = createId();
    this.contents.push({ id: newId, type: "select", label, options });
    controller.attach(newId);
    return this;
  }

  /**
   * @param {string} label
   * @param {File | null} file
   * @param {InputController} controller
   * @returns {this}
   */
  file(label, file, controller) {
    const newId = createId();
    this.contents.push({ id: newId, type: "file", label, file });
    controller.attach(newId);
    return this;
  }

  /**
   * @param {HTMLElement} container
   */
  build(container) {
    const ui = this.contents
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
          case "select":
            return `
              <div class="controller-panel-kv-element">
                <label>${content.label}</label>
                <select id="${content.id}">
                  ${content.options
                    .map(
                      (option) => `<option value="${option}">${option}</option>`
                    )
                    .join("\n")}
                </select>
              </div>
            `;
          case "file":
            return `
              <div class="controller-panel-kv-element">
                <label>${content.label}</label>
                <label class="input-file-custom-button">
                  <input id="${content.id}" type="file">
                  ${content.file ? content.file.name : "파일 선택"}
                </label>
              </div>
            `;
        }
      })
      .join("\n");

    container.innerHTML = ui;

    this.contents.forEach((content) => {
      // UI 생성 후 후처리 필요 시 사용
      // ex) event listener
    });
  }

  static builder() {
    return new ControllerPanelHtmlBuilder();
  }
}
