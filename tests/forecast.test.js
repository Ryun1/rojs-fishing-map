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

  /* ---------- Task 2: ranked spots for a window ---------- */
  var CALM = { wave: 0.2, waveDir: 315, per: 8, wind: 8, windDir: 90, gust: 12, sst: 19 };
  /* A swell that the real exposure model lets through: 3.0 m from the middle of the spot's first open sector. */
  function unsafeFor(i) {
    var s = pico.SPOTS[i].open[0], a = s[0], b = s[1];
    if (b < a) b += 360;
    return { wave: 3.0, waveDir: ((a + b) / 2) % 360, per: 8, wind: 8, windDir: 90, gust: 12, sst: 19 };
  }
  function calmLive(fn) {
    pico.state.live = liveFixture(Date.UTC(2026, 10, 24, 0), 48, function (s, h) { return fn ? (fn(s, h) || CALM) : CALM; });
    pico.state.source = 'live';
  }
  var T12 = Date.UTC(2026, 10, 24, 12);

  test('ranks by fishability then score', function () {
    calmLive(function (s) {
      if (s === 2) return unsafeFor(2);
      if (s === 0) return { wave: 0.2, waveDir: 315, per: 8, wind: 45, windDir: 90, gust: 55, sst: 19 };
    });
    var r = pico.rankSpots(T12, 3, '');
    eq(r.length, 5);
    var last = r[4];
    eq(last.spot.id, pico.SPOTS[2].id); eq(last.level, 3); eq(last.score, null);
    var zero = r.filter(function (x) { return x.spot.id === pico.SPOTS[0].id; })[0];
    eq(zero.level, 2);
    ok(r[0].level === 0 && r[1].level === 0 && r[2].level === 0, 'first three are level 0');
    ok(r[0].score >= r[1].score && r[1].score >= r[2].score, 'sorted by score');
  });

  test('worst half hour wins', function () {
    calmLive(function (s, h) { if (s === 1 && h === 13) return unsafeFor(1); });
    var r = pico.rankSpots(T12, 3, ''), e = r.filter(function (x) { return x.i === 1; })[0];
    eq(e.level, 3);
    ok(e.at !== Date.UTC(2026, 10, 24, 12, 30) && e.at !== Date.UTC(2026, 10, 24, 13), 'at is a safe half hour');
  });

  test('picked species', function () {
    calmLive();
    var id = pico.SPECIES[0].id, r = pico.rankSpots(T12, 3, id);
    r.forEach(function (x) { if (x.score !== null) eq(x.sp.id, id); });
    ok(r.some(function (x) { return x.score !== null; }), 'some score');
  });

  test('partial window', function () {
    pico.state.live = liveFixture(Date.UTC(2026, 10, 24, 0), 24, function () { return CALM; });
    pico.state.source = 'live';
    var r = pico.rankSpots(Date.UTC(2026, 10, 24, 22), 3, '');
    eq(r[0].samples, 6); eq(r[0].missing, 3); ok(r[0].level !== null, 'level');
    pico.state.len = 3; pico.state.fish = '';
    pico.renderRanked(pico.whenAt(Date.UTC(2026, 10, 24, 22)));
    ok(document.getElementById('ranked').textContent.indexOf('covers only part') >= 0, 'partial note');
  });

  test('window across midnight', function () {
    calmLive();
    document.getElementById('f-date').value = '2026-11-24';
    document.getElementById('f-time').value = '23:00';
    pico.state.len = 3; pico.state.fish = '';
    pico.renderRanked(pico.readWhen());
    var h = document.getElementById('h-rank').textContent;
    ok(h.indexOf('23:00–02:00') >= 0, 'range in ' + h);
    ok(h.indexOf('next day') >= 0, 'next day in ' + h);
  });

  test('all unsafe', function () {
    calmLive();
    pico.state.warn = [{ awarenessLevelID: 'red', awarenessTypeName: 'Agitação Marítima', idAreaAviso: 'ACE', startTime: '2026-11-24T00:00:00', endTime: '2026-11-25T00:00:00' }];
    var r = pico.rankSpots(T12, 3, '');
    eq(r.length, 5);
    r.forEach(function (x) { eq(x.level, 3); eq(x.score, null); });
  });

  test('manual mode', function () {
    pico.state.live = null; pico.state.source = 'manual';
    var r = pico.rankSpots(T12, 3, '');
    eq(r.length, 5);
    r.forEach(function (x) { ok(x.level !== null, 'level null'); });
  });

  test('bad saved fish', function () {
    localStorage.setItem('pico-prefs-v1', '{"fish":"nosuchfish","len":3}');
    pico.loadPrefs();
    eq(pico.state.fish, '');
  });

  /* ---------- Task 3: best times through the day ---------- */
  test('timeline has 48 cells', function () {
    calmLive();
    var tl = pico.dayTimeline(pico.SPOTS[0], 0, 2026, 11, 24, '');
    eq(tl.length, 48); eq(tl[0].t, 0); eq(tl[47].t, 1410);
  });

  test('timeline on clock change', function () {
    calmLive();
    eq(pico.dayTimeline(pico.SPOTS[0], 0, 2026, 10, 25, '').length, 50);
  });

  test('timeline levels follow forecast', function () {
    calmLive(function (s, h) { if (s === 0 && (h === 12 || h === 13)) return unsafeFor(0); });
    var tl = pico.dayTimeline(pico.SPOTS[0], 0, 2026, 11, 24, ''), at = function (h, m) {
      return tl.filter(function (c) { return c.utc === Date.UTC(2026, 10, 24, h, m); })[0];
    };
    eq(at(12, 0).level, 3); eq(at(12, 30).level, 3); eq(at(13, 0).level, 3); eq(at(16, 0).level, 0);
  });

  test('timeline species scores', function () {
    calmLive();
    var id = pico.SPECIES[0].id;
    pico.dayTimeline(pico.SPOTS[0], 0, 2026, 11, 24, id).forEach(function (c) { ok(typeof c.score === 'number', 'score at ' + c.t); });
    pico.dayTimeline(pico.SPOTS[0], 0, 2026, 11, 24, '').forEach(function (c) { eq(c.score, null); });
  });

  test('timeline outside the forecast has no data', function () {
    calmLive();
    var tl = pico.dayTimeline(pico.SPOTS[0], 0, 2026, 11, 26, pico.SPECIES[0].id);
    tl.forEach(function (c) { eq(c.level, null); eq(c.score, null); });
  });

  test('timeline manual', function () {
    pico.state.live = null; pico.state.source = 'manual';
    pico.dayTimeline(pico.SPOTS[0], 0, 2026, 11, 24, '').forEach(function (c) { ok(c.level !== null, 'level at ' + c.t); });
  });

  test('no moon selector', function () {
    ok(document.getElementById('f-moon') === null, 'f-moon present');
    pico.render();
    ok(document.getElementById('besttimes').textContent.indexOf('Moon') < 0, 'Moon in best times');
  });

  test('best times renders strip and bars', function () {
    calmLive();
    pico.state.fish = pico.SPECIES[0].id;
    document.getElementById('f-date').value = '2026-11-24';
    document.getElementById('f-time').value = '10:00';
    pico.render();
    var b = document.getElementById('besttimes');
    eq(b.querySelectorAll('.strip > *').length, 48);
    eq(b.querySelectorAll('.bars .cell').length, 48);
    eq(b.querySelectorAll('.strip .sel').length, 1);
    ok(b.querySelectorAll('.inwin').length > 0, 'inwin');
    pico.state.fish = '';
    pico.render();
    eq(b.querySelectorAll('.bars').length, 0);
    ok(b.textContent.indexOf('Good') >= 0, 'stretch label');
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
    var t = tests[i], snap = null, settled = false;
    function done(err) {
      if (settled) return;
      settled = true;
      var bad = err ? String(err && err.message || err) : null;
      try { if (snap) restore(snap); } catch (e) { failures.push({ name: t.name, msg: 'restore: ' + String(e && e.message || e) }); }
      if (bad) failures.push({ name: t.name, msg: bad }); else if (!failures.length || failures[failures.length - 1].name !== t.name) passed++;
      Promise.resolve().then(function () { runNext(i + 1); });
    }
    try { snap = snapshot(); } catch (e) { failures.push({ name: t.name, msg: 'snapshot: ' + String(e && e.message || e) }); }
    try {
      var p = t.fn();
      if (p && typeof p.then === 'function') p.then(function () { done(); }, done); else done();
    } catch (e) { done(e); }
  }
  if (!pico) {
    window.picoTestResult = { pass: 0, fail: 1, failures: [{ name: 'harness', msg: 'window.pico missing (init failed?)' }] };
    return;
  }
  Promise.resolve().then(function () { runNext(0); });
})();
