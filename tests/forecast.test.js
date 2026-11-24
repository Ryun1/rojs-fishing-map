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

  function redWarn() { return { awarenessLevelID: 'red', awarenessTypeName: 'Agitação Marítima', idAreaAviso: 'ACE', startTime: '2026-11-24T00:00:00', endTime: '2026-11-25T00:00:00' }; }

  test('all unsafe', function () {
    calmLive();
    pico.state.warn = [redWarn()];
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

  /* ---------- Task 4: offline copy, saved warnings, clearing what-if ---------- */
  test('status fresh', function () {
    var now = Date.now();
    ok(pico.statusText('live', now - 30 * 60000, now).indexOf('Forecast loaded ') === 0);
  });
  test('status old', function () {
    var now = Date.now(), t = pico.statusText('live', now - 5 * 3600000, now);
    ok(/5 h old$/.test(t), t);
    ok(t.indexOf('Forecast from ') === 0, t);
  });
  test('stale class', function () {
    calmLive();
    pico.state.live.at = Date.now() - 30 * 3600000; pico.state.source = 'live';
    pico.render();
    ok(document.getElementById('status').classList.contains('stale'));
  });
  test('saved warnings restore', function () {
    localStorage.setItem('pico-warn-v1', JSON.stringify({ at: Date.now(), list: [redWarn()] }));
    pico.state.warn = null; pico.restoreWarn();
    eq(pico.state.warn.length, 1);
    localStorage.setItem('pico-warn-v1', JSON.stringify({ at: Date.now() - 49 * 3600000, list: [redWarn()] }));
    pico.state.warn = null; pico.restoreWarn();
    eq(pico.state.warn.length, 1, 'kept at 49 h');
  });
  test('saved warnings dropped after 7 days or when malformed', function () {
    localStorage.setItem('pico-warn-v1', JSON.stringify({ at: Date.now() - 8 * 864e5, list: [redWarn()] }));
    pico.state.warn = null; pico.restoreWarn();
    eq(pico.state.warn, null);
    localStorage.setItem('pico-warn-v1', JSON.stringify({ at: Date.now(), list: 'red' }));
    pico.restoreWarn();
    eq(pico.state.warn, null, 'non-array list');
  });
  test('restored red warning makes every spot unsafe', function () {
    calmLive();
    localStorage.setItem('pico-warn-v1', JSON.stringify({ at: Date.now() - 50 * 3600000, list: [redWarn()] }));
    pico.state.warn = null; pico.restoreWarn();
    pico.rankSpots(T12, 3, '').forEach(function (x) { eq(x.level, 3); });
  });
  test('warnings note', function () {
    var n = document.getElementById('warnnote');
    pico.state.warnAt = null; pico.render();
    eq(n.textContent, 'Official warnings not checked.');
    calmLive();
    pico.state.warnAt = pico.state.live.at - 5 * 3600000; pico.render();
    ok(/^Official warnings not checked since \w{3} \d\d:\d\d\.$/.test(n.textContent), n.textContent);
    pico.state.warnAt = pico.state.live.at; pico.render();
    ok(n.hidden, 'hidden when current');
  });
  test('example values are not a forecast', function () {
    pico.state.live = null; pico.state.source = 'example';
    pico.rankSpots(T12, 3, '').forEach(function (x) { eq(x.level, null); });
    pico.state.len = 3; pico.state.fish = '';
    pico.renderRanked(pico.whenAt(T12));
    var m = document.getElementById('rankmsg');
    ok(!m.hidden && m.textContent.indexOf('No forecast loaded.') === 0, 'line shown');
    pico.dayTimeline(pico.SPOTS[0], 0, 2026, 11, 24, '').forEach(function (c) { eq(c.level, null); });
  });
  test('best times keeps stretches with a fish picked, with labels', function () {
    calmLive();
    pico.state.fish = pico.SPECIES[0].id;
    document.getElementById('f-date').value = '2026-11-24';
    document.getElementById('f-time').value = '10:00';
    pico.render();
    var b = document.getElementById('besttimes');
    ok(b.textContent.indexOf('Good') >= 0, 'stretches present');
    ok(b.querySelectorAll('.windows').length >= 1, 'windows list');
    ok(b.querySelector('.strip').getAttribute('aria-label').indexOf('Fishability: ') === 0, 'strip label');
    ok(b.querySelector('.bars').getAttribute('aria-label').indexOf(pico.SPECIES[0].name) >= 0, 'bars label');
  });
  test('all-day stretch reads All day', function () {
    calmLive(function (s, h) { return CALM; });
    pico.state.live = liveFixture(Date.UTC(2026, 10, 23, 0), 96, function () { return CALM; });
    pico.state.fish = '';
    document.getElementById('f-date').value = '2026-11-24';
    document.getElementById('f-time').value = '10:00';
    pico.render();
    var b = document.getElementById('besttimes');
    ok(b.textContent.indexOf('All day') >= 0, b.textContent.slice(0, 80));
    ok(b.textContent.indexOf('00:00\u201300:00') < 0, 'no 00:00-00:00');
  });
  /* From main (c60f382), adapted to the reviewed UI: the detail sits inside the spot list, the badge reads "No forecast",
     and the status pill reports the forecast's age while the summary says the time is past its end. */
  function badges() { return [].map.call(document.querySelectorAll('#spotlist .spotrow .badge'), function (b) { return b.textContent; }); }
  function setDay() { document.getElementById('f-date').value = '2026-11-24'; document.getElementById('f-time').value = '10:00'; pico.state.followNow = false; }
  test('past the forecast end the spot views show no data', function () {
    pico.state.live = liveFixture(Date.UTC(2026, 10, 24, 0), 12, function () { return CALM; });
    pico.state.source = 'live';
    setDay(); document.getElementById('f-time').value = '20:00';
    pico.render();
    var d = document.querySelector('#spotlist .detail');
    ok(d.textContent.indexOf('Fishable:') < 0, 'no Fishable badge');
    badges().forEach(function (t) { eq(t, 'No forecast'); });
    eq(badges().length, 5);
    eq(document.getElementById('h-sum').textContent, 'No forecast for this time');
  });
  test('example values show no data in the spot views', function () {
    pico.state.live = null; pico.state.source = 'example';
    setDay(); pico.render();
    ok(document.querySelector('#spotlist .detail').textContent.indexOf('Fishable:') < 0, 'no Fishable badge');
    badges().forEach(function (t) { eq(t, 'No forecast'); });
    eq(document.getElementById('status').textContent, 'No forecast');
  });
  test('typed values still rate the spots', function () {
    pico.state.live = null; pico.state.source = 'manual';
    setDay(); pico.render();
    var b = badges();
    eq(b.length, 5);
    b.forEach(function (t) { ok(t !== 'No forecast', 'real level'); });
  });
  test('flat scores say so instead of All day', function () {
    pico.state.live = liveFixture(Date.UTC(2026, 10, 23, 0), 96, function () { return CALM; });
    pico.state.source = 'live';
    pico.state.fish = 'sargo';
    /* Sargo's time-of-day weights vary, so flatten them for this test. */
    var sargo = pico.SPECIES.filter(function (x) { return x.id === 'sargo'; })[0], saved = sargo.time;
    sargo.time = { dawn: 1, day: 1, dusk: 1, night: 1 };
    try {
      setDay(); pico.render();
      var t = document.getElementById('besttimes').textContent, nm = sargo.name;
      ok(/scores about the same all day \(\d+–\d+\), so no time stands out\./.test(t), t);
      ok(t.indexOf(nm + ' scores about') >= 0, 'fish name');
      ok(t.indexOf('All day ' + nm) < 0, 'no All day window');
    } finally { sargo.time = saved; }
  });
  test('best times note names the picked fish', function () {
    pico.state.live = liveFixture(Date.UTC(2026, 10, 23, 0), 96, function () { return CALM; });
    pico.state.source = 'live';
    setDay();
    pico.state.fish = ''; pico.render();
    ok(document.getElementById('besttimes').textContent.indexOf('Pick a fish above') >= 0, 'prompt without fish');
    pico.state.fish = pico.SPECIES[0].id; pico.render();
    var t = document.getElementById('besttimes').textContent;
    ok(t.indexOf('The bars show the ' + pico.SPECIES[0].name + ' score.') >= 0, t);
    ok(t.indexOf('Pick a fish above') < 0, 'no prompt');
  });
  test('ranked row press keeps focus', function () {
    calmLive();
    pico.render();
    var rows = document.querySelectorAll('#ranked .spotrow'), r = rows[2];
    r.focus(); r.click();
    ok(document.activeElement && document.activeElement.classList.contains('spotrow'), 'focus on a row');
    eq(document.activeElement.getAttribute('data-spot'), r.getAttribute('data-spot'));
  });
  test('explicit failed load switches back to the saved forecast', function () {
    calmLive(); pico.state.source = 'manual'; pico.state.tideAuto = false;
    window.fetch = function () { return Promise.reject(new Error('offline')); };
    return pico.loadLive(true).then(function () {
      eq(pico.state.source, 'live'); eq(pico.state.tideAuto, true);
      ok(document.getElementById('livemsg').textContent.indexOf('saved on this phone') >= 0);
      pico.state.source = 'manual';
      return pico.loadLive(false);
    }).then(function () {
      eq(pico.state.source, 'manual');
      eq(document.getElementById('livemsg').textContent, 'Could not reach Open-Meteo. Your typed values are in use.');
    });
  });
  test('clear what-if', function () {
    calmLive(); pico.state.source = 'manual'; pico.render();
    var b = document.getElementById('b-clear');
    ok(!b.hidden, 'visible');
    pico.state.tideAuto = false;
    b.click();
    eq(pico.state.source, 'live');
    eq(pico.state.tideAuto, true);
    ok(b.hidden, 'hidden');
  });
  test('auto load keeps manual', function () {
    var fx = liveFixture(Date.UTC(2026, 10, 24, 0), 48, function () { return CALM; });
    var realFetch = window.fetch;
    window.fetch = function (u) {
      var body = String(u).indexOf('marine-api') >= 0 ? fx.m.map(function (x) { return { hourly: x }; })
        : String(u).indexOf('api.open-meteo') >= 0 ? fx.w.map(function (x) { return { hourly: x }; }) : [];
      return Promise.resolve({ ok: true, json: function () { return Promise.resolve(body); } });
    };
    pico.state.source = 'manual';
    return pico.loadLive(false).then(function () {
      eq(pico.state.source, 'manual');
      return pico.loadLive(true);
    }).then(function () {
      eq(pico.state.source, 'live');
      window.fetch = realFetch;
    }, function (e) { window.fetch = realFetch; throw e; });
  });

  /* ---------- UI review: no made-up ratings, summary, week view, species rows, tabs, catch cards ---------- */
  function at(date, time) {
    document.getElementById('f-date').value = date; document.getElementById('f-time').value = time;
    pico.state.followNow = false;
  }
  function texts(sel) { return [].map.call(document.querySelectorAll(sel), function (e) { return e.textContent; }); }
  /* A calm forecast for 9 days from the start of yesterday (UTC), so it covers the real "today" the week view starts from. */
  function weekLive(fn) {
    var d = new Date(), start = Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate() - 1);
    pico.state.live = liveFixture(start, 24 * 9, function (s, h) { return fn ? (fn(s, h) || CALM) : CALM; });
    pico.state.source = 'live';
  }

  test('no forecast means no ratings anywhere', function () {
    pico.state.live = null; pico.state.source = 'live';
    at('2026-11-24', '10:00'); pico.render();
    texts('#spotlist .spotrow .badge').forEach(function (t) { eq(t, 'No forecast'); });
    [].forEach.call(document.querySelectorAll('#map-spots .mk'), function (g) { ok(/no forecast$/.test(g.getAttribute('aria-label')), g.getAttribute('aria-label')); });
    eq(document.getElementById('h-sum').textContent, 'No forecast for this time');
    eq(document.querySelectorAll('#rank .fishrow').length, pico.SPECIES.length, 'fish still ranked by season');
    ok(document.getElementById('besttimes').textContent.indexOf('High tide') >= 0 || document.getElementById('besttimes').textContent.indexOf('Low tide') >= 0, 'tides still shown');
  });
  test('typed values rate the spots, with a banner', function () {
    pico.state.live = null; pico.state.source = 'manual';
    at('2026-11-24', '10:00'); pico.render();
    texts('#spotlist .spotrow .badge').forEach(function (t) { ok(t !== 'No forecast', t); });
    ok(document.getElementById('manualbanner').textContent.indexOf('Using your own conditions') >= 0, 'banner');
  });
  test('fish scores use their own words', function () {
    calmLive(); at('2026-11-24', '10:00'); pico.render();
    var words = texts('#rank .score small');
    eq(words.length, pico.SPECIES.length);
    words.forEach(function (w) { ok(['Likely', 'Possible', 'Unlikely'].indexOf(w) >= 0, w); });
  });
  test('time-of-day reasons read naturally', function () {
    ['dawn', 'day', 'dusk', 'night'].forEach(function (ph) {
      pico.SPECIES.forEach(function (sp) {
        var r = pico.scoreFor(sp, pico.SPOTS[0], { month: 11, anom: 0, eff: 0.5, phase: ph, moving: true, danger: false });
        ok(!/Weaker at (day|night)/.test(r.why), r.why);
      });
    });
  });
  test('tapping a fish shows its score breakdown', function () {
    calmLive(); at('2026-11-24', '10:00'); pico.render();
    var d = document.querySelector('#rank details');
    eq(d.querySelectorAll('.factors li').length, 5);
    d.open = true;
    return new Promise(function (res) { setTimeout(res, 0); }).then(function () {
      pico.render();
      ok(document.querySelector('#rank details[data-fishd="' + d.getAttribute('data-fishd') + '"]').open, 'stays open after a re-render');
      pico.state.openFish = {};
    });
  });
  test('summary names the best spot and stays off unsafe ones', function () {
    calmLive(function (s) { return s === 0 ? unsafeFor(0) : null; });
    pico.state.spot = pico.SPOTS[0].id; at('2026-11-24', '10:00'); pico.render();
    var h = document.getElementById('h-sum').textContent;
    ok(h.indexOf(pico.SPOTS[0].name) < 0, h);
    ok(/Good$/.test(h), h);
    ok(document.querySelector('#summary [data-goto]'), 'show button for another spot');
    pico.state.warn = [{ awarenessLevelID: 'red', awarenessTypeName: 'Agitação Marítima', idAreaAviso: 'ACE', startTime: '2026-11-24T00:00:00', endTime: '2026-11-25T00:00:00' }];
    pico.render();
    eq(document.getElementById('h-sum').textContent, 'Stay off the rocks');
  });
  test('best spot for each fish leaves out Poor and Unsafe spots', function () {
    calmLive(function (s) { return s === 0 ? unsafeFor(0) : null; });
    at('2026-11-24', '10:00'); pico.render();
    eq(document.querySelectorAll('#grid tbody tr').length, pico.SPECIES.length);
    eq(document.querySelectorAll('#grid [data-spot="' + pico.SPOTS[0].id + '"]').length, 0);
  });
  test('week view: 7 days by 5 spots, worst hour per part of the day', function () {
    weekLive(function (s) { return s === 2 ? unsafeFor(2) : null; });
    pico.render();
    var cells = document.querySelectorAll('#week [data-week]');
    eq(cells.length, 35);
    [].forEach.call(cells, function (b) {
      eq(b.querySelectorAll('.seg').length, 3);
      if (b.getAttribute('data-week').split('|')[1] === pico.SPOTS[2].id) eq(b.querySelectorAll('.seg.l3').length, 3, b.getAttribute('aria-label'));
    });
    eq([].filter.call(cells, function (b) { return b.tabIndex === 0; }).length, 1, 'one tab stop');
  });
  test('tapping a week box picks that day, spot and part of the day', function () {
    weekLive();
    pico.render();
    var b = document.querySelectorAll('#week [data-week]')[7], v = b.getAttribute('data-week').split('|');
    b.click();
    eq(document.getElementById('f-date').value, v[0]);
    eq(pico.state.spot, v[1]);
    eq(document.getElementById('f-time').value, '06:00');
    eq(document.getElementById('f-len').value, '6');
  });
  test('week view says when typed values are in use', function () {
    weekLive(); pico.state.source = 'manual'; pico.render();
    eq(document.querySelectorAll('#week [data-week]').length, 0);
    ok(document.getElementById('week').textContent.indexOf('your own values') >= 0);
  });
  test('following now hides the Now button until the time is changed', function () {
    calmLive(); pico.state.followNow = true; pico.render();
    ok(document.getElementById('b-now').hidden, 'hidden while following');
    var t = document.getElementById('f-time');
    t.value = '09:00'; t.dispatchEvent(new Event('input', { bubbles: true }));
    eq(pico.state.followNow, false);
    ok(!document.getElementById('b-now').hidden, 'shown after a change');
  });
  test('the best-times timeline moves the time with the arrow keys', function () {
    calmLive(); at('2026-11-24', '10:00'); pico.render();
    var s = document.getElementById('scrub');
    s.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true }));
    eq(document.getElementById('f-time').value, '10:30');
    s = document.getElementById('scrub');
    s.dispatchEvent(new KeyboardEvent('keydown', { key: 'Home', bubbles: true }));
    eq(document.getElementById('f-time').value, '00:00');
  });
  test('focus survives a re-render', function () {
    weekLive(); pico.render();
    var b = document.querySelectorAll('#week [data-week]')[3], v = b.getAttribute('data-week');
    b.focus(); pico.render();
    eq(document.activeElement && document.activeElement.getAttribute('data-week'), v);
  });
  test('tabs show one panel at a time', function () {
    pico.showTab('seasons', false);
    ok(document.getElementById('p-forecast').hidden && !document.getElementById('p-seasons').hidden, 'seasons shown');
    eq(document.getElementById('t-seasons').getAttribute('aria-selected'), 'true');
    pico.showTab('forecast', false);
    ok(!document.getElementById('p-forecast').hidden, 'forecast back');
  });

  /* ---------- Phase 3: species model ---------- */
  function S(id) { return pico.SPECIES.filter(function (x) { return x.id === id; })[0]; }
  function P(id) { return pico.SPOTS.filter(function (x) { return x.id === id; })[0]; }
  test('normal on day 366', function () {
    var v = pico.sstNormal(2028, 12, 31);
    ok(typeof v === 'number' && !isNaN(v), 'number: ' + v);
    eq(v, pico.sstNormal(2027, 12, 31));
  });
  test('normal follows the year', function () {
    ok(pico.sstNormal(2026, 8, 20) > 22 && pico.sstNormal(2026, 3, 1) < 17, pico.sstNormal(2026, 8, 20) + ' / ' + pico.sstNormal(2026, 3, 1));
  });
  test('steepness', function () {
    eq(pico.steepOf(P('madalena')), 0);
    ok(pico.steepOf(P('saoroque')) > 0.95, 'saoroque');
    var l = pico.steepOf(P('lajes'));
    ok(l > 0.5 && l < 0.6, 'lajes ' + l);
  });
  test('species fields', function () {
    pico.SPECIES.forEach(function (sp) {
      ok(typeof sp.base === 'number' && sp.base > 0 && sp.base <= 1, sp.id + ' base');
      ok(typeof sp.deep === 'number' && sp.deep >= -1 && sp.deep <= 1, sp.id + ' deep');
      ok(typeof sp.warm === 'number', sp.id + ' warm');
      ok(sp.ev && ['measured', 'estimated'].indexOf(sp.ev.time) >= 0, sp.id + ' ev.time');
    });
    eq(S('veja').time.night, 0);
  });
  function cx(o) {
    var c = { month: 7, anom: 0, eff: 0.8, phase: 'dawn', moving: true, danger: false };
    for (var k in o) c[k] = o[k];
    return c;
  }
  var PHASES = ['dawn', 'day', 'dusk', 'night'];
  test('every fish can reach Possible', function () {
    pico.SPECIES.forEach(function (sp) {
      var best = 0;
      for (var m = 1; m <= 12; m++) PHASES.forEach(function (ph) {
        pico.SPOTS.forEach(function (spot) { best = Math.max(best, pico.scoreFor(sp, spot, cx({ month: m, phase: ph })).score); });
      });
      ok(best >= 45, sp.id + ' best ' + best);
    });
  });
  test('rare fish rank lower out of season', function () {
    var c = cx({ month: 11, phase: 'day' }), sargo = pico.scoreFor(S('sargo'), P('ponta'), c).score;
    ok(sargo > pico.scoreFor(S('amberjack'), P('ponta'), c).score, 'amberjack');
    ok(sargo > pico.scoreFor(S('bonito'), P('ponta'), c).score, 'bonito');
  });
  test('veja at night', function () {
    var r = pico.scoreFor(S('veja'), P('ponta'), cx({ phase: 'night' }));
    eq(r.score, 0);
    ok(r.why.indexOf('Does not feed after dark') >= 0, r.why);
  });
  test('habitat', function () {
    var c = cx({ month: 8, phase: 'dusk' });
    ok(pico.scoreFor(S('barracuda'), P('saoroque'), c).score > pico.scoreFor(S('barracuda'), P('madalena'), c).score, 'bicuda deeper is better');
    ok(pico.scoreFor(S('sargo'), P('madalena'), c).score >= pico.scoreFor(S('sargo'), P('saoroque'), c).score, 'sargo shelf');
  });
  test('temperature only counts from 1 degree', function () {
    function sc(a) { return pico.scoreFor(S('barracuda'), P('ponta'), cx({ month: 8, phase: 'dawn', anom: a })); }
    eq(sc(0.9).score, sc(0).score);
    ok(sc(2).score > sc(0).score, 'warmer helps');
    ok(sc(-2).score < sc(0).score, 'cooler hurts');
    ok(sc(-2).why.indexOf('cooler than normal') >= 0, sc(-2).why);
  });
  test('missing sea temperature', function () {
    var r = pico.scoreFor(S('barracuda'), P('ponta'), cx({ anom: null }));
    ok(isFinite(r.score), 'finite');
    eq(r.adj.temp, 0);
  });
  test('unsafe cap', function () {
    pico.SPECIES.forEach(function (sp) { ok(pico.scoreFor(sp, P('ponta'), cx({ danger: true })).score <= 15, sp.id); });
  });
  test('score range', function () {
    pico.SPECIES.forEach(function (sp) {
      pico.SPOTS.forEach(function (spot) {
        PHASES.forEach(function (ph) {
          [-3, 0, 3].forEach(function (a) {
            [0, 1, 3].forEach(function (e) {
              for (var m = 1; m <= 12; m++) {
                var s = pico.scoreFor(sp, spot, cx({ month: m, phase: ph, anom: a, eff: e })).score;
                ok(s === Math.round(s) && s >= 0 && s <= 100, sp.id + ' ' + s);
              }
            });
          });
        });
      });
    });
  });
  test('evidence in reasons', function () {
    PHASES.forEach(function (ph) {
      pico.SPECIES.forEach(function (sp) {
        pico.SPOTS.forEach(function (spot) {
          [1, 7].forEach(function (m) {
            var w = pico.scoreFor(sp, spot, cx({ month: m, phase: ph })).why;
            ok(/\((measured|estimated|angler lore)\)\.$|good spot for it\.$/.test(w), w);
          });
        });
      });
    });
  });
  test('no forecast ranks by base and season', function () {
    pico.state.live = null; pico.state.source = 'live';
    at('2026-07-15', '10:00'); pico.render();
    var first = document.querySelector('#rank .sname');
    ok(first && first.textContent.indexOf(S('amberjack').name) < 0, first && first.textContent);
  });
  test('breakdown shows evidence', function () {
    calmLive(); at('2026-11-24', '10:00'); pico.render();
    var d = document.querySelector('#rank details[data-fishd="veja"]');
    ok(d, 'veja row');
    var t = d.textContent;
    ok(t.indexOf('measured') >= 0, 'measured');
    ok(t.indexOf('estimated') >= 0, 'estimated');
    ok(t.indexOf('multiplied together') >= 0, 'multiplied');
  });
  test('sea line says normal', function () {
    calmLive(); at('2026-11-24', '10:00'); pico.render();
    var a = 19 - pico.sstNormal(2026, 11, 24), t = document.querySelector('#spotlist .detail').textContent;
    var want = Math.abs(a) < 1 ? 'about normal for the date' : (a > 0 ? 'warmer than normal' : 'cooler than normal');
    ok(t.indexOf(want) >= 0, want + ' in ' + t);
  });
  test('conditions row adds up', function () {
    calmLive(function () { var c = {}; for (var k in CALM) c[k] = CALM[k]; c.sst = 20.5; return c; });
    at('2026-11-24', '10:00'); pico.render();
    var d = document.querySelector('#rank details[data-fishd="veja"]');
    var row = d.querySelectorAll('.factors li')[4].querySelector('.v').textContent.replace('−', '-');
    var note = d.querySelector('.factors + p').textContent.replace(/−/g, '-');
    var parts = note.match(/\(([-+]?\d+), estimated\); swell ([-+]?\d+) and tide ([-+]?\d+)/);
    ok(parts, note);
    eq(parseInt(row, 10), parseInt(parts[1], 10) + parseInt(parts[2], 10) + parseInt(parts[3], 10));
  });
  test('what-if without a sea temperature still rates', function () {
    pico.state.live = null; pico.state.source = 'manual';
    document.getElementById('f-temp').value = '';
    setDay(); pico.render();
    var b = badges();
    eq(b.length, 5);
    b.forEach(function (t) { ok(t !== 'No forecast', 'rated: ' + t); });
    ok(document.querySelector('#spotlist .detail').textContent.indexOf('temperature unknown') >= 0, 'sea unknown');
  });
  test('fallback reason only for strong scores', function () {
    /* Sargo at Ponta in March by day: every part just above its limit, score Possible. */
    var r = pico.scoreFor(S('sargo'), P('ponta'), cx({ month: 3, phase: 'day' }));
    ok(r.score < 70, 'score ' + r.score);
    ok(r.why.indexOf('good spot for it') < 0, r.why);
    ok(/\((measured|estimated|angler lore)\)\.$/.test(r.why), r.why);
  });
  test('how-to has no temperature gate', function () {
    var t = document.getElementById('howto').textContent;
    ok(t.indexOf('multiplied') >= 0, 'multiplied');
    ok(t.indexOf('cap the total') < 0, 'no cap');
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
