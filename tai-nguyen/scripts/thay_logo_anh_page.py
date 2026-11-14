import sys, numpy as np
from PIL import Image, ImageFilter
src, out, box, cx, top, w = sys.argv[1], sys.argv[2], list(map(int, sys.argv[3].split(','))), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
im = Image.open(src).convert('RGB'); a = np.array(im).astype(float)
x0,y0,x1,y1 = box
# tô nền: nội suy dọc giữa hàng ngay trên và ngay dưới hộp (nền kem mượt), lấy trung bình 6px
from numpy.lib.stride_tricks import sliding_window_view as sw
def sm(v,k=81):
    pad=np.pad(v,((k//2,k//2),(0,0)),mode='edge'); return np.stack([np.convolve(pad[:,c],np.ones(k)/k,mode='valid') for c in range(3)],1)
t = sm(np.median(a[y0-10:y0-2, x0:x1],axis=0)); b = sm(np.median(a[y1+2:y1+10, x0:x1],axis=0))
for i,y in enumerate(range(y0,y1)):
    k=(i+1)/(y1-y0+1); a[y,x0:x1]=t*(1-k)+b*k
fill = Image.fromarray(a.astype('uint8'))
# làm mịn nhẹ mép hộp
blur = fill.filter(ImageFilter.GaussianBlur(6)); m = Image.new('L', im.size, 0)
m.paste(255, (x0,y0,x1,y1)); m = m.filter(ImageFilter.GaussianBlur(3))
fill = Image.composite(blur, fill, m) if False else fill
logo = Image.open('/home/user/merah-he-thong/tai-nguyen/mau-thiet-ke/logo_dark.png').convert('RGBA')
h = int(logo.height * w / logo.width); logo = logo.resize((w,h), Image.LANCZOS); A=np.array(logo); A[...,0]=88;A[...,1]=48;A[...,2]=36; logo=Image.fromarray(A)
fill = fill.convert('RGBA'); fill.alpha_composite(logo, (cx - w//2, top))
fill.convert('RGB').save(out, quality=95)
print(logo.size)
