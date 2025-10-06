import axios from 'axios'

const BASE = import.meta.env.VITE_API_BASE || ''

export async function apiUpload(file: File){
  const fd = new FormData()
  fd.append('file', file)
  const r = await axios.post(`${BASE}/api/upload`, fd, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  return r.data
}

export async function apiProcess(body: any){
  const r = await axios.post(`${BASE}/api/process`, body)
  return r.data
}

export async function apiStatus(job_id: string){
  const r = await axios.get(`${BASE}/api/status/${job_id}`)
  return r.data
}

export async function apiClips(){
  const r = await axios.get(`${BASE}/api/clips`)
  return r.data
}
