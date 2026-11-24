# Browser tests

Run from the repo root: `python3 -m http.server 8137` then `playwright-cli open 'http://localhost:8137/?test'`.
Read the result with `playwright-cli eval "() => JSON.stringify(window.picoTestResult)"` (it is undefined until the tests finish).
The result is `{pass, fail, failures: [{name, msg}]}`; it is also printed in `<pre id="test-out">` on the page.
`?test` stops the service worker and the live-forecast fetch; the app's functions are on `window.pico`.
Add tests to `forecast.test.js` with `test(name, fn)`, `eq`, `ok` and `liveFixture`; they run in order and `fn` may return a promise.
A service worker left over from a normal visit can serve stale files, so run `playwright-cli delete-data` first.
