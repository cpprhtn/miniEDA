/**
 * @param {number} length
 * @returns {string}
 */
export function createRandomString(length) {
  const characters = "abcdefghijklmnopqrstuvwxyz0123456789";
  let result = "";
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return result;
}

/**
 * @returns {string}
 */
export function createId() {
  const current = Date.now().toString(36);
  const random = createRandomString(6);
  return `${current}${random}`.toUpperCase();
}
