import { Camera, UploadCloud, Settings as Cog } from 'lucide-react'

export default function Navbar({onNav, route}:{onNav:(r:any)=>void, route:string}){
  const Item = ({label, icon, r}:{label:string, icon:any, r:string}) => (
    <button onClick={()=>onNav(r)} className={`flex items-center gap-2 px-4 py-2 rounded-2xl hover:bg-brand-800 transition ${route===r?'bg-brand-700':''}`}>
      {icon}
      <span className="font-semibold">{label}</span>
    </button>
  )
  return (
    <header className="header">
      <div className="container py-3 flex items-center gap-3">
        <div className="text-xl font-bold tracking-tight flex items-center gap-2">
          <Camera className="w-6 h-6"/> BlueAI Clips
        </div>
        <div className="flex-1"/>
        <nav className="flex gap-2">
          <Item label="Dashboard" icon={<Camera className="w-4 h-4"/>} r="dashboard"/>
          <Item label="Upload" icon={<UploadCloud className="w-4 h-4"/>} r="upload"/>
          <Item label="Settings" icon={<Cog className="w-4 h-4"/>} r="settings"/>
        </nav>
      </div>
    </header>
  )
}
