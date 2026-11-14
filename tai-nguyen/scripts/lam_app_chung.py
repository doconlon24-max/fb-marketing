"""Tạo SPA MARKETING (bản dùng chung) từ merah-studio/src.html.
Chạy: python lam_app_chung.py <thu muc merah-studio> <thu muc app-chung> <chk.js>"""
import io, re, sys
SRC, OUT, CHK = sys.argv[1], sys.argv[2], sys.argv[3]
s = io.open(SRC + "/src.html", encoding="utf-8").read().replace("\r\n", "\n")
def rep(a, b, cnt=1):
    global s
    assert a in s, "KHONG THAY: " + a[:100]
    s = s.replace(a, b, cnt)
def sub(pat, b, flags=0, need=True):
    global s
    n = len(re.findall(pat, s, flags))
    assert n or not need, "KHONG THAY regex: " + pat
    s = re.sub(pat, b, s, flags=flags)

# ---- tiêu đề, thương hiệu
rep("<title>QUẢN TRỊ MERAH</title>", "<title>SPA MARKETING</title>")
rep('<div class="brand"><h1>MERAH Studio</h1><span>Makati · nội dung fanpage</span></div>',
    '<div class="brand"><h1 id="brandName">SPA MARKETING</h1><span id="brandSub">Quản trị fanpage &amp; quảng cáo</span></div><button class="btn small ghost" id="openSetup" title="Cài đặt thương hiệu, page, Drive, Sheet">⚙ Cài đặt</button>')
rep('const ARTIFACT_NAME="MERAH Studio";', 'const ARTIFACT_NAME="SPA MARKETING";')
rep('{{ID_KET_NOI}}', '__APP_SLUG__', cnt=99)
rep('const LOGO_LIGHT="__LOGO_LIGHT__", LOGO_DARK="__LOGO_DARK__";', 'let LOGO_LIGHT="", LOGO_DARK="";')

# ---- hằng số MERAH -> cấu hình riêng từng người
sub(r'const PAGES=\[[^\]]*\];', 'let PAGES=["Page của tôi"];')
rep('const GROUPS=', 'let GROUPS=')
rep('const TIMES=', 'let TIMES=')
sub(r'const RULES=`[^`]*`;', '''let RULES=`Quy tắc thương hiệu (sửa trong ⚙ Cài đặt):
- Viết đúng sự thật, không bịa số liệu, không hứa kết quả tuyệt đối.
- Tuân thủ chính sách quảng cáo của Meta.`;''')
sub(r'const CAPTION_STYLE=`[^`]*`;', '''let CAPTION_STYLE=`Phong cách caption: câu ngắn, xuống dòng nhiều, emoji vừa phải, có hook dòng đầu, có lời kêu gọi nhắn tin, cuối bài 5–8 hashtag.`;''')
rep('cho MERAH Beauty', 'cho ${BRAND}', cnt=9)
sub(r'const FIX_IMG_FOLDER="[^"]*";', 'let FIX_IMG_FOLDER="";')
sub(r'const SHEET_ID="[^"]*", SHEET_SERVER="Google Sheets";', 'let SHEET_ID="";const SHEET_SERVER="Google Sheets";')
sub(r'const DRIVE="Google Drive", ADS_SRV="META ADS", AD_ACC="[^"]*";', 'const DRIVE="Google Drive", ADS_SRV="META ADS";let AD_ACC="";')
sub(r'const FOLD=\{[^}]*\};', 'let FOLD={};')
sub(r'const QC_SUB=\[\[.*?\]\];', 'let QC_SUB=[];', flags=re.S)

# ---- nút "Mở thư mục gốc" -> theo cấu hình
for k, fid in [("p-nguon", "{{ID_DRIVE}}"), ("p-tp", "{{ID_DRIVE}}"),
               ("q-nguon", "{{ID_DRIVE}}"), ("q-tp", "{{ID_DRIVE}}")]:
    rep(f'<a class="btn" target="_blank" rel="noopener" href="https://drive.google.com/drive/folders/{fid}">Mở thư mục gốc</a>',
        f'<a class="btn" target="_blank" rel="noopener" data-fold="{k}" href="#">Mở thư mục gốc</a>')

# ---- trang Thư mục & liên kết: dựng từ cấu hình
sub(r'(<section class="view" id="v-f-all">).*?(</section>)', r'''\1
    <div class="head"><div><h2>Thư mục &amp; liên kết</h2><p>Thư mục Drive và bảng tính của bạn (tạo trong ⚙ Cài đặt). Bấm để mở tab mới.</p></div></div>
    <div class="stack" id="linksBox"></div>
  \2''', flags=re.S)

# ---- hộp thoại cài đặt
rep('<div class="toast" id="toast" role="status"></div>', '''<dialog id="setupDlg" aria-labelledby="suTitle" style="width:min(640px,calc(100% - 24px));max-height:calc(100vh - 24px)">
  <div class="dlg-h"><h3 id="suTitle">Cài đặt SPA MARKETING</h3></div>
  <form id="setupForm" method="dialog" style="padding:0 18px 4px;display:grid;gap:12px;overflow:auto;max-height:calc(100vh - 170px)">
    <p class="note" style="margin:0">Mỗi người dùng có dữ liệu riêng: bài, ý tưởng, cài đặt chỉ bạn thấy. App dùng Google Drive, Google Sheets, Meta Ads của <b>chính tài khoản bạn</b> (bật kết nối trên claude.ai).</p>
    <label class="f">Tên thương hiệu *<input id="suBrand" required placeholder="VD: Lily Spa"></label>
    <label class="f">Khu vực / thành phố<input id="suCity" placeholder="VD: Quận 1, TP.HCM"></label>
    <label class="f">Các fanpage (mỗi dòng 1 page) *<textarea id="suPages" rows="3" required placeholder="Lily Spa Quận 1&#10;Lily Spa Clinic"></textarea></label>
    <label class="f">Giờ đăng mỗi ngày (cách nhau dấu phẩy)<input id="suTimes" placeholder="07:00, 11:00, 19:00"></label>
    <label class="f">ID tài khoản quảng cáo Meta (chỉ số, không có act_)<input id="suAd" inputmode="numeric" placeholder="VD: 1234567890"></label>
    <label class="f">Quy tắc thương hiệu (dịch vụ, giá, chữ cấm dùng…)<textarea id="suRules" rows="4"></textarea></label>
    <label class="f">Phong cách caption + chữ ký cuối bài (địa chỉ, SĐT, hashtag)<textarea id="suCap" rows="3"></textarea></label>
    <label class="f">Logo (tuỳ chọn, PNG nền trong)<input type="file" id="suLogo" accept="image/*"></label>
    <fieldset style="border:1px solid var(--line);border-radius:12px;padding:10px 12px"><legend class="note">Google Drive &amp; Sheet</legend>
      <label style="display:flex;gap:8px;align-items:center"><input type="radio" name="suMode" value="new" checked> Tự tạo thư mục Drive + Google Sheet mới cho tôi (khuyên dùng)</label>
      <label style="display:flex;gap:8px;align-items:center"><input type="radio" name="suMode" value="old"> Dùng thư mục / Sheet có sẵn (dán link)</label>
      <div id="suOld" hidden style="display:grid;gap:8px;margin-top:8px">
        <label class="f">Link Google Sheet<input id="suSheet" placeholder="https://docs.google.com/spreadsheets/d/…"></label>
        <label class="f">Thư mục TƯ LIỆU ĐĂNG BÀI<input id="suF1" placeholder="link thư mục Drive"></label>
        <label class="f">Thư mục THÀNH PHẨM (page)<input id="suF2"></label>
        <label class="f">Thư mục TƯ LIỆU QUẢNG CÁO<input id="suF3"></label>
        <label class="f">Thư mục SPA (trong TƯ LIỆU QUẢNG CÁO)<input id="suF5"></label>
        <label class="f">Thư mục SPY (trong TƯ LIỆU QUẢNG CÁO)<input id="suF6"></label>
        <label class="f">Thư mục THÀNH PHẨM QUẢNG CÁO<input id="suF4"></label>
        <label class="f">Thư mục ẢNH YÊU CẦU SỬA<input id="suF7"></label>
      </div>
      <p class="note" id="suDone" hidden style="margin:8px 0 0"></p>
    </fieldset>
    <p class="note" id="suMsg" role="status" style="margin:0"></p>
  </form>
  <div class="dlg-f"><span></span><div class="row"><button class="btn" id="suCancel" type="button">Đóng</button><button class="btn primary" id="suSave" type="button">Lưu cài đặt</button></div></div>
</dialog>

<div class="toast" id="toast" role="status"></div>''')

# ---- JS: cấu hình, dữ liệu riêng, tạo hệ thống, đổi tên thương hiệu
rep('/* ---------- state ---------- */', r'''/* ---------- cấu hình riêng từng người (SPA MARKETING) ---------- */
let CFG=null,BRAND="Thương hiệu",CITY="";
const idOf=x=>{x=String(x||"").trim();const m=x.match(/\/d\/([\w-]{20,})/)||x.match(/folders\/([\w-]{20,})/)||x.match(/[?&]id=([\w-]{20,})/)||x.match(/^([\w-]{20,})$/);return m?m[1]:""};
function applyCfg(c){CFG=c||{};BRAND=CFG.brand||"Thương hiệu";CITY=CFG.city||"";
  if(CFG.pages&&CFG.pages.length)PAGES=CFG.pages;if(CFG.times&&CFG.times.length)TIMES=CFG.times;
  if(CFG.rules)RULES=CFG.rules;if(CFG.cap)CAPTION_STYLE=CFG.cap;
  SHEET_ID=CFG.sheet||"";AD_ACC=CFG.ad||"";const f=CFG.fold||{};FIX_IMG_FOLDER=f.fix||"";
  FOLD={"p-nguon":f.tl||"","p-tp":f.tp||"","q-nguon":f.tq||"","q-tp":f.tpq||"","q-spy":f.spy||""};
  QC_SUB=[["SPA",f.spa||"","Spa tự quay"],["SPY",f.spy||"","Sưu tầm (đã xin phép) – bỏ chữ, giọng gốc, làm lại thành của bạn"]].filter(x=>x[1]);
  if(CFG.logo){LOGO_LIGHT=LOGO_DARK=CFG.logo;try{logos.light.src=logos.dark.src=CFG.logo}catch(e){}}
  $("#brandName").textContent=BRAND;$("#brandSub").textContent=(CITY?CITY+" · ":"")+"SPA MARKETING";document.title=BRAND+" – SPA MARKETING";
  document.querySelectorAll("[data-fold]").forEach(a=>{const id=FOLD[a.dataset.fold];a.href=id?"https://drive.google.com/drive/folders/"+id:"#";a.hidden=!id});
  renderLinks();brandify(document.body)}
function renderLinks(){const box=$("#linksBox");if(!box)return;const f=(CFG&&CFG.fold)||{};
  const L=(id,t,d,sheet)=>id?`<a class="flink" href="https://${sheet?"docs.google.com/spreadsheets/d/"+id+"/edit":"drive.google.com/drive/folders/"+id}" target="_blank" rel="noopener"><b>${t}</b>${d?`<small>${d}</small>`:""}</a>`:"";
  box.innerHTML=`<div class="panel"><h3>Drive – tư liệu &amp; thành phẩm</h3><div class="flinks">${L(f.root,"📁 Thư mục gốc","Toàn bộ dữ liệu")}${L(f.tl,"📥 TƯ LIỆU ĐĂNG BÀI","Thả tư liệu page theo ngày dd-mm-yyyy")}${L(f.tq,"📥 TƯ LIỆU QUẢNG CÁO","SPA / SPY")}${L(f.tp,"✅ THÀNH PHẨM","Bài page chờ duyệt")}${L(f.tpq,"🎬 THÀNH PHẨM QUẢNG CÁO","Video/ảnh quảng cáo")}${L(f.fix,"🖼 ẢNH YÊU CẦU SỬA","Ảnh dán khi yêu cầu sửa")}</div></div>
  <div class="panel"><h3>Bảng tính &amp; công cụ</h3><div class="flinks">${L(SHEET_ID,"📊 Google Sheet DUYỆT BÀI","Tab BAI-DANG, QUANG-CAO, HOI-SEP",1)}<a class="flink" href="https://claude.ai/code/routines" target="_blank" rel="noopener"><b>⚙️ Nhân viên đám mây (routines)</b><small>Lịch chạy tự động</small></a><a class="flink" href="https://business.facebook.com/latest/home" target="_blank" rel="noopener"><b>📣 Meta Business Suite</b></a><a class="flink" href="https://adsmanager.facebook.com/adsmanager/manage/campaigns${AD_ACC?"?act="+AD_ACC:""}" target="_blank" rel="noopener"><b>📈 Ads Manager</b></a></div></div>`}
/* chữ mẫu cũ trong giao diện -> tên thương hiệu của người dùng */
function brandify(root){if(!root||/merah/i.test(BRAND))return;const w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);let n;const fix=[];
  while(n=w.nextNode())if(/MERAH|Merah|Makati/.test(n.nodeValue))fix.push(n);
  for(const t of fix)t.nodeValue=t.nodeValue.replace(/MERAH BEAUTY/g,BRAND.toUpperCase()).replace(/MERAH|Merah/g,BRAND).replace(/Makati( City)?/g,CITY||"")}
let brandObs=null;function watchBrand(){if(brandObs||/merah/i.test(BRAND))return;let q=false;brandObs=new MutationObserver(()=>{if(q)return;q=true;requestAnimationFrame(()=>{q=false;brandify(document.body)})});brandObs.observe(document.body,{childList:true,subtree:true})}
async function mkFolder(title,parentId){const f=await callT(DRIVE,"create_file",{title,contentMimeType:"application/vnd.google-apps.folder",...(parentId?{parentId}:{})});if(!f||!f.id)throw new Error("Không tạo được thư mục "+title);return f.id}
const SHEET_TABS=[["BAI-DANG",["Mã bài","Ngày","Giờ","Giờ VN","Dạng","Chủ đề","Link ảnh/video","Caption","TRẠNG THÁI","Ghi chú của bạn (cần sửa gì)","Nhật ký hệ thống","LỊCH SỬ SỬA (mỗi dòng 1 lần: giờ – ai – nội dung – bản)"]],
  ["HOI-SEP",["Mã","Ngày","Phòng","Câu hỏi","Sếp trả lời","Ghi chú hệ thống","Lựa chọn (JSON cho app hiện ô tích)"]],
  ["QC-DANH-GIA",["ID (chiến dịch hoặc quảng cáo)","Tên","Cấp","Nhãn (Tốt/Khá/Tệ hoặc Win/Không win)","Ghi chú nhà quảng cáo","Cập nhật lúc"]],
  ["QUANG-CAO",["Mã","Ngày thành phẩm (dd/mm/yyyy)","Nguồn (SPA/SPY)","Tên thành phẩm (VD1, ANH1…)","Dạng (Ảnh/Video)","Link Drive","Phong cách","PAGE ĐĂNG (sếp chọn)","TRẠNG THÁI","Ghi chú sếp","Nhật ký hệ thống","ID POST (hệ thống ghi sau khi đăng)","CAPTION (Content QC viết, hiện trong bản xem trước)","LỊCH SỬ SỬA (mỗi dòng 1 lần: giờ – ai – nội dung – bản)"]],
  ["TIEN-DO-TU-LIEU",["Khoá (LOẠI/thư mục)","Loại (PAGE/SPA/SPY)","Thư mục ngày","TRẠNG THÁI (Đã tiếp nhận / Đang xử lý / Xử lý xong / Lỗi)","Ghi chú (làm gì, ra thành phẩm nào)","Cập nhật lúc","Lịch sử (mỗi dòng: giờ – ai – việc)"]]];
SHEET_TABS.push(["DO-LUONG",["Ngày","Khoảng số liệu","Mục","Nhận định","Đề xuất / giao cho","Ưu tiên"]],
  ["SPY-ADS",["Ngày quét","Dịch vụ","Nền tảng","Đối thủ / kênh","Quốc gia","Link bài","Số ngày chạy / lượt xem","Hook / ghi chú","TRẠNG THÁI","ID","Ảnh bìa"]],
  ["SPY-DOI-THU",["{}"]]);
const colL=n=>String.fromCharCode(64+n);
async function ensureTabs(id){if(!id||!mcp||lsGet("fbm_tabs_"+id))return;let ok=true;
  for(const [t,h] of SHEET_TABS.slice(-3)){try{await sheetTool("get_values",{spreadsheetId:id,range:t+"!A1:A1"})}
    catch(e){try{await sheetTool("update_spreadsheet",{spreadsheetId:id,requests:[{addSheet:{properties:{title:t,gridProperties:{frozenRowCount:1}}}}]});
      await sheetTool("update_values",{spreadsheetId:id,range:`${t}!A1:${colL(h.length)}1`,values:[h]})}catch(e2){ok=false}}}
  if(ok)lsSet("fbm_tabs_"+id,"1")}
async function createSystem(brand,say){const root=await mkFolder(brand+" – SPA MARKETING");say("Đã tạo thư mục gốc, đang tạo thư mục con…");
  const tl=await mkFolder("TƯ LIỆU ĐĂNG BÀI",root),tq=await mkFolder("TƯ LIỆU QUẢNG CÁO",root),spa=await mkFolder("SPA",tq),spy=await mkFolder("SPY",tq),
    tp=await mkFolder("THÀNH PHẨM",root),tpq=await mkFolder("THÀNH PHẨM QUẢNG CÁO",root),fix=await mkFolder("ẢNH YÊU CẦU SỬA",root);
  say("Đang tạo Google Sheet DUYỆT BÀI…");
  const sh=await callT(DRIVE,"create_file",{title:brand+" – DUYỆT BÀI",contentMimeType:"application/vnd.google-apps.spreadsheet",parentId:root});if(!sh||!sh.id)throw new Error("Không tạo được Google Sheet");
  await sheetTool("update_spreadsheet",{spreadsheetId:sh.id,requests:[{updateSheetProperties:{properties:{sheetId:0,title:"BAI-DANG",gridProperties:{frozenRowCount:1}},fields:"title,gridProperties.frozenRowCount"}},
    ...SHEET_TABS.slice(1).map(([t])=>({addSheet:{properties:{title:t,gridProperties:{frozenRowCount:1}}}}))]});
  for(const [t,h] of SHEET_TABS)await sheetTool("update_values",{spreadsheetId:sh.id,range:`${t}!A1:${colL(h.length)}1`,values:[h]});
  return {sheet:sh.id,fold:{root,tl,tq,spa,spy,tp,tpq,fix}}}
function shrinkLogo(file){return new Promise((ok,bad)=>{const u=URL.createObjectURL(file),im=new Image();im.onload=()=>{const k=Math.min(1,400/Math.max(im.width,im.height)),c=document.createElement("canvas");c.width=Math.round(im.width*k);c.height=Math.round(im.height*k);c.getContext("2d").drawImage(im,0,0,c.width,c.height);URL.revokeObjectURL(u);ok(c.toDataURL("image/png"))};im.onerror=()=>bad(new Error("Không đọc được logo"));im.src=u})}
function openSetup(first){return new Promise(res=>{const d=$("#setupDlg"),c=CFG||{};
  $("#suTitle").textContent=first?"Chào mừng! Cài đặt lần đầu":"Cài đặt SPA MARKETING";
  $("#suBrand").value=c.brand||"";$("#suCity").value=c.city||"";$("#suPages").value=(c.pages||[]).join("\n");$("#suTimes").value=(c.times||TIMES).join(", ");
  $("#suAd").value=c.ad||"";$("#suRules").value=c.rules||RULES;$("#suCap").value=c.cap||CAPTION_STYLE;$("#suMsg").textContent="";
  const has=!!(c.sheet);document.querySelectorAll('[name=suMode]').forEach(r=>{r.checked=r.value===(has?"old":"new");r.closest("label").hidden=false});
  if(has){const f=c.fold||{};$("#suSheet").value=c.sheet?"https://docs.google.com/spreadsheets/d/"+c.sheet+"/edit":"";[["suF1","tl"],["suF2","tp"],["suF3","tq"],["suF4","tpq"],["suF5","spa"],["suF6","spy"],["suF7","fix"]].forEach(([i,k])=>$("#"+i).value=f[k]?"https://drive.google.com/drive/folders/"+f[k]:"")}
  const syncMode=()=>{$("#suOld").hidden=document.querySelector('[name=suMode]:checked').value!=="old"};syncMode();document.querySelectorAll('[name=suMode]').forEach(r=>r.onchange=syncMode);
  $("#suCancel").hidden=!!first;$("#suCancel").onclick=()=>{d.close();res(null)};d.oncancel=e=>{if(first)e.preventDefault()};d.showModal();
  $("#suSave").onclick=async()=>{const say=t=>$("#suMsg").textContent=t;const brand=$("#suBrand").value.trim(),pages=$("#suPages").value.split(/\r?\n/).map(x=>x.trim()).filter(Boolean);
    if(!brand||!pages.length){say("Cần nhập tên thương hiệu và ít nhất 1 page.");return}
    const n={...c,brand,city:$("#suCity").value.trim(),pages,times:$("#suTimes").value.split(/[,;\s]+/).map(x=>x.trim()).filter(x=>/^\d{1,2}:\d{2}$/.test(x)).map(x=>x.padStart(5,"0")),
      ad:$("#suAd").value.replace(/\D/g,""),rules:$("#suRules").value.trim(),cap:$("#suCap").value.trim()};
    if(!n.times.length)n.times=["07:00","11:00","19:00"];
    $("#suSave").disabled=true;
    try{const lf=$("#suLogo").files[0];if(lf)n.logo=await shrinkLogo(lf);
      if(document.querySelector('[name=suMode]:checked').value==="new"){if(!mcp)throw new Error("App chưa được phép dùng Google Drive / Sheets – bấm cho phép khi trang hỏi rồi thử lại.");
        if(c.sheet&&!await confirmBox("Bạn đã có hệ thống. Tạo thêm bộ thư mục + Sheet MỚI?"))throw new Error("Đã huỷ");
        say("Đang tạo thư mục trên Google Drive của bạn…");Object.assign(n,await createSystem(brand,say))}
      else{const fold={tl:idOf($("#suF1").value),tp:idOf($("#suF2").value),tq:idOf($("#suF3").value),tpq:idOf($("#suF4").value),spa:idOf($("#suF5").value),spy:idOf($("#suF6").value),fix:idOf($("#suF7").value),root:(c.fold||{}).root||""};
        n.sheet=idOf($("#suSheet").value);n.fold=fold;if(!n.sheet){throw new Error("Chưa dán link Google Sheet hợp lệ.")}}
      await db.doc("cfg/main").set(n);applyCfg(n);ensureTabs(n.sheet);say("Đã lưu.");d.close();toast("Đã lưu cài đặt");res(n)}
    catch(e){say(errTxt?errTxt(e):String(e&&e.message||e))}finally{$("#suSave").disabled=false}}})}

/* ---------- state ---------- */''')

# ---- khởi động: dữ liệu riêng từng người + bắt buộc cài đặt lần đầu
rep('''  db=d;assets=a;sample=s;downloads=dl;''', '''  assets=a;sample=s;downloads=dl;
  const usr=await window.claude.use("user").catch(()=>null);let uid=null;try{uid=usr&&await usr.id()}catch(e){}
  if(d&&uid){const P="data/users/"+uid+"/app/";db={collection:n=>d.collection(P+n),doc:p=>d.doc(P+p)}}else db=null;''')
rep('''  const ok=()=>{clearTimeout(timer);$("#connDot").className="dot on";$("#connText").textContent="Đã lưu tự động";banner("")};''',
    '''  const ok=()=>{clearTimeout(timer);$("#connDot").className="dot on";$("#connText").textContent="Đã lưu tự động";banner("")};
  mcp=await window.claude.use("mcp").catch(()=>null);
  let cfg=null;try{const g=await db.doc("cfg/main").get();cfg=g&&g.exists?(typeof g.data==="function"?g.data():g.data):null}catch(e){}
  if(!cfg||!cfg.brand){clearTimeout(timer);cfg=await openSetup(true)}else applyCfg(cfg);watchBrand();ensureTabs(SHEET_ID);''')
rep('''  mcp=await window.claude.use("mcp").catch(()=>null);
  if(mcp){lazyLoad(curView)''', '''  if(mcp){lazyLoad(curView)''')
rep('''  setTimeout(sheetPull,2500);''', '''  if(!SHEET_ID){sheetMsg("Chưa có Google Sheet – mở ⚙ Cài đặt.",true);return}
  setTimeout(sheetPull,2500);''')
s = s.replace("</script>\n</body>", '''document.addEventListener("click",e=>{if(e.target.closest("#openSetup"))openSetup(false)});
</script>
</body>''', 1)
# ---- GĐ4 (12/11/2026): SPY + Đo lường cho người dùng ngoài MERAH
sub(r'const PG_NAME=new Map\(\[.*?\]\]\);', 'const PG_NAME=new Map();')
rep('"pg:{{ID_FACEBOOK}}"', '"all"', cnt=9)
rep('name:"MR 1 - HOÀNG"', 'name:"Tài khoản quảng cáo chính"', cnt=9)
sub(r'href="https://drive\.google\.com/drive/folders/1GtCIo5[\w-]+"', 'data-fold="q-spy" href="#"')
# bấm SPY: bản chia sẻ không có máy tải hộ -> chỉ lưu bài vào danh sách SPY của người dùng
rep('const ping=mcp&&url?spyPing(key,who,url):Promise.resolve("off");', 'const ping=Promise.resolve("off");')
rep('"Đã ghi vào danh sách chờ tải")}', '"Đã lưu vào danh sách SPY (tab SPY-ADS) – bấm link bài để xem video")}')
rep('`Muốn tải nội dung này không?', '`Lưu bài này vào danh sách SPY để làm lại?')
sub(r'Đồng ý: video sẽ được tải về thư mục SPY ngày hôm nay để EDIT video làm quảng cáo\. Việc tải do máy tính của sếp làm khi máy đang bật\.',
    'Đồng ý: bài được ghi vào tab SPY-ADS trên Google Sheet của bạn (kèm link) để đội làm quảng cáo dựng lại theo cách của mình.')
rep('"⏳ Chờ máy tải – huỷ"', '"✓ Đã lưu – bỏ chọn"')
rep('Chờ máy tải', 'Dùng làm ý tưởng', cnt=99)
# khung Gửi link SPY: bản chia sẻ không có máy tải hộ -> chỉ lưu link
rep('(ok?(sent===ok?" · máy đang tải ngay":" · máy sẽ tải khi phiên Claude trên máy sẵn sàng"):"")', '(ok?" · đã lưu vào tab SPY-ADS để đội EDIT làm lại":"")')
rep('Dán link video → máy tự tải về Drive SPY/ngày gửi → EDIT clone + viết content → chờ Sếp duyệt.', 'Dán link video → lưu vào danh sách SPY (tab SPY-ADS) → đội EDIT làm lại → chờ duyệt.')
rep('video được tải về thư mục SPY để EDIT video làm quảng cáo', 'bài được lưu vào danh sách SPY để làm lại thành quảng cáo của bạn', cnt=9)
io.open(OUT + "/src.html", "w", encoding="utf-8", newline="\n").write(s)
io.open(OUT + "/index.html", "w", encoding="utf-8", newline="\n").write(s)
io.open(CHK, "w", encoding="utf-8").write("\n".join(re.findall(r"<script>(.*?)</script>", s, re.S)))
left = sorted(set(re.findall(r"1[\w-]{30,40}", s)))
print("ok; ID con sot:", left)
