from pathlib import Path

p=Path('partner.html')
s=p.read_text()
old="""<input id=\"mediaFile-'+i+'\" class=\"field\" type=\"file\" accept=\"image/*\"><button class=\"btn secondary\" data-upload-slot=\"'+i+'\">UPLOAD / REPLACE IMAGE '+i+'</button></div>'}).join('');document.querySelectorAll('[data-upload-slot]').forEach(b=>b.onclick=()=>uploadMedia(Number(b.dataset.uploadSlot)))}catch(e){$('mediaMsg').className='error';$('mediaMsg').textContent=e.message}}"""
new="""<input id=\"mediaFile-'+i+'\" type=\"file\" accept=\"image/*\" style=\"display:none\"><button class=\"btn secondary\" data-upload-slot=\"'+i+'\">UPLOAD / REPLACE IMAGE '+i+'</button></div>'}).join('');document.querySelectorAll('[data-upload-slot]').forEach(b=>{const slot=Number(b.dataset.uploadSlot),input=$('mediaFile-'+slot);b.onclick=()=>input.click();input.onchange=()=>{if(input.files?.[0])uploadMedia(slot)}})}catch(e){$('mediaMsg').className='error';$('mediaMsg').textContent=e.message}}"""
if old not in s:
    raise SystemExit('MEDIA UPLOAD BLOCK NOT FOUND')
s=s.replace(old,new,1)
p.write_text(s)
print('Partner mobile upload picker patch applied')
