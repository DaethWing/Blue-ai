import { useState } from 'react'
import { apiUpload, apiProcess, apiStatus } from '../lib/api'

export default function Upload(){
  const [file, setFile] = useState<File|null>(null)
  const [job, setJob] = useState<string|undefined>()
  const [status, setStatus] = useState<any>(null)

  const onGo = async () => {
    if(!file) return
    const up = await apiUpload(file)
    const pr = await apiProcess({ file_id: up.file_id, target_ratios:['9:16','1:1','16:9'], max_clips:4, clip_min_seconds:20, clip_max_seconds:60, burn_captions:true, face_aware:true, brand_text:'BlueAI' })
    setJob(pr.job_id)
    const poll = async () => {
      if(!pr.job_id) return
      const st = await apiStatus(pr.job_id); setStatus(st)
      if(st.status==='done' || st.status==='error') return
      setTimeout(poll, 2000)
    }
    poll()
  }

  return (
    <div className="space-y-4">
      <div className="surface">
        <div className="font-semibold mb-2">Upload a video</div>
        <input type="file" accept="video/*" onChange={e=>setFile(e.target.files?.[0]||null)} className="block w-full text-sm"/>
        <button onClick={onGo} className="btn mt-3">Generate Clips</button>
        <div className="muted mt-2">AI will transcribe, pick highlights, add captions & a BlueAI watermark.</div>
      </div>
      {job && (
        <div className="surface">
          <div className="text-sm">Job: {job}</div>
          <div className="mt-1">Status: <span className="font-semibold">{status?.status||'starting'}</span></div>
          <div className="w-full h-2 bg-white/10 rounded mt-2 overflow-hidden">
            <div className="h-2 bg-white/80" style={{width: `${Math.round((status?.progress||0)*100)}%`}} />
          </div>
          <div className="text-xs mt-1 muted">{status?.message}</div>
        </div>
      )}
    </div>
  )
}
