{
  const burger = document.querySelector('.burger');
  const mnav = document.getElementById('mnav');
  if (burger && mnav) {
    burger.addEventListener('click', () => {
      const open = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', String(!open));
      mnav.classList.toggle('open', !open);
      document.body.style.overflow = open ? '' : 'hidden';
    });
    mnav.addEventListener('click', e => {
      if (e.target.closest('a')) { burger.setAttribute('aria-expanded', 'false'); mnav.classList.remove('open'); document.body.style.overflow = ''; }
    });
  }

  // Contact form: opens the visitor's email app addressed to the office.
  // Swap the action for your host's form handler (Netlify Forms, Formspree, etc.) to receive submissions directly.
  const form = document.querySelector('form.qf');
  if (form && !form.hasAttribute('data-hosted')) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const d = new FormData(form);
      const lines = [...d.entries()].filter(([, v]) => String(v).trim()).map(([k, v]) => `${k}: ${v}`);
      const subject = `Service request - ${d.get('Service') || 'General'} - ${d.get('Name') || ''}`;
      const href = `mailto:office@haleshvac.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join('\n'))}`;
      const msg = form.querySelector('.msg');
      if (msg) msg.textContent = 'Opening your email app… If nothing opens, email office@haleshvac.com or call 706-765-7219.';
      window.location.href = href;
    });
  }
}
