import { useState } from 'react'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Upload from './pages/Upload'
import Settings from './pages/Settings'

export default function App(){
  const [route, setRoute] = useState<'dashboard'|'upload'|'settings'>('dashboard')
  return (
    <div className="min-h-screen bg-brand-900 text-white">
      <Navbar onNav={setRoute} route={route} />
      <main className="container py-6">
        {route==='dashboard' && <Dashboard/>}
        {route==='upload' && <Upload/>}
        {route==='settings' && <Settings/>}
      </main>
    </div>
  )
}
