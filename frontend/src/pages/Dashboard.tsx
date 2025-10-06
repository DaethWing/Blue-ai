import { useEffect, useState } from 'react'
import { apiClips } from '../lib/api'

export default function Dashboard(){
  const [clips, setClips] = useState<any[]>([])
  useEffect(()=>{ (async()=> setClips(await apiClips()))() },[])
  return (
    <div className="grid-clips">
      {clips.map((c)=> (
        <div key={c.url} className="surface">
          <video src={c.url} controls className="w-full rounded-xl"/>
          <div className="mt-2 text-sm font-semibold">{c.meta?.title || 'Clip'}</div>
          <div className="text-xs muted">{c.meta?.ratio} • {Math.round(c.meta?.duration||0)}s</div>
          <div className="mt-2">
            {(c.meta?.hashtags||[]).map((h:string, i:number)=> <span key={i} className="pill">#{h}</span>)}
          </div>
        </div>
      ))}
      {clips.length===0 && <div className="muted">No clips yet. Go to Upload and generate some!</div>}
    </div>
  )
}
