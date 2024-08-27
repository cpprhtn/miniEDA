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
   * @param {((value: string) => void)=} onChange
   * @returns {this}
   */
  select(label, options, onChange) {
    const newId = createId();
    this.contents.push({ id: newId, type: "select", label, options, onChange });
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
   * @param {string} label
   * @param {string} value
   * @param {InputController} controller
   * @param {((value: string) => void)=} onSubmit
   * @returns {this}
   */
  textField(label, value, controller, onSubmit) {
    const newId = createId();
    this.contents.push({
      type: "text-field",
      id: newId,
      label,
      value,
      onConfirm: onSubmit,
    });
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
          case "text-field":
            return `
              <div class="controller-panel-kv-element">
                <label>${content.label}</label>
                <input id="${content.id}" type="text" value="${content.value}">
              </div>
            `;
        }
      })
      .join("\n");

    container.innerHTML = ui;

    this.contents.forEach((content) => {
      if (content.type === "select") {
        const select = document.getElementById(content.id);
        if (select) {
          select.addEventListener("change", (ev) => {
            content.onChange(ev.target["value"]);
          });
        }
      } else if (content.type === "text-field") {
        const input = document.getElementById(content.id);
        if (input) {
          input.addEventListener("keydown", (ev) => {
            if (ev.key === "Enter") {
              content.onConfirm(ev.target["value"]);
            }
          });
        }
      }
    });
  }

  static builder() {
    return new ControllerPanelHtmlBuilder();
  }
}
