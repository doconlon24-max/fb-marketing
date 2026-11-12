"""Ảnh FEEDBACK trước/sau gửi khách (mẫu sếp 11/11/2026, vuông 1080): dải trên kem-vàng (BEFORE · logo · AFTER),
2 ảnh cạnh nhau, vạch vàng giữa có hạt kim cương, dải dưới nâu đồng có TÊN DỊCH VỤ vàng ánh kim + dòng phụ.
python feedback_merah.py <truoc> <sau> "<DỊCH VỤ>" "<dòng phụ>" <ra.jpg> [--ghi-chu "..."]
Dùng ảnh khách thật (đã che mắt/được đồng ý). Ảnh AI thì bắt buộc --ghi-chu "AI simulation · illustrative only"."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R='tai-nguyen/thuong-hieu/'
NAU=(74,46,34); VANG=(201,164,106); VANG2=(240,214,160); DONG1=(59,36,22); DONG2=(138,90,50)
def F(f,s,w=None):
    ft=ImageFont.truetype(R+'font/'+f,s)
    if w:
        try: ft.set_variation_by_axes([w])
        except Exception: pass
    return ft
def grad(w,h,stops,vertical=True):
    g=Image.new('RGB',(w,h)); d=ImageDraw.Draw(g); n=h if vertical else w
    for i in range(n):
        t=i/max(n-1,1)
        for k in range(len(stops)-1):
            a,b=stops[k],stops[k+1]
            if a[0]<=t<=b[0]: u=(t-a[0])/(b[0]-a[0]); c=tuple(int(x+(y-x)*u) for x,y in zip(a[1],b[1])); break
        d.line([(0,i),(w,i)] if vertical else [(i,0),(i,h)],fill=c)
    return g
GOLD=[(0,(250,232,188)),(0.45,(214,172,104)),(0.55,(190,145,80)),(1,(246,222,170))]
def gold_text(bg,xy,text,ft,sp=0):
    d0=ImageDraw.Draw(bg); ws=[d0.textlength(c,font=ft) for c in text]; tw=int(sum(ws)+sp*(len(text)-1)); asc,desc=ft.getmetrics()
    m=Image.new('L',(tw+4,asc+desc+4),0); dm=ImageDraw.Draw(m); x=0
    for c,w in zip(text,ws): dm.text((x,0),c,font=ft,fill=255); x+=w+sp
    sh=Image.new('RGBA',m.size,(30,15,5,0)); sh.putalpha(m.point(lambda v:v*0.55)); sh=sh.filter(ImageFilter.GaussianBlur(3))
    X,Y=int(xy[0]-tw/2),int(xy[1]); bg.paste(sh,(X+2,Y+3),sh); bg.paste(grad(m.width,m.height,GOLD),(X,Y),m)
def pill(bg,cx,cy,text,ft,h=62):
    d=ImageDraw.Draw(bg); tw=d.textlength(text,font=ft); w=int(tw+70); x,y=int(cx-w/2),int(cy-h/2)
    sh=Image.new('RGBA',(w+30,h+30),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([15,19,w+15,h+19],h//2,fill=(90,60,30,80))
    sh=sh.filter(ImageFilter.GaussianBlur(6)); bg.paste(sh,(x-15,y-15),sh)
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle([0,0,w-1,h-1],h//2,fill=255)
    bg.paste(grad(w,h,[(0,(252,244,226)),(1,(236,214,172))]),(x,y),m)
    d.rounded_rectangle([x,y,x+w-1,y+h-1],h//2,outline=VANG,width=3)
    d.text((cx,cy),text,font=ft,fill=NAU,anchor='mm')
def fit(im,w,h,top_bias=0.25):
    r=w/h
    if im.width/im.height>r: nw=int(im.height*r); x=(im.width-nw)//2; im=im.crop((x,0,x+nw,im.height))
    else: nh=int(im.width/r); y=int((im.height-nh)*top_bias); im=im.crop((0,y,im.width,y+nh))
    return im.resize((w,h),Image.LANCZOS)
def main(truoc,sau,dv,phu,ra,ghichu=None):
    W=H=1080; TOP=150; BOT=170; B=14
    bg=grad(W,H,[(0,(250,240,222)),(0.14,(236,212,170)),(0.15,(120,80,45)),(0.84,(120,80,45)),(0.85,DONG2),(1,DONG1)])
    # dải trên: ánh sáng
    top=grad(W,TOP,[(0,(252,245,230)),(0.5,(246,232,205)),(1,(232,206,160))]); bg.paste(top,(0,0))
    # dải dưới nâu đồng có quầng sáng
    bot=grad(W,BOT,[(0,(110,70,38)),(0.5,DONG1),(1,(44,26,15))]); glow=Image.new('L',(W,BOT),0)
    ImageDraw.Draw(glow).ellipse([W*0.2,-BOT*0.4,W*0.8,BOT*1.2],fill=110); glow=glow.filter(ImageFilter.GaussianBlur(60))
    bot.paste(Image.new('RGB',(W,BOT),(170,120,65)),(0,0),glow); bg.paste(bot,(0,H-BOT))
    # 2 ảnh: không viền kẻ, chỉ đổ bóng mềm
    G=26; ph=H-TOP-BOT-2*G+10; pw=(W-3*G)//2; y0=TOP+G-6
    mid=grad(W,H-TOP-BOT,[(0,(248,238,220)),(1,(236,220,194))]); bg.paste(mid,(0,TOP))
    for i,fn in enumerate([truoc,sau]):
        im=fit(Image.open(fn).convert('RGB'),pw,ph); x=G+i*(pw+G)
        sh=Image.new('RGBA',(pw+80,ph+80),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([40,48,pw+40,ph+48],22,fill=(70,40,20,120))
        sh=sh.filter(ImageFilter.GaussianBlur(16)); bg.paste(sh,(x-40,y0-40),sh)
        m=Image.new('L',(pw,ph),0); ImageDraw.Draw(m).rounded_rectangle([0,0,pw-1,ph-1],22,fill=255); bg.paste(im,(x,y0),m)
    d=ImageDraw.Draw(bg); cx=W//2
    dm=Image.new('L',(56,120),0); ImageDraw.Draw(dm).polygon([(28,0),(56,60),(28,120),(0,60)],fill=255)
    ds=Image.new('RGBA',(96,160),(0,0,0,0)); ds.paste((60,35,15,140),(20,24),dm); ds=ds.filter(ImageFilter.GaussianBlur(6)); bg.paste(ds,(cx-48,y0+ph//2-80),ds)
    bg.paste(grad(56,120,[(0,(252,236,190)),(0.5,(196,150,82)),(1,(250,228,180))],vertical=False),(cx-28,y0+ph//2-60),dm)
    # dải trên: BEFORE · logo · AFTER
    ft=F('Cinzel.ttf',36,700); pill(bg,175,TOP//2+2,'BEFORE',ft); pill(bg,W-175,TOP//2+2,'AFTER',ft)
    lg=Image.open(R+'logo/LOGO_MERAH_nau_tach_nen.png').convert('RGBA'); lg=lg.crop(lg.getbbox())
    lh=112; lg=lg.resize((int(lg.width*lh/lg.height),lh),Image.LANCZOS); bg.paste(lg,((W-lg.width)//2,(TOP-lh)//2+2),lg)
    # dải dưới: tên dịch vụ
    gold_text(bg,(W/2,H-BOT+18),dv.upper(),F('Cinzel.ttf',78,700),sp=12)
    y=H-BOT+112; d=ImageDraw.Draw(bg)
    d.text((W/2,y+16),phu,font=F('CormorantGaramond-Italic.ttf',42,600),fill=VANG2,anchor='mm')
    if ghichu: d.text((W-24,H-14),ghichu,font=F('Montserrat.ttf',15,400),fill=(200,170,130),anchor='rd')
    bg.save(ra,quality=93); return ra
if __name__=='__main__':
    a=sys.argv[1:]; g=a[a.index('--ghi-chu')+1] if '--ghi-chu' in a else None
    main(a[0],a[1],a[2],a[3],a[4],g)
