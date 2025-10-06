export default function Settings(){
  return (
    <div className='surface space-y-2'>
      <h2 className='text-lg font-bold'>Settings</h2>
      <p className='muted'>This frontend expects your backend to expose /api endpoints and uses your Render URL by default.</p>
      <p className='muted'>To target another backend, set <code>VITE_API_BASE</code> in Render → Environment.</p>
    </div>
  )
}
