import Navbar from './components/Navbar';
import MapView from './components/MapView';
import Sidebar from './components/Sidebar';

export default function App() {
  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-slate-900 text-white">
      <Navbar />
      <div className="flex flex-1 relative overflow-hidden">
        <Sidebar />
        <MapView />
      </div>
    </div>
  );
}
