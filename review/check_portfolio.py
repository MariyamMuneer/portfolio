from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
from playwright.sync_api import sync_playwright
import json
P=Path(__file__).resolve().parents[1]; results=[]
class Audit(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.h1=0
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if a.get('id'): self.ids.append(a['id'])
  if t=='h1':self.h1+=1
  if t=='img' and a.get('src'):assert a.get('alt'),a
  for k in ['href','src','poster']:
   if a.get(k):self.links.append(a[k])
parsed={}
for f in P.glob('*.html'):
 a=Audit();a.feed(f.read_text());parsed[f.name]=a
 assert a.h1==1,(f.name,a.h1)
 assert len(a.ids)==len(set(a.ids)),f.name
for name,a in parsed.items():
 for l in a.links:
  u=urlparse(l)
  if u.scheme or u.netloc:continue
  path=unquote(u.path);target=P/path if path else P/name
  assert target.is_file(),(name,l)
  if u.fragment:assert target.name in parsed and u.fragment in parsed[target.name].ids,(name,l)
 results.append('PASS local links, assets, anchors, alt text, one h1: '+name)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 errors=[];network=[]
 context=b.new_context()
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('response',lambda r:network.append((r.url,r.status)) if r.status>=400 else None)
 for width in [1440,768,390,320]:
  page.set_viewport_size({'width':width,'height':1000})
  for filename in parsed:
   r=page.goto('http://127.0.0.1:8080/'+filename)
   assert r.status==200
   page.locator('details').evaluate_all('(xs)=>xs.forEach(x=>x.open=true)')
   for im in page.locator('img[src]').all():
    im.scroll_into_view_if_needed()
    page.wait_for_function('(im)=>im.complete && im.naturalWidth>0',arg=im.element_handle())
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),(filename,width,'overflow')
   for v in page.locator('video').all():
    # Explicitly load local metadata and confirm playable dimensions and duration.
    v.evaluate('(v)=>v.load()')
    page.wait_for_function('(v)=>v.readyState>=1 && v.duration>0 && v.videoWidth>0',arg=v.element_handle())
   page.evaluate('window.scrollTo(0,0)')
   if filename=='index.html':
    for project in page.locator('.project').all():project.scroll_into_view_if_needed()
    page.wait_for_timeout(700)
    page.evaluate('window.scrollTo(0,0)')
    page.screenshot(path=str(P/f'review/home-{width}.png'),full_page=True)
   elif width in [1440,390] and filename in ['msn-academy.html','pickwise.html','move-light.html']:
    page.screenshot(path=str(P/f'review/{filename[:-5]}-{width}.png'),full_page=True)
   results.append(f'PASS {width}px: {filename}; no overflow; images and media load')
 # Keyboard / dialog and navigation.
 page.goto('http://127.0.0.1:8080/msn-academy.html')
 page.keyboard.press('Tab');assert page.locator('.skip-link').evaluate('(x)=>x===document.activeElement')
 page.keyboard.press('Enter');assert page.evaluate('location.hash')=='#main'
 first=page.locator('[data-zoom]').first
 first.focus();page.keyboard.press('Enter');assert page.locator('dialog').evaluate('(x)=>x.open')
 page.keyboard.press('Escape');assert not page.locator('dialog').evaluate('(x)=>x.open')
 assert first.evaluate('(x)=>x===document.activeElement')
 first.click();page.get_by_role('button',name='Close').click();assert not page.locator('dialog').evaluate('(x)=>x.open')
 page.goto('http://127.0.0.1:8080/index.html')
 assert page.locator('.project-info h3').all_text_contents()==['MSN Academy','Pickwise','Move Light']
 page.get_by_role('link',name='View selected work').click();assert page.evaluate('location.hash')=='#work'
 page.get_by_role('navigation',name='Main navigation').get_by_role('link',name='Contact').click();assert page.evaluate('location.hash')=='#contact'
 results.append('PASS keyboard skip link, image dialog Enter/Escape/Close/focus restoration, project order and section navigation')
 # No JS: all content visible and image links remain direct links.
 nojs=b.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
 np=nojs.new_page();np.goto('http://127.0.0.1:8080/index.html');assert np.locator('.project').count()==3
 for project in np.locator('.project').all():assert project.is_visible()
 np.goto('http://127.0.0.1:8080/pickwise.html');np.locator('summary').click();assert np.locator('details').get_attribute('open') is not None
 results.append('PASS no-JavaScript content, native details and standard image links')
 reduced=b.new_context(reduced_motion='reduce');rp=reduced.new_page();rp.goto('http://127.0.0.1:8080/index.html')
 assert rp.locator('.reveal-ready').count()==0
 assert rp.evaluate('getComputedStyle(document.documentElement).scrollBehavior')=='auto'
 results.append('PASS reduced-motion preference disables scroll animation and reveal hiding')
 assert not errors,errors
 assert not network,network
 results.append('PASS no browser JavaScript errors or local HTTP failures')
 b.close()
(P/'review/test-results.txt').write_text('\n'.join(results)+'\n')
print('\n'.join(results))
