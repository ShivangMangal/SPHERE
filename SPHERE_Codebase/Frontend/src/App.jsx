import React, { useState } from 'react';
import { LogIn, LogOut, Upload, FileText, CheckCircle2, Loader2, Sparkles, AlertCircle, BarChart3, ShieldCheck, Leaf, ChevronDown } from 'lucide-react';
import SPHERELogo from './components/SPHERELogo';
import mockData from './utils/mockData.json';

export default function App() {
  const [view, setView] = useState('home'); 
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [visibleCount, setVisibleCount] = useState(50);
  const [categoryFilter, setCategoryFilter] = useState('All');

  const handleUpload = () => {
    setIsUploading(true);
    let progress = 0;
    const interval = setInterval(() => {
      progress += 20;
      setUploadProgress(progress);
      if (progress >= 100) {
        clearInterval(interval);
        setTimeout(() => {
          setIsUploading(false);
          setView('results');
        }, 500);
      }
    }, 200);
  };

  const allReqs = mockData.requirement_groups.flatMap(g => g.requirements);
  const highPriority = allReqs.filter(r => r.priority === 'HIGH').length;
  const uniqueCategories = ['All', ...new Set(allReqs.map(r => r.requirement_type).filter(Boolean))];
  
  let filteredGroups = mockData.requirement_groups;
  if (categoryFilter !== 'All') {
    filteredGroups = filteredGroups.map(g => ({
      ...g,
      requirements: g.requirements.filter(r => r.requirement_type === categoryFilter)
    })).filter(g => g.requirements.length > 0);
  }
  
  const displayGroups = filteredGroups.slice(0, visibleCount);

  return (
    <div className="w-full min-h-screen pb-20" style={{ background: 'var(--bg-primary)', color: 'var(--text-primary)' }}>
      {/* Navbar */}
      <nav className="fixed top-0 left-0 right-0 z-50 h-[72px] px-6 border-b" style={{ background: 'var(--bg-card)', borderColor: 'var(--border-light)' }}>
        <div className="h-full max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setView('home')}>
            <SPHERELogo />
            <span className="text-xl font-bold tracking-tight">SPHERE</span>
          </div>
          <div className="flex items-center gap-4">
            <button onClick={() => setView('home')} className="text-sm font-medium hover:text-black">Home</button>
            <button onClick={() => setView('upload')} className="text-sm font-medium hover:text-black">Upload Dataset</button>
            <button className="btn-dark flex items-center gap-2 px-4 py-2 rounded-lg text-sm text-white" style={{ background: '#1a1a1a' }}>
              <LogIn size={16} /> City Planner
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="pt-[72px] w-full max-w-6xl mx-auto px-6 py-6 flex flex-col">
        {view === 'home' && (
          <div className="text-center py-20 mt-10">
            <h1 className="text-5xl font-extrabold tracking-tight mb-6" style={{ color: 'var(--text-primary)' }}>
              AI Requirements Engineering for <span style={{ color: '#ec4899' }}>Urban Planning</span>
            </h1>
            <p className="text-lg mb-10 max-w-2xl mx-auto" style={{ color: 'var(--text-secondary)' }}>
              Upload your Civil Engineering documents, public surveys, and city council mandates. SPHERE instantly classifies, prioritizes, and resolves requirements mathematically.
            </p>
            <button onClick={() => setView('upload')} className="px-8 py-4 rounded-full text-white font-semibold text-lg flex items-center gap-2 mx-auto shadow-lg" style={{ background: 'linear-gradient(135deg, #c8b4ff, #f5c8d8)' }}>
              <Upload size={20} /> Upload Dataset
            </button>
          </div>
        )}

        {view === 'upload' && (
          <div className="max-w-2xl mx-auto mt-20 bg-white p-10 rounded-3xl shadow-xl text-center" style={{ border: '1px solid var(--border-light)' }}>
            <div className="w-20 h-20 mx-auto rounded-2xl flex items-center justify-center mb-6 shadow-sm" style={{ background: 'linear-gradient(135deg, #c8b4ff, #f5c8d8)' }}>
              <Upload size={32} className="text-white" />
            </div>
            <h2 className="text-2xl font-bold mb-2">Upload Civil Requirements</h2>
            <p className="text-sm mb-6" style={{ color: 'var(--text-secondary)' }}>Select a PDF or CSV dataset to process</p>
            
            {!isUploading && (
              <div className="mb-8">
                <input 
                  type="file" 
                  id="file-upload" 
                  className="hidden" 
                  accept=".csv,.pdf"
                  onChange={(e) => {
                    const file = e.target.files[0];
                    if (file) {
                      document.getElementById('file-name').innerText = 'Selected: ' + file.name;
                    }
                  }}
                />
                <label htmlFor="file-upload" className="cursor-pointer px-6 py-3 rounded-lg border-2 border-dashed border-gray-300 hover:border-pink-400 hover:bg-pink-50 transition-all inline-block w-full max-w-sm">
                  <div className="flex flex-col items-center gap-2">
                    <FileText size={24} className="text-gray-400" />
                    <span id="file-name" className="text-sm font-medium text-gray-600">Click to browse files</span>
                  </div>
                </label>
              </div>
            )}
            
            {isUploading ? (
              <div className="space-y-4">
                <Loader2 size={32} className="animate-spin mx-auto text-pink-400" />
                <p className="font-medium text-pink-500">Processing with SPHERE AI...</p>
                <div className="w-full h-3 rounded-full overflow-hidden bg-gray-100">
                  <div className="h-full bg-pink-400 transition-all duration-300" style={{ width: `${uploadProgress}%` }}></div>
                </div>
              </div>
            ) : (
              <button onClick={handleUpload} className="px-8 py-4 rounded-xl text-white font-semibold flex items-center gap-2 mx-auto" style={{ background: '#1a1a1a' }}>
                <Sparkles size={20} /> Process with AI
              </button>
            )}
          </div>
        )}

        {view === 'results' && (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="flex items-center justify-between mb-8">
              <div>
                <h2 className="text-3xl font-bold">Civil Requirements Dashboard</h2>
                <p style={{ color: 'var(--text-secondary)' }}>Analysis complete. Extracted {allReqs.length} total requirements.</p>
              </div>
              <div className="flex flex-col gap-3 items-end">
                <div className="flex gap-4">
                  <div className="px-4 py-2 rounded-lg font-bold text-emerald-600 bg-emerald-50 border border-emerald-100 flex items-center gap-2">
                    <ShieldCheck size={20} /> {highPriority} High Priority
                  </div>
                  <div className="px-4 py-2 rounded-lg font-bold text-pink-600 bg-pink-50 border border-pink-100 flex items-center gap-2">
                    <Leaf size={20} /> {allReqs.filter(r => r.requirement_type === 'Environmental').length} Environmental
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-semibold text-gray-500">Filter Category:</span>
                  <select 
                    value={categoryFilter}
                    onChange={(e) => { setCategoryFilter(e.target.value); setVisibleCount(50); }}
                    className="px-3 py-1.5 rounded-lg border border-gray-200 bg-white text-sm font-medium shadow-sm outline-none focus:ring-2 focus:ring-pink-200 cursor-pointer"
                  >
                    {uniqueCategories.map(cat => (
                      <option key={cat} value={cat}>{cat}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 gap-6 mb-8">
              {displayGroups.map((group, idx) => (
                <div key={idx} className="bg-white p-6 rounded-2xl shadow-sm" style={{ border: '1px solid var(--border-light)' }}>
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="text-xl font-bold">{group.group_name}</h3>
                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${group.priority === 'HIGH' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-700'}`}>
                      {group.priority} Priority
                    </span>
                  </div>
                  
                  {group.requirements.map((req, rIdx) => (
                    <div key={rIdx} className="space-y-3">
                      <p className="text-lg leading-relaxed">{req.sentence}</p>
                      <div className="flex flex-wrap gap-2 pt-2">
                        <span className="px-3 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-100">
                          {req.requirement_type}
                        </span>
                        <span className="px-3 py-1 rounded-full text-xs font-medium bg-purple-50 text-purple-700 border border-purple-100">
                          Score: {req.priority_score}
                        </span>
                        {req.priority_reasons.map((reason, rIdx2) => (
                          <span key={rIdx2} className="px-3 py-1 rounded-full text-xs font-medium bg-gray-50 text-gray-600 border border-gray-200">
                            {reason}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              ))}
            </div>

            {visibleCount < mockData.requirement_groups.length && (
              <button 
                onClick={() => setVisibleCount(prev => prev + 50)} 
                className="mx-auto flex items-center gap-2 px-6 py-3 rounded-full font-bold text-gray-700 bg-gray-100 hover:bg-gray-200 transition-colors"
              >
                Load More Results <ChevronDown size={20} />
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
