// Benjamin Michels preview — micro-interactions
(function () {
  var header = document.getElementById('header');
  var progress = document.getElementById('scrollProgress');
  var hamburger = document.getElementById('hamburger');
  var mobileNav = document.getElementById('mobileNav');

  function onScroll() {
    var y = window.scrollY || document.documentElement.scrollTop;
    if (header) header.classList.toggle('scrolled', y > 20);
    if (progress) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = (h > 0 ? (y / h) * 100 : 0) + '%';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

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

  // Current year
  var yr = document.getElementById('year');
  if (yr) yr.textContent = new Date().getFullYear();
})();

// Booking placeholder — no real endpoint in the preview
function bookingPlaceholder(e) {
  e.preventDefault();
  alert('Platzhalter: Hier wird dein echter Buchungslink eingebunden (z. B. Calendly / Cal.com).');
  return false;
}
