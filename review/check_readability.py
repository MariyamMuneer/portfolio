"""Checks for the type/contrast, contact and pointer-interaction refinement."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os
BASE=os.environ.get('PORTFOLIO_TEST_URL','http://127.0.0.1:8090')
OUT=Path(os.environ.get('PORTFOLIO_TEST_OUTPUT',str(Path(__file__).parent)))
results=[]
def luminance(rgb):
 channels=[int(x)/255 for x in rgb]
 linear=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in channels]
 return sum(a*b for a,b in zip(linear,[.2126,.7152,.0722]))
def contrast(fg,bg):
 lo,hi=sorted([luminance(fg),luminance(bg)]);return (hi+.05)/(lo+.05)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 context=browser.new_context(permissions=['clipboard-read','clipboard-write'],viewport={'width':1440,'height':1000})
 page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(BASE+'/index.html');page.wait_for_timeout(1500)
 assert int(page.locator('body').evaluate('(e)=>getComputedStyle(e).fontWeight'))>=500
 assert int(page.locator('h1').evaluate('(e)=>getComputedStyle(e).fontWeight'))>=600
 assert page.locator('.hero-summary').evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)')>=16
 assert page.locator('.creative-preview').first.evaluate('(e)=>parseFloat(getComputedStyle(e).borderRadius)')>=24
 for selector,bg in [('.hero-summary',[245,241,233]),('.short-description',[245,241,233]),('.site-footer h2',[37,38,43]),('.google-blue',[255,255,255]),('.google-red',[255,255,255]),('.google-yellow',[255,255,255]),('.google-green',[255,255,255]),('.coursera-word',[255,255,255])]:
  color=page.locator(selector).first.evaluate('(e)=>getComputedStyle(e).color')
  rgb=[int(x.strip()) for x in color[color.index('(')+1:color.index(')')].split(',')[:3]]
  ratio=contrast(rgb,bg);assert ratio>=4.5,(selector,ratio)
  results.append(f'PASS text contrast {selector}: {ratio:.2f}:1')
 card=page.locator('.academy-preview');page.evaluate('document.documentElement.style.scrollBehavior="auto"');card.scroll_into_view_if_needed();page.wait_for_timeout(1100)
 box=card.bounding_box();page.mouse.move(box['x']+box['width']*.8,box['y']+box['height']*.3);page.wait_for_timeout(500)
 assert card.evaluate('(e)=>e.style.getPropertyValue("--tilt-x")')!=''
 assert 'cursor-open.svg' in card.evaluate('(e)=>getComputedStyle(e).cursor')
 page.mouse.move(5,5);page.wait_for_timeout(400)
 assert card.evaluate('(e)=>e.style.getPropertyValue("--tilt-x")')==''
 results.append('PASS desktop pointer tilt responds and resets; contextual native SVG cursor with pointer fallback')
 page.locator('#about').scroll_into_view_if_needed();page.wait_for_timeout(250)
 assert page.get_by_role('navigation',name='Main navigation').get_by_role('link',name='About').get_attribute('aria-current')=='location'
 assert page.locator('.reading-progress').evaluate('(e)=>getComputedStyle(e).transform')!='matrix(0, 0, 0, 1, 0, 0)'
 results.append('PASS reading position indicator and active About navigation update while scrolling')
 assert 'coursera.org/learn/foundations-user-experience-design' in page.locator('.education-link').get_attribute('href')
 page.get_by_role('button',name='Copy email').click()
 page.wait_for_function('document.querySelector(".copy-status").textContent === "Email copied"')
 assert page.evaluate('navigator.clipboard.readText()')=='termezimariyam@gmail.com'
 results.append('PASS copy-email action copies the correct address and announces confirmation')
 page.emulate_media(reduced_motion='reduce');card.scroll_into_view_if_needed();box=card.bounding_box();page.mouse.move(box['x']+box['width']*.7,box['y']+box['height']*.3);page.wait_for_timeout(100)
 assert card.evaluate('(e)=>e.style.getPropertyValue("--tilt-x")')==''
 results.append('PASS reduced motion disables pointer tilt')
 for width in [390,320]:
  page.set_viewport_size({'width':width,'height':900});page.goto(BASE+'/index.html')
  assert page.locator('.short-description').first.evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)')>=15
  assert page.locator('.creative-about-facts dd').first.evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)')>=14
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.goto(BASE+'/pickwise.html');page.wait_for_timeout(50)
  assert page.locator('.story-copy>p').first.evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)')>=16
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  results.append(f'PASS larger homepage and case-study type fits at {width}px')
 assert not errors,errors
 browser.close()
OUT.mkdir(parents=True,exist_ok=True);(OUT/'readability-test-results.txt').write_text('\n'.join(results)+'\n')
print('\n'.join(results))
