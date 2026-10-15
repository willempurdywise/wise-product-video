"""Generate portable, synthetic storyboard inputs; no original product screenshots."""
from pathlib import Path
import json
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent / 'generated'
root.mkdir(exist_ok=True)
for name, title, button, color in [
    ('home','Your account','Review payment','white'),
    ('review','Review payment','Confirm and pay','white'),
    ('methods','Choose how to pay','Current account','white'),
    ('success','ALL SET','Done','#163300'),
]:
    im = Image.new('RGB',(390,844),color)
    d = ImageDraw.Draw(im)
    ink = 'white' if name == 'success' else '#163300'
    d.text((30,24),'9:41',fill=ink, font_size=18)
    if name == 'methods':
        d.rectangle((0,0,389,53),fill='#bfbfbf')
    d.text((28,140),title,fill=ink,font_size=28)
    d.text((28,220),'100.00 SGD',fill=ink,font_size=32)
    d.rounded_rectangle((16,756,374,804),radius=24,fill='#9FE870')
    d.text((70,770),button,fill='#163300',font_size=18)
    im.save(root/f'{name}.png')
scenes = [
    {'screen':'home','hold':1,'taps':[{'at':.88,'box':[16,756,374,804]}]},
    {'screen':'review','transition':{'type':'push'},'hold':1},
    {'screen':'methods','transition':{'type':'modal-in'},'hold':1},
    {'screen':'review','transition':{'type':'modal-out'},'hold':1,'taps':[{'at':1.48,'box':[16,756,374,804]}]},
    {'screen':'success','transition':{'type':'fade'},'hold':1.5,
     'overlays':[{'file':'@loader.gif','box':[160,350,70,70]}]},
]
config = {'screens':{name:{'file':f'{name}.png','flatten_radius':0} for name in ('home','review','methods','success')},'scenes':scenes}
(root/'storyboard.json').write_text(json.dumps(config,indent=2)+'\n')
print(root/'storyboard.json')

# A separate scrolling example keeps sticky chrome outside the content viewport.
content = Image.new('RGB',(390,1500),'white')
d = ImageDraw.Draw(content)
for i in range(15):
    d.rectangle((0,i*100,389,i*100+99),fill=('#eeeeee' if i%2 else 'white'))
    d.text((25,i*100+35),f'Transaction {i+1}',fill='#163300',font_size=24)
content.save(root/'long-content.png')
config['scenes'] = [{'screen':'home','hold':5,'scroll':{'file':'long-content.png','viewport':[0,100,390,620],'steps':[{'at':1,'duration':.45,'to':180},{'at':2.1,'duration':.55,'to':410},{'at':3.4,'duration':.4,'to':550}]}}]
(root/'scroll-storyboard.json').write_text(json.dumps(config,indent=2)+'\n')
