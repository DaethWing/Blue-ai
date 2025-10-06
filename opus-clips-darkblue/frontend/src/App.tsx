import { useState } from 'react'
import Dashboard from './pages/Dashboard'
import Upload from './pages/Upload'
import Settings from './pages/Settings'
import Navbar from './components/Navbar'

export default function App(){
  const [route, setRoute] = useState<'dashboard'|'upload'|'settings'>('dashboard')
  return (
    <div className="min-h-screen bg-navy-900 text-white">
      <Navbar onNav={setRoute} route={route} />
      <main className="max-w-6xl mx-auto p-6">
        {route==='dashboard' && <Dashboard/>}
        {route==='upload' && <Upload/>}
        {route==='settings' && <Settings/>}
      </main>
    </div>
  )
}
