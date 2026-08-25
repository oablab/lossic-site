#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=1200,630; BG=(246,245,238); INK=(51,59,43); MUTED=(117,125,102)
card=Image.new('RGB',(W,H),BG)
glow=Image.new('L',(W,H),0); ImageDraw.Draw(glow).ellipse([160,40,700,580],fill=60); glow=glow.filter(ImageFilter.GaussianBlur(80))
card=Image.composite(Image.new('RGB',(W,H),(168,179,148)),card,glow)
icon=Image.open('icon.png').convert('RGBA').resize((300,300),Image.Resampling.LANCZOS);card.paste(icon,(140,165),icon)
d=ImageDraw.Draw(card); bold=ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc',96,index=1); reg=ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc',34,index=0)
d.text((520,170),'Lossic',font=bold,fill=INK)
for y,line in [(320,'The lossless player'),(366,'that tells the story'),(412,'behind your music.')]: d.text((524,y),line,font=reg,fill=MUTED)
card.save('og.png')
print('og.png',card.size)
