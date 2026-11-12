import io, re, sys
p = sys.argv[1]; s = io.open(p, encoding="utf-8").read(); n = [0]
def f(m):
    n[0] += 1; return f'<{m.group(1)} id="md{n[0]}" '
s = re.sub(r'<(video|audio) (?!id=)', f, s)
io.open(p, "w", encoding="utf-8", newline="\n").write(s); print("ids", n[0])
