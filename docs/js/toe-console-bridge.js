/**
 * TOE / MQGT shared console state for cbaird26.github.io (same origin).
 * Include this script on any app under https://cbaird26.github.io/ to read/write
 * the same dial bundle as Theory of Everything Foundation.
 */
(function (global) {
  var KEY = 'mqgt_toe_console_v1';
  var VER = 1;

  function read() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch (e) {
      return null;
    }
  }

  function write(payload) {
    try {
      payload = payload || {};
      payload.v = VER;
      localStorage.setItem(KEY, JSON.stringify(payload));
    } catch (e) {}
  }

  function subscribe(fn) {
    if (typeof fn !== 'function') return;
    global.addEventListener('storage', function (e) {
      if (e.key === KEY && e.newValue) {
        try {
          fn(JSON.parse(e.newValue));
        } catch (err) {
          fn(null);
        }
      }
    });
  }

  global.TOE_CONSOLE_BRIDGE = {
    KEY: KEY,
    VERSION: VER,
    read: read,
    write: write,
    subscribe: subscribe
  };
})(typeof window !== 'undefined' ? window : this);
