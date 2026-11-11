// Behavioral reference; no framework or fixed visual theme required.
const $ = id => document.getElementById(id);
const panes = [$('slides'), $('notes')];
const controls = [$('previous'), $('next'), $('slide-index')];
let data, active = -1, cards = [], notes = [], frame = 0;
let dataURL;
function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}
function safeURL(value) {
  if (typeof value !== 'string' || !value.trim()) return null;
  try { const url = new URL(value, dataURL); return ['https:', 'http:'].includes(url.protocol) ? url.href : null; } catch { return null; }
}
function sourceLink(source) {
  const url = safeURL(source?.url);
  if (!url) return element('p', 'Source link unavailable.', 'source-note');
  const a = element('a', source.title || 'Original source', 'source-note'); a.href = url; return a;
}
function fallback(container, message = 'Slide image unavailable. Use the source link and text equivalent below.') {
  container.replaceChildren(element('p', message, 'media-fallback'));
}
function position(node, pane) { return node.getBoundingClientRect().top - pane.getBoundingClientRect().top + pane.scrollTop - pane.clientTop; }
function align(pane, node) { pane.scrollTo({top:position(node,pane),behavior:'instant'}); }
function select(index, {origin = 'navigation', history = 'push', focus = false} = {}) {
  index = Math.max(0, Math.min(data.slides.length - 1, index));
  const changed = active !== index; active = index;
  $('reader').dataset.selected = data.slides[index].id;
  cards.forEach((node,i) => node.setAttribute('aria-current',String(i===index)));
  notes.forEach((node,i) => node.setAttribute('aria-current',String(i===index)));
  $('slide-index').value = String(index);
  $('previous').disabled = index === 0; $('next').disabled = index === data.slides.length - 1;
  $('progress').textContent = `${index + 1} / ${data.slides.length}`;
  if (changed && !['slides','notes'].includes(origin)) $('status').textContent = `Slide ${index+1}: ${data.slides[index].title}`;
  if (origin !== 'slides') align(panes[0], cards[index]);
  if (origin !== 'notes') align(panes[1], notes[index]);
  const hash = '#slide=' + encodeURIComponent(data.slides[index].id);
  if (history !== 'none' && location.hash !== hash) window.history[history === 'push' ? 'pushState' : 'replaceState'](null,'',hash);
  if (focus) notes[index].querySelector('h2').focus({preventScroll:true});
}
function fromHash() {
  let id; try { id = decodeURIComponent(location.hash.replace(/^#slide=/,'')); } catch { id = ''; }
  const index = data.slides.findIndex(slide => slide.id === id);
  select(index < 0 ? 0 : index,{history:index < 0 ? 'replace' : 'none'});
}
function onScroll(pane, nodes, origin) {
  // Read only this pane. A reciprocal programmatic scroll sees the same active ID,
  // so it cannot bounce, recursively scroll, or add browser history entries.
  let index = 0;
  for (let i=0;i<nodes.length;i++) if (position(nodes[i],pane) <= pane.scrollTop + 24) index=i;
  if (index !== active) select(index,{origin,history:'replace'});
}
function geometry() {
  document.documentElement.style.setProperty('--header-height',`${$('reader-header').getBoundingClientRect().height}px`);
  if (active >= 0) { align(panes[0],cards[active]); align(panes[1],notes[active]); }
}
function validate(value) {
  if (!value || !Array.isArray(value.slides) || !value.slides.length) throw new Error('No slides are available.');
  const ids = new Set();
  for (const slide of value.slides) {
    if (typeof slide.id !== 'string' || !slide.id || ids.has(slide.id) || typeof slide.title !== 'string' || !Array.isArray(slide.explanation) || slide.explanation.some(p=>typeof p!=='string')) throw new Error('Slide data is incomplete or contains duplicate IDs.');
    ids.add(slide.id);
  }
  return value;
}
async function start() {
  const script = document.querySelector('script[data-source]');
  dataURL = new URL(script?.dataset.source || './demo-data.json',document.baseURI);
  const response = await fetch(dataURL); if (!response.ok) throw new Error(`Could not load lesson data (${response.status}).`);
  data = validate(await response.json());
  $('course-title').textContent = data.title || 'Course reader';
  $('course-description').textContent = data.description || '';
  $('slide-index').replaceChildren();
  data.slides.forEach((slide,i) => {
    const source = data.sources?.find(source => source.id === slide.source_id);
    const card = element('article',undefined,'slide-card'); card.dataset.slideId = slide.id;
    card.append(element('p',`Slide ${i+1} · source page ${slide.pdf_page ?? 'unavailable'}`,'eyebrow'),element('h2',slide.title));
    const media = element('div'); const imageURL = safeURL(slide.media?.url);
    if (imageURL) { const img = element('img'); img.alt = slide.media.alt || slide.title; img.loading='lazy'; img.width=800; img.height=450; img.addEventListener('error',()=>fallback(media),{once:true}); img.src=imageURL; media.append(img); }
    else fallback(media, 'No slide image supplied. The text equivalent remains available.');
    card.append(media,element('p',slide.keyIdea || slide.title,'key-idea'),sourceLink(source));
    const note = element('article',undefined,'slide-note'); note.id = 'note-' + slide.id;
    const heading = element('h2',slide.title); heading.tabIndex=-1;
    note.append(element('p',`Notes for slide ${i+1}`,'eyebrow'),heading,element('p',slide.keyIdea || '', 'key-idea'));
    slide.explanation.forEach(paragraph=>note.append(element('p',paragraph)));
    if(slide.caveat) note.append(element('p',slide.caveat,'caveat'));
    note.append(sourceLink(source));
    panes[0].append(card); panes[1].append(note); cards.push(card); notes.push(note);
    const option = element('option',`${i+1}. ${slide.title}`); option.value=String(i); $('slide-index').append(option);
  });
  controls.forEach(control=>control.disabled=false);
  document.querySelector('.skip').addEventListener('click',event=>{event.preventDefault();$('notes').focus();});
  geometry(); fromHash();
  panes[0].addEventListener('scroll',()=>onScroll(panes[0],cards,'slides'),{passive:true});
  panes[1].addEventListener('scroll',()=>onScroll(panes[1],notes,'notes'),{passive:true});
  $('previous').addEventListener('click',()=>select(active-1)); $('next').addEventListener('click',()=>select(active+1));
  $('slide-index').addEventListener('change',event=>select(Number(event.target.value)));
  panes.forEach(pane=>pane.addEventListener('keydown',event=>{
    // Do not steal keys from links, buttons, selects, or editable descendants.
    if(event.target !== pane || event.altKey || event.ctrlKey || event.metaKey) return;
    const targets={ArrowLeft:active-1,ArrowRight:active+1,Home:0,End:data.slides.length-1};
    if(event.key in targets){event.preventDefault();select(targets[event.key]);}
  }));
  window.addEventListener('popstate',fromHash); window.addEventListener('hashchange',fromHash);
  window.addEventListener('resize',()=>{cancelAnimationFrame(frame);frame=requestAnimationFrame(geometry);});
  $('reader').setAttribute('aria-busy','false');
}
start().catch(error=>{
  $('reader').setAttribute('aria-busy','false'); $('error').hidden=false;
  $('error').textContent=`Unable to open the reader: ${error.message} Check the data file and serve this folder over HTTP. Reload to retry.`;
  $('course-description').textContent='Reader unavailable; source data was not loaded.';
  controls.forEach(control=>control.disabled=true);
});
