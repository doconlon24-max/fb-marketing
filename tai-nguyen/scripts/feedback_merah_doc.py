"""Ảnh FEEDBACK kiểu 2 – XẾP DỌC (hợp ảnh vùng mắt/môi chụp ngang). 1080x1350, nền nâu chocolate ánh vàng.
Logo kem trên cùng · TÊN DỊCH VỤ vàng ánh kim + chữ nghiêng · 2 ảnh ngang xếp dọc đổ bóng · nhãn BEFORE/AFTER · dòng lợi ích.
python feedback_merah_doc.py <truoc|-> <sau|-> "<DỊCH VỤ>" <ra.jpg>  (bản gọn: ảnh to tối đa, ít chữ)
Dùng '-' thay ảnh để ra khung mẫu trống. Chỉ dùng ảnh khách MERAH thật."""
import sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R='tai-nguyen/thuong-hieu/'
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
            if a[0]<=t<=b[0]: u=(t-a[0])/(b[0]-a[0]) if b[0]>a[0] else 0; c=tuple(int(x+(y-x)*u) for x,y in zip(a[1],b[1])); break
        d.line([(0,i),(w,i)] if vertical else [(i,0),(i,h)],fill=c)
    return g
GOLD=[(0,(255,240,200)),(0.42,(226,186,118)),(0.58,(184,136,70)),(1,(250,226,176))]
def gold_text(bg,cx,y,text,ft,sp=0,glow=True):
    d0=ImageDraw.Draw(bg); ws=[d0.textlength(c,font=ft) for c in text]; tw=int(sum(ws)+sp*(len(text)-1)); a,dd=ft.getmetrics()
    m=Image.new('L',(tw+8,a+dd+8),0); dm=ImageDraw.Draw(m); x=4
    for c,w in zip(text,ws): dm.text((x,4),c,font=ft,fill=255); x+=w+sp
    X,Y=int(cx-m.width/2),int(y)
    if glow:
        gl=Image.new('RGBA',m.size,(255,200,120,0)); gl.putalpha(m.filter(ImageFilter.GaussianBlur(10)).point(lambda v:int(v*0.45))); bg.paste(gl,(X,Y),gl)
    sh=Image.new('RGBA',m.size,(20,8,2,0)); sh.putalpha(m.point(lambda v:int(v*0.6))); sh=sh.filter(ImageFilter.GaussianBlur(3)); bg.paste(sh,(X+2,Y+4),sh)
    bg.paste(grad(m.width,m.height,GOLD),(X,Y),m)
def fit(im,w,h):
    r=w/h
    if im.width/im.height>r: nw=int(im.height*r); x=(im.width-nw)//2; im=im.crop((x,0,x+nw,im.height))
    else: nh=int(im.width/r); y=(im.height-nh)//2; im=im.crop((0,y,im.width,y+nh))
    return im.resize((w,h),Image.LANCZOS)
def tag(bg,x,y,text,dark):
    ft=F('Montserrat.ttf',26,700); d=ImageDraw.Draw(bg); sp=6
    tw=sum(d.textlength(c,font=ft) for c in text)+sp*(len(text)-1); w,h=int(tw+60),54
    sh=Image.new('RGBA',(w+30,h+30),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([15,19,w+15,h+19],h//2,fill=(0,0,0,110)); sh=sh.filter(ImageFilter.GaussianBlur(7)); bg.paste(sh,(x-15,y-15),sh)
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle([0,0,w-1,h-1],h//2,fill=255)
    fill=grad(w,h,[(0,(92,58,36)),(1,(54,32,20))]) if dark else grad(w,h,GOLD)
    bg.paste(fill,(x,y),m); xx=x+30; col=(246,224,178) if dark else (60,36,22)
    for c in text: d.text((xx,y+12),c,font=ft,fill=col); xx+=d.textlength(c,font=ft)+sp
def main(truoc,sau,dv,ra,ghichu=None,*_):
    W,H=1080,1350
    bg=grad(W,H,[(0,(46,28,18)),(0.5,(74,46,30)),(1,(36,22,14))])
    glow=Image.new('L',(W,H),0); gd=ImageDraw.Draw(glow)
    gd.ellipse([W*0.1,-260,W*0.9,420],fill=150); gd.ellipse([-300,H*0.55,W*0.5,H*1.1],fill=60); gd.ellipse([W*0.6,H*0.3,W*1.3,H*0.8],fill=50)
    glow=glow.filter(ImageFilter.GaussianBlur(120)); bg.paste(Image.new('RGB',(W,H),(196,140,78)),(0,0),glow)
    # dải trên gọn: logo nhỏ + tên dịch vụ (ảnh chiếm tối đa)
    TOP=132; M=14; GAP=12
    lg=Image.open(R+'logo/LOGO_MERAH_kem_tach_nen.png').convert('RGBA'); lg=lg.crop(lg.getbbox()); lh=66
    lg=lg.resize((int(lg.width*lh/lg.height),lh),Image.LANCZOS); bg.paste(lg,((W-lg.width)//2,12),lg)
    gold_text(bg,W/2,80,dv.upper(),F('Cinzel.ttf',38,700),sp=8,glow=False)
    pw=W-2*M; ph=(H-TOP-M-GAP)//2; x=M; ys=[TOP,TOP+ph+GAP]
    for i,(fn,lab) in enumerate([(truoc,'BEFORE'),(sau,'AFTER')]):
        y=ys[i]
        if fn and fn!='-': im=fit(Image.open(fn).convert('RGB'),pw,ph)
        else:
            im=grad(pw,ph,[(0,(120,92,72)),(1,(90,66,50))]); dd=ImageDraw.Draw(im)
            dd.text((pw/2,ph/2),('Ảnh trước' if i==0 else 'Ảnh sau'),font=F('Montserrat.ttf',30,400),fill=(200,175,150),anchor='mm')
        sh=Image.new('RGBA',(pw+60,ph+60),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([30,38,pw+30,ph+38],22,fill=(0,0,0,140))
        sh=sh.filter(ImageFilter.GaussianBlur(12)); bg.paste(sh,(x-30,y-30),sh)
        m=Image.new('L',(pw,ph),0); ImageDraw.Draw(m).rounded_rectangle([0,0,pw-1,ph-1],22,fill=255); bg.paste(im,(x,y),m)
        tag(bg,x+18,y+ph-70,lab,dark=(i==0))
    if ghichu: ImageDraw.Draw(bg).text((W-22,TOP-14),ghichu,font=F('Montserrat.ttf',17,400),fill=(214,188,150),anchor='rd')
    bg.save(ra,quality=93); return ra
if __name__=='__main__':
    a=sys.argv[1:]; g=a[a.index('--ghi-chu')+1] if '--ghi-chu' in a else None; main(*a[:4],ghichu=g)
