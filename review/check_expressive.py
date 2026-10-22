"""Serve the portfolio first; run with python review/check_expressive.py.
Requires Playwright and /usr/bin/chromium. No app build dependencies.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
from playwright.sync_api import sync_playwright
import os, hashlib, json

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get('PORTFOLIO_TEST_URL', 'http://127.0.0.1:8090')
OUTPUT = Path(os.environ.get('PORTFOLIO_TEST_OUTPUT', str(ROOT/'review')))
OUTPUT.mkdir(exist_ok=True, parents=True)
results = []
class Audit(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.links=[]; self.h1=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.append(a['id'])
        if tag=='h1': self.h1+=1
        if tag=='img' and a.get('src'): assert a.get('alt'), a
        for key in ['href','src','poster']:
            if a.get(key): self.links.append(a[key])
parsed={}
for f in ROOT.glob('*.html'):
    a=Audit(); a.feed(f.read_text()); parsed[f.name]=a
    assert a.h1==1, (f.name,a.h1)
    assert len(a.ids)==len(set(a.ids)),f.name
for filename,a in parsed.items():
    for link in a.links:
        u=urlparse(link)
        if u.scheme or u.netloc: continue
        target=ROOT/unquote(u.path) if u.path else ROOT/filename
        assert target.is_file(),(filename,link)
        if u.fragment: assert u.fragment in parsed[target.name].ids,(filename,link)
results.append('PASS all six pages: local links, image alt text, anchors, unique IDs and heading semantics')
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    errors=[]; failures=[]
    page=browser.new_page()
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('response',lambda r:failures.append((r.url,r.status)) if r.status>=400 else None)
    page.goto(BASE+'/index.html',wait_until='domcontentloaded')
    # Check actual running animation objects and end-state styles, not CSS declarations.
    evidence=page.evaluate('''() => document.getAnimations().map(a => ({target:a.effect.target.dataset.hero || a.effect.target.className, duration:a.effect.getTiming().duration,delay:a.effect.getTiming().delay,keyframes:a.effect.getKeyframes().map(k=>({opacity:k.opacity, transform:k.transform}))}))''')
    assert len(evidence)>=7,evidence
    assert len({x['delay'] for x in evidence})>=4
    assert any(x['target']=='portrait' for x in evidence)
    assert any(x['target']=='line' for x in evidence)
    (OUTPUT/'animation-evidence.json').write_text(json.dumps(evidence,indent=2))
    page.wait_for_timeout(1500)
    assert page.locator('[data-hero="portrait"]').evaluate('(e)=>getComputedStyle(e).opacity')=='1'
    assert page.locator('[data-hero="line"]').first.evaluate('(e)=>getComputedStyle(e).transform')=='none'
    results.append('PASS real hero animations: staggered lines, portrait entrance, delayed supporting content, completed visible states')
    # Scroll-triggered animation must begin and finish, not remain hidden.
    target=page.locator('.pickwise-preview')
    assert target.evaluate('(e)=>getComputedStyle(e).opacity')=='0'
    page.evaluate('document.documentElement.style.scrollBehavior="auto"')
    target.scroll_into_view_if_needed(); page.wait_for_timeout(100)
    assert target.get_attribute('data-revealed')=='true'
    assert target.evaluate('(e)=>e.getAnimations().length')>0
    page.wait_for_timeout(1100)
    assert target.evaluate('(e)=>getComputedStyle(e).opacity')=='1'
    results.append('PASS project scroll reveal begins on intersection, animates and ends fully visible')
    before=page.locator('.pick-home').evaluate('(e)=>getComputedStyle(e).transform')
    target.hover();page.wait_for_timeout(850)
    after=page.locator('.pick-home').evaluate('(e)=>getComputedStyle(e).transform')
    assert before!=after,(before,after)
    results.append('PASS project hover produces screen movement; title/action transitions retained')
    # Test clicking a project through the transition and using Back.
    target.click();page.wait_for_url('**/pickwise.html');page.go_back();page.wait_for_url('**/index.html')
    assert page.locator('main').evaluate('(e)=>getComputedStyle(e).opacity')=='1'
    results.append('PASS animated case-study navigation and browser Back restore a usable page')
    for width in [1440,768,390,320]:
        page.set_viewport_size({'width':width,'height':1000})
        for filename in parsed:
            assert page.goto(BASE+'/'+filename).status==200
            page.evaluate('document.documentElement.style.scrollBehavior="auto"')
            page.locator('details').evaluate_all('(xs)=>xs.forEach(x=>x.open=true)')
            for image in page.locator('img[src]').all():
                image.scroll_into_view_if_needed()
                page.wait_for_function('(i)=>i.complete && i.naturalWidth>0',arg=image.element_handle())
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,filename)
            # No permanent clipping of headings or navigational containers.
            assert page.locator('h1').evaluate('(e)=>e.getBoundingClientRect().right<=innerWidth+1'),(filename,width)
            for video in page.locator('video').all():
                video.evaluate('(v)=>v.load()')
                page.wait_for_function('(v)=>v.readyState>=1 && v.duration>0 && v.videoWidth>0',arg=video.element_handle())
            results.append(f'PASS {width}px {filename}: no page overflow, images load, playable video metadata')
    page.set_viewport_size({'width':390,'height':844})
    page.goto(BASE+'/index.html');page.wait_for_timeout(1400)
    toggle=page.get_by_role('button',name='Menu',exact=True)
    toggle.focus();page.keyboard.press('Enter')
    menu=page.locator('.mobile-menu');assert menu.evaluate('(d)=>d.open')
    assert toggle.get_attribute('aria-expanded')=='true'
    page.wait_for_timeout(550)
    # Tab cycling stays in the modal (including the close button).
    for _ in range(8):
        page.keyboard.press('Tab')
        assert menu.evaluate('(d)=>d.contains(document.activeElement)')
    page.keyboard.press('Escape');assert not menu.evaluate('(d)=>d.open')
    assert toggle.evaluate('(e)=>e===document.activeElement')
    assert toggle.get_attribute('aria-expanded')=='false'
    toggle.click();menu.get_by_role('button',name='Close navigation').click();page.wait_for_timeout(220)
    assert not menu.evaluate('(d)=>d.open')
    toggle.click();menu.get_by_role('link',name='02 About').click();page.wait_for_url('**/index.html#about')
    assert not menu.evaluate('(d)=>d.open')
    toggle.click();page.set_viewport_size({'width':1000,'height':900});page.wait_for_function('!document.querySelector(".mobile-menu").open')
    results.append('PASS mobile menu: keyboard opening, focus containment, Escape/Close, focus return, links and desktop resize')
    page.goto(BASE+'/msn-academy.html');page.wait_for_timeout(1000)
    page.keyboard.press('Tab');assert page.locator('.skip-link').evaluate('(e)=>e===document.activeElement')
    page.keyboard.press('Enter');assert page.evaluate('location.hash')=='#main'
    link=page.locator('[data-zoom]').first;link.focus();page.keyboard.press('Enter')
    assert page.locator('.image-dialog').evaluate('(d)=>d.open')
    page.keyboard.press('Escape');assert not page.locator('.image-dialog').evaluate('(d)=>d.open')
    assert link.evaluate('(e)=>e===document.activeElement')
    results.append('PASS keyboard skip navigation and image dialog Escape/focus return')
    page.goto(BASE+'/index.html')
    names=page.locator('.creative-project h3').all_text_contents()
    assert [x.strip() for x in names]==['MSN Academy','Pickwise','Move Light'],names
    portrait=page.locator('.hero-portrait img')
    assert portrait.get_attribute('src')=='assets/mariyam-professional-portrait.jpg'
    assert portrait.get_attribute('fetchpriority')=='high'
    results.append('PASS featured project order and original portrait prominently in hero')
    nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
    np=nojs.new_page();np.goto(BASE+'/index.html')
    assert np.get_by_role('navigation',name='Main navigation').is_visible()
    assert not np.get_by_role('button',name='Menu',exact=True).is_visible()
    for el in np.locator('[data-reveal]').all():assert el.is_visible()
    np.goto(BASE+'/pickwise.html');np.locator('summary').click();assert np.locator('details').get_attribute('open') is not None
    results.append('PASS no-JavaScript navigation, content and native research disclosure')
    reduced=browser.new_context(reduced_motion='reduce',viewport={'width':390,'height':844})
    rp=reduced.new_page();rp.goto(BASE+'/index.html')
    assert rp.evaluate('document.getAnimations().length')==0
    assert rp.evaluate('getComputedStyle(document.documentElement).scrollBehavior')=='auto'
    for el in rp.locator('[data-reveal]').all():assert el.evaluate('(e)=>getComputedStyle(e).opacity')=='1'
    rp.get_by_role('button',name='Menu',exact=True).click();assert rp.locator('.mobile-menu').evaluate('(d)=>d.open')
    assert rp.evaluate('document.getAnimations().length')==0
    rp.keyboard.press('Escape')
    # Changing the preference mid-session must also reveal pending content.
    page.emulate_media(reduced_motion='reduce')
    page.wait_for_function('document.getAnimations().length===0',timeout=1000)
    assert page.evaluate('document.getAnimations().length')==0
    for el in page.locator('[data-reveal]').all():assert el.evaluate('(e)=>getComputedStyle(e).opacity')=='1'
    results.append('PASS initial and changed reduced-motion preference; menu usable without animation')
    assert not errors,errors
    assert not failures,failures
    results.append('PASS no JavaScript errors or local HTTP failures')
    browser.close()
(OUTPUT/'expressive-test-results.txt').write_text('\n'.join(results)+'\n')
print('\n'.join(results))
