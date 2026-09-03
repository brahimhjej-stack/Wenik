from pathlib import Path
p=Path('index.html')
s=p.read_text()
old="BHI2mvri3pacvHazW4kV-SXuKRMZsfdpNACT225u6jJyL2_oHB4Y_zExfjRAOFHqqkW5c8UnmGfpPlhCJh0H0V0"
new="BH1kiwu9TR9zO7U8tzXJKPdmVzMTtXKcTM8EVUGZsz7PBgJFK6nIjp9wCkqWoAOZDymWCmxkELxC8jspxxMsExg"
if s.count(old)!=1: raise SystemExit('GUARD FAILED: old public key not found exactly once')
s=s.replace(old,new,1)
if s.count(new)!=1: raise SystemExit('GUARD FAILED: new public key count')
p.write_text(s)
