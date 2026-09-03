from pathlib import Path

path = Path('admin.html')
text = path.read_text(encoding='utf-8')
marker = '/* WENIK FLEXIBLE WIN DRAW */'
if marker in text:
    print('Flexible WIN draw already applied')
    raise SystemExit(0)

old = "async function loadWins(){try{const list=await rpc('admin_campaign_list');$('winList').innerHTML=(list||[]).map(c=>'<div class=\"card\"><div class=\"row\"><div><b>'+esc(c.title)+'</b><div class=\"muted\">'+esc(c.code)+'</div></div><span class=\"pill\">'+esc(c.status)+'</span></div><div class=\"muted\">Eligible '+c.eligible_entries+' · Prize slots '+c.prize_slots+' · Winners '+c.winner_count+'</div>'+((c.entries_locked_at&&c.prize_slots>0&&!c.draw_finalized_at&&(c.status==='closed'||c.status==='drawn'))?'<button class=\"btn\" onclick=\"drawWin(\\''+c.id+'\\')\">RUN FINAL DRAW</button>':'')+'</div>').join('')||'<div class=\"card muted\">No WIN campaigns.</div>'}catch(e){$('winList').innerHTML='<div class=\"card error\">'+esc(e.message)+'</div>'}}\nwindow.drawWin=async id=>{if(!confirm('Run the final draw now? This finalizes winners.'))return;try{const rows=await rpc('admin_draw_campaign_winners',{p_campaign_id:id});alert('Draw complete: '+(rows?.length||0)+' winners.');await loadWins()}catch(e){alert(e.message)}};$('refreshWins').onclick=loadWins;"

new = "/* WENIK FLEXIBLE WIN DRAW */\nasync function loadWins(){try{const list=await rpc('admin_campaign_list');$('winList').innerHTML=(list||[]).map(c=>{const remaining=Math.max(Number(c.prize_slots||0)-Number(c.winner_count||0),0);const canDraw=c.entries_locked_at&&remaining>0&&!c.draw_finalized_at&&c.status==='closed';return '<div class=\"card\"><div class=\"row\"><div><b>'+esc(c.title)+'</b><div class=\"muted\">'+esc(c.code)+'</div></div><span class=\"pill\">'+esc(c.status)+'</span></div><div class=\"muted\">Eligible '+c.eligible_entries+' · Prize slots '+c.prize_slots+' · Winners '+c.winner_count+' · Remaining '+remaining+'</div>'+(canDraw?'<div class=\"two\"><input id=\"drawCount-'+c.id+'\" class=\"field\" type=\"number\" min=\"1\" max=\"'+remaining+'\" value=\"'+Math.min(4,remaining)+'\" placeholder=\"Number of winners\"><button class=\"btn\" onclick=\"drawWin(\\''+c.id+'\\','+remaining+','+Number(c.eligible_entries||0)+')\">RUN DRAW</button></div>':'')+'</div>'}).join('')||'<div class=\"card muted\">No WIN campaigns.</div>'}catch(e){$('winList').innerHTML='<div class=\"card error\">'+esc(e.message)+'</div>'}}\nwindow.drawWin=async(id,remaining,eligible)=>{const el=$('drawCount-'+id),count=Number(el?.value||0);if(!Number.isInteger(count)||count<1){alert('Enter a valid number of winners.');return}if(count>remaining){alert('Only '+remaining+' prize slots remain.');return}if(count>eligible){alert('Only '+eligible+' eligible customers are available.');return}if(!confirm('Run draw for '+count+' winner'+(count===1?'':'s')+' now?'))return;try{const rows=await rpc('admin_draw_campaign_winners_v2',{p_campaign_id:id,p_winner_count:count});alert('Draw complete: '+(rows?.length||0)+' winners.');await loadWins()}catch(e){alert(e.message)}};$('refreshWins').onclick=loadWins;"

if old not in text:
    raise SystemExit('Expected WIN block not found; refusing to modify admin.html')

text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
print('Applied flexible WIN draw UI safely')
