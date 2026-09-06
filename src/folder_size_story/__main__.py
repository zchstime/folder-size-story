import argparse
from collections import defaultdict
from pathlib import Path

def scan(root):
 root=Path(root); dirs=defaultdict(int); exts=defaultdict(int); files=[]; skipped=0
 for p in root.rglob("*"):
  if p.is_symlink(): skipped+=1; continue
  if not p.is_file(): continue
  try: size=p.stat().st_size
  except OSError: skipped+=1; continue
  files.append((size,p)); exts[p.suffix.lower() or "[no extension]"]+=size
  parent=p.parent
  while parent==root or root in parent.parents: dirs[str(parent.relative_to(root)) or "."]+=size; parent=parent.parent
 return {"total":sum(x[0] for x in files),"files":sorted(files,reverse=True),"dirs":sorted(dirs.items(),key=lambda x:-x[1]),"extensions":sorted(exts.items(),key=lambda x:-x[1]),"skipped":skipped}
def human(n):
 for unit in ("B","KB","MB","GB","TB"):
  if n<1024 or unit=="TB": return f"{n:.1f} {unit}"
  n/=1024
def markdown(x,top):
 out=["# Folder Size Story",f"\nTotal: **{human(x['total'])}** · skipped symlinks/errors: {x['skipped']}\n","## Largest files"]+[f"- {human(s)} `{p}`" for s,p in x["files"][:top]]+["","## Largest folders"]+[f"- {human(s)} `{p}`" for p,s in x["dirs"][:top]]+["","## File types"]+[f"- {human(s)} `{e}`" for e,s in x["extensions"][:top]]
 return "\n".join(out)+"\n"
def main(argv=None):
 p=argparse.ArgumentParser(description="Explain disk usage by file, folder, and extension"); p.add_argument("root"); p.add_argument("--top",type=int,default=10); p.add_argument("--output")
 a=p.parse_args(argv); text=markdown(scan(a.root),a.top); Path(a.output).write_text(text) if a.output else print(text)
if __name__=="__main__": main()
