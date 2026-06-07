// Benjamin Michels preview — interactions
(function () {
  var header = document.getElementById('header');
  var progress = document.getElementById('scrollProgress');
  var hamburger = document.getElementById('hamburger');
  var mobileNav = document.getElementById('mobileNav');
  var sticky = document.getElementById('stickyCta');

  function onScroll() {
    var y = window.scrollY || document.documentElement.scrollTop;
    if (header) header.classList.toggle('scrolled', y > 20);
    if (progress) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = (h > 0 ? (y / h) * 100 : 0) + '%';
    }
    if (sticky) {
      var nearEnd = (window.innerHeight + y) > (document.body.scrollHeight - 220);
      sticky.classList.toggle('show', y > 700 && !nearEnd);
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile nav
  if (hamburger && mobileNav) {
    hamburger.addEventListener('click', function () {
      hamburger.classList.toggle('active');
      mobileNav.classList.toggle('active');
      document.body.style.overflow = mobileNav.classList.contains('active') ? 'hidden' : '';
    });
    mobileNav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        hamburger.classList.remove('active');
        mobileNav.classList.remove('active');
        document.body.style.overflow = '';
      });
    });
  }

  // Reveal on scroll
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });

  // Count-up stats
  function animateCount(el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    if (isNaN(target)) return;
    var dur = 1400, start = null;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased).toLocaleString('de-DE');
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var statsRow = document.getElementById('statsRow');
  if (statsRow) {
    var sObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.querySelectorAll('[data-count]').forEach(animateCount);
          sObs.unobserve(e.target);
        }
      });
    }, { threshold: 0.4 });
    sObs.observe(statsRow);
  }

  // FAQ accordion
  document.querySelectorAll('.faq-q').forEach(function (q) {
    q.addEventListener('click', function () {
      var item = q.closest('.faq-item');
      var a = item.querySelector('.faq-a');
      var open = item.classList.toggle('open');
      q.querySelector('.faq-tog').textContent = open ? '+' : '+';
      a.style.maxHeight = open ? a.scrollHeight + 'px' : '0';
    });
  });

  // Service tabs
  var tabs = document.getElementById('tabs');
  if (tabs) {
    tabs.querySelectorAll('.tab-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var key = btn.getAttribute('data-tab');
        tabs.querySelectorAll('.tab-btn').forEach(function (b) { b.classList.toggle('active', b === btn); });
        document.querySelectorAll('.tab-panel').forEach(function (p) {
          p.classList.toggle('active', p.getAttribute('data-panel') === key);
        });
      });
    });
  }

  // Pflegekassen-Zuschuss calculator (Pflegegrad -> monthly subsidy)
  var rGrad = document.getElementById('rGrad');
  if (rGrad) {
    var PFLEGEGELD = { 1: 0, 2: 347, 3: 599, 4: 800, 5: 990 }; // €/Monat 2025
    var ENTLASTUNG = 131; // Entlastungsbetrag €/Monat
    var fmt = function (n) { return n.toLocaleString('de-DE'); };
    var GRADTXT = { 1: 'Pflegegrad 1', 2: 'Pflegegrad 2', 3: 'Pflegegrad 3', 4: 'Pflegegrad 4', 5: 'Pflegegrad 5' };
    function recalc() {
      var g = parseInt(rGrad.value, 10);
      var zuschuss = PFLEGEGELD[g] + ENTLASTUNG;
      var gv = document.getElementById('vGrad'); if (gv) gv.textContent = GRADTXT[g];
      document.getElementById('calcOut').textContent = 'bis zu ' + fmt(zuschuss) + ' €';
    }
    rGrad.addEventListener('input', recalc);
    recalc();
  }

  // Multi-step wizard
  var form = document.getElementById('leadForm');
  if (form) {
    var steps = form.querySelectorAll('.wstep');
    var bar = document.getElementById('wbar');
    var cur = 0;
    function show(i) {
      steps.forEach(function (s, idx) { s.classList.toggle('active', idx === i); });
      if (bar) bar.style.width = ((i + 1) / steps.length * 100) + '%';
      cur = i;
    }
    form.querySelectorAll('.opt input[type="radio"]').forEach(function (input) {
      input.addEventListener('change', function () {
        var group = input.closest('.opts');
        group.querySelectorAll('.opt').forEach(function (o) { o.classList.remove('sel'); });
        input.closest('.opt').classList.add('sel');
        setTimeout(function () { if (cur < steps.length - 1) show(cur + 1); }, 240);
      });
    });
    form.querySelectorAll('[data-next]').forEach(function (b) {
      b.addEventListener('click', function () { if (cur < steps.length - 1) show(cur + 1); });
    });
    form.querySelectorAll('[data-prev]').forEach(function (b) {
      b.addEventListener('click', function () { if (cur > 0) show(cur - 1); });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault(); // preview only — no submission
      steps.forEach(function (s) { s.classList.remove('active'); });
      if (bar) bar.style.width = '100%';
      var ok = document.getElementById('wsuccess');
      if (ok) ok.classList.add('show');
    });
    show(0);
  }

  var yr = document.getElementById('year');
  if (yr) yr.textContent = new Date().getFullYear();
})();
