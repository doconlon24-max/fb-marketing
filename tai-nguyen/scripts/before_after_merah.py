"""Ảnh Before/After chuẩn MERAH (4:5): logo trên, 2 ảnh cạnh nhau, tên dịch vụ, dòng phụ.
python before_after_merah.py <truoc> <sau> "<DỊCH VỤ>" "<dòng phụ>" <ra.jpg> [--ghi-chu "AI simulation · illustrative only"]"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R='tai-nguyen/thuong-hieu/'
KEM=(246,238,228); KEM2=(236,224,207); NAU=(74,46,34); VANG=(201,164,106); VANG2=(232,207,160)
def font(f,s,w=None):
    ft=ImageFont.truetype(R+'font/'+f,s)
    if w:
        try: ft.set_variation_by_axes([w])
        except Exception: pass
    return ft
def spaced(d,xy_center_y,text,ft,fill,sp,W):
    ws=[d.textlength(c,font=ft) for c in text]; tot=sum(ws)+sp*(len(text)-1); x=(W-tot)/2
    for c,w in zip(text,ws): d.text((x,xy_center_y),c,font=ft,fill=fill); x+=w+sp
def main(truoc,sau,dv,phu,ra,ghichu=None):
    W,H=1080,1350; bg=Image.new('RGB',(W,H),KEM); d=ImageDraw.Draw(bg)
    for y in range(H):
        t=abs(y/H-0.45)*1.6; c=tuple(int(a+(b-a)*min(t,1)) for a,b in zip(KEM,KEM2)); d.line([(0,y),(W,y)],fill=c)
    # khung viền vàng đôi
    d.rounded_rectangle([28,28,W-28,H-28],36,outline=VANG,width=3)
    d.rounded_rectangle([42,42,W-42,H-42],28,outline=VANG2,width=1)
    # logo
    lg=Image.open(R+'logo/LOGO_MERAH_nau_tach_nen.png').convert('RGBA'); bb=lg.getbbox(); lg=lg.crop(bb)
    lh=170; lg=lg.resize((int(lg.width*lh/lg.height),lh),Image.LANCZOS); bg.paste(lg,((W-lg.width)//2,80),lg)
    # 2 ảnh
    pw,ph=446,600; gap=36; top=300; x0=(W-2*pw-gap)//2
    for i,(fn,lab) in enumerate([(truoc,'BEFORE'),(sau,'AFTER')]):
        im=Image.open(fn).convert('RGB'); r=pw/ph
        if im.width/im.height>r: nw=int(im.height*r); im=im.crop(((im.width-nw)//2,0,(im.width-nw)//2+nw,im.height))
        else: nh=int(im.width/r); im=im.crop((0,0,im.width,nh))
        im=im.resize((pw,ph),Image.LANCZOS); x=x0+i*(pw+gap)
        sh=Image.new('RGBA',(pw+60,ph+60),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([30,38,pw+30,ph+38],26,fill=(74,46,34,60))
        sh=sh.filter(ImageFilter.GaussianBlur(14)); bg.paste(sh,(x-30,top-30),sh)
        d.rounded_rectangle([x-6,top-6,x+pw+6,top+ph+6],30,fill=VANG2,outline=VANG,width=2)
        m=Image.new('L',(pw,ph),0); ImageDraw.Draw(m).rounded_rectangle([0,0,pw,ph],24,fill=255); bg.paste(im,(x,top),m)
        ft=font('Montserrat.ttf',24,600); tw=sum(d.textlength(c,font=ft) for c in lab)+5*(len(lab)-1)
        bw=tw+56; bx=x+(pw-bw)/2; by=top+ph-24
        d.rounded_rectangle([bx,by,bx+bw,by+48],24,fill=NAU,outline=VANG,width=2)
        xx=bx+28
        for c in lab: d.text((xx,by+10),c,font=ft,fill=VANG2); xx+=d.textlength(c,font=ft)+5
    # tên dịch vụ
    y=top+ph+70
    ft=font('Cinzel.ttf',104,600); spaced(d,y,dv.upper(),ft,NAU,10,W)
    y+=150
    d.line([(W/2-150,y),(W/2-22,y)],fill=VANG,width=2); d.line([(W/2+22,y),(W/2+150,y)],fill=VANG,width=2)
    d.regular_polygon((W/2,y,8),4,fill=VANG)
    ft=font('CormorantGaramond-Italic.ttf',54,500); d.text(((W-d.textlength(phu,font=ft))/2,y+18),phu,font=ft,fill=(138,90,50))
    if ghichu:
        ft=font('Montserrat.ttf',17,400); d.text(((W-d.textlength(ghichu,font=ft))/2,H-72),ghichu,font=ft,fill=(160,135,110))
    bg.save(ra,quality=93); return ra
if __name__=='__main__':
    a=sys.argv[1:]; g=a[a.index('--ghi-chu')+1] if '--ghi-chu' in a else None
    main(a[0],a[1],a[2],a[3],a[4],g)
