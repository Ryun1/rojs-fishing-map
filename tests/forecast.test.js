/* Browser tests for the forecast. Open the app with ?test; results land in window.picoTestResult. */
(function () {
  var pico = window.pico;
  var tests = [], failures = [], passed = 0;

  function test(name, fn) { tests.push({ name: name, fn: fn }); }
  function eq(actual, expected, msg) {
    if (actual !== expected) throw new Error((msg ? msg + ': ' : '') + 'expected ' + JSON.stringify(expected) + ', got ' + JSON.stringify(actual));
  }
  function ok(cond, msg) { if (!cond) throw new Error(msg || 'not ok'); }

  /* A state.live-shaped object: 5 spots, `hours` hourly values from startUtcMs; fn(spotIdx, hourIdx) gives the values. */
  function liveFixture(startUtcMs, hours, fn) {
    var m = [], w = [], s, h, t0 = startUtcMs / 1000;
    for (s = 0; s < 5; s++) {
      var mm = { time: [], wave_height: [], wave_direction: [], wave_period: [], swell_wave_height: [], swell_wave_direction: [], swell_wave_period: [], wind_wave_height: [], wind_wave_direction: [], sea_surface_temperature: [] };
      var ww = { time: [], wind_speed_10m: [], wind_direction_10m: [], wind_gusts_10m: [] };
      for (h = 0; h < hours; h++) {
        var v = fn(s, h), t = t0 + h * 3600;
        mm.time.push(t); mm.wave_height.push(v.wave); mm.wave_direction.push(v.waveDir); mm.wave_period.push(v.per);
        mm.swell_wave_height.push(v.wave); mm.swell_wave_direction.push(v.waveDir); mm.swell_wave_period.push(v.per);
        mm.wind_wave_height.push(0); mm.wind_wave_direction.push(v.windDir); mm.sea_surface_temperature.push(v.sst);
        ww.time.push(t); ww.wind_speed_10m.push(v.wind); ww.wind_direction_10m.push(v.windDir); ww.wind_gusts_10m.push(v.gust);
      }
      m.push(mm); w.push(ww);
    }
    return { at: Date.now(), m: m, w: w };
  }

  window.picoTest = { test: test, eq: eq, ok: ok, liveFixture: liveFixture };

  test('whenAt matches readWhen', function () {
    document.getElementById('f-date').value = '2026-11-24';
    document.getElementById('f-time').value = '07:30';
    eq(JSON.stringify(pico.whenAt(pico.readWhen().utc)), JSON.stringify(pico.readWhen()));
  });

  test('whenAt across DST', function () {
    eq(pico.whenAt(Date.UTC(2026, 9, 25, 0, 30)).local, '2026-10-25T00:30');
    eq(pico.whenAt(Date.UTC(2026, 9, 25, 2, 30)).local, '2026-10-25T01:30');
  });

  test('fixture feeds spotCond', function () {
    pico.state.live = liveFixture(Date.UTC(2026, 10, 24, 0), 48, function () { return { wave: 0.5, waveDir: 315, per: 9, wind: 8, windDir: 90, gust: 12, sst: 19 }; });
    pico.state.source = 'live';
    var c = pico.spotCond(pico.SPOTS[0], 0, pico.whenAt(Date.UTC(2026, 10, 24, 10)));
    ok(c !== null, 'cond is null');
    eq(c.raw.src, 'live');
  });

  function finish() {
    var r = { pass: passed, fail: failures.length, failures: failures };
    window.picoTestResult = r;
    var pre = document.createElement('pre'); pre.id = 'test-out'; pre.textContent = JSON.stringify(r, null, 1);
    document.body.appendChild(pre);
  }
  /* Each test starts from, and leaves behind, the page as it was: state, form values, fetch and pico- storage. */
  function snapshot() {
    var snap = { state: {}, fetch: window.fetch, fields: [], store: {} }, k, i, els = document.querySelectorAll('input, select');
    for (k in pico.state) snap.state[k] = pico.state[k];
    for (i = 0; i < els.length; i++) snap.fields.push({ el: els[i], value: els[i].value, checked: els[i].checked });
    try {
      for (i = 0; i < localStorage.length; i++) { k = localStorage.key(i); if (k.indexOf('pico-') === 0) snap.store[k] = localStorage.getItem(k); }
    } catch (e) {}
    return snap;
  }
  function restore(snap) {
    var k, i, keys = [];
    for (k in pico.state) if (!(k in snap.state)) delete pico.state[k];
    for (k in snap.state) pico.state[k] = snap.state[k];
    for (i = 0; i < snap.fields.length; i++) { snap.fields[i].el.value = snap.fields[i].value; snap.fields[i].el.checked = snap.fields[i].checked; }
    window.fetch = snap.fetch;
    try {
      for (i = 0; i < localStorage.length; i++) if (localStorage.key(i).indexOf('pico-') === 0) keys.push(localStorage.key(i));
      keys.forEach(function (key) { localStorage.removeItem(key); });
      for (k in snap.store) localStorage.setItem(k, snap.store[k]);
    } catch (e) {}
    try { pico.render(); } catch (e) {}
  }
  function runNext(i) {
    if (i >= tests.length) { finish(); return; }
    var t = tests[i], snap = snapshot(), done = function (err) {
      restore(snap);
      if (err) failures.push({ name: t.name, msg: String(err && err.message || err) }); else passed++;
      runNext(i + 1);
    };
    try {
      var p = t.fn();
      if (p && typeof p.then === 'function') p.then(function () { done(); }, done); else done();
    } catch (e) { done(e); }
  }
  Promise.resolve().then(function () { runNext(0); });
})();
