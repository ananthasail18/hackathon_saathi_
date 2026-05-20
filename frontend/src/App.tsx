import { useState } from 'react';
import './index.css';

// Mock data for initial UI presentation
const MOCK_HACKATHONS = [
  {
    id: 1,
    title: "AI Innovators Challenge",
    platform: "Devfolio",
    matchScore: 98,
    date: "Oct 15 - Oct 17",
    prize: "$10,000",
    tags: ["AI", "GenAI", "Python"],
    status: "Recommended",
    url: "https://devpost.com/hackathons", // Using Devpost for demo
    start_date: "2026-10-15",
    end_date: "2026-10-17"
  },
  {
    id: 2,
    title: "Global FinTech Hack",
    platform: "Devpost",
    matchScore: 85,
    date: "Nov 01 - Nov 05",
    prize: "$25,000",
    tags: ["Web3", "Finance", "React"],
    status: "Recommended",
    url: "https://devpost.com/hackathons",
    start_date: "2026-11-01",
    end_date: "2026-11-05"
  }
];

function App() {
  const [activeTab, setActiveTab] = useState('discover');
  const [hackathons, setHackathons] = useState(MOCK_HACKATHONS);
  const [loadingAction, setLoadingAction] = useState<number | null>(null);

  const mockProfile = {
    name: "Anant",
    email: "anant@example.com",
    github: "https://github.com/anant",
    bio: "I love building autonomous AI agents."
  };

  const handleApply = async (hackathonId: number, url: string) => {
    setLoadingAction(hackathonId);
    try {
      // Hit our FastAPI backend to launch the Playwright agent
      const res = await fetch("http://localhost:8000/api/apply", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          profile: mockProfile,
          url: url
        })
      });
      const data = await res.json();
      alert(data.status); // Alerts "Agent Launched..."
      
      // Update UI
      setHackathons(hackathons.map(h => h.id === hackathonId ? { ...h, status: "Drafting" } : h));
    } catch (err) {
      alert("Error connecting to agent backend.");
    }
    setLoadingAction(null);
  };

  const handleCalendarSync = async (hackathon: any) => {
    // Open Google Calendar in a new tab immediately for the user
    window.open("https://calendar.google.com/calendar/r", "_blank");
    
    try {
      const res = await fetch("http://localhost:8000/api/calendar/sync", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: hackathon.title,
          start_date: hackathon.start_date,
          end_date: hackathon.end_date,
          url: hackathon.url
        })
      });
      const data = await res.json();
      alert(data.message);
      
      if (data.status === "Success") {
        setHackathons(hackathons.map(h => h.id === hackathon.id ? { ...h, status: "Synced to Calendar" } : h));
      }
    } catch (err) {
      alert("Error syncing to calendar via API, but Google Calendar was opened in a new tab.");
    }
  };

  return (
    <div className="container" style={{ paddingBottom: '4rem' }}>
      <header style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        padding: '2rem 0',
        borderBottom: '1px solid var(--border-color)',
        marginBottom: '2rem'
      }}>
        <div>
          <h1 className="gradient-text" style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>Hackathon Saathi</h1>
          <p style={{ color: 'var(--text-muted)' }}>Your Agentic Hackathon Companion</p>
        </div>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button 
            className={`btn ${activeTab === 'discover' ? 'btn-primary' : 'btn-outline'}`}
            onClick={() => setActiveTab('discover')}
          >
            Discover Matches
          </button>
          <button 
            className={`btn ${activeTab === 'profile' ? 'btn-primary' : 'btn-outline'}`}
            onClick={() => setActiveTab('profile')}
          >
            My Profile
          </button>
        </div>
      </header>

      <main className="animate-fade-in">
        {activeTab === 'discover' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
              <h2>Highly Recommended For You</h2>
              <button className="btn btn-outline" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ color: 'var(--accent)' }}>●</span> Auto-Scan Active
              </button>
            </div>
            
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '2rem' }}>
              {hackathons.map(hackathon => (
                <div key={hackathon.id} className="glass-panel" style={{ padding: '2rem', transition: 'transform var(--transition-normal)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                    <span style={{ 
                      background: 'rgba(255,255,255,0.1)', 
                      padding: '0.25rem 0.75rem', 
                      borderRadius: '999px',
                      fontSize: '0.75rem',
                      color: 'var(--text-muted)'
                    }}>
                      {hackathon.platform}
                    </span>
                    <span style={{ 
                      color: hackathon.status.includes('Synced') ? 'var(--accent)' : '#fbbf24',
                      fontWeight: 600,
                      fontSize: '0.85rem'
                    }}>
                      {hackathon.status.includes('Synced') ? '✓ Calendar Synced' : `⭐ ${hackathon.matchScore}% Match`}
                    </span>
                  </div>
                  
                  <h3 style={{ fontSize: '1.4rem', marginBottom: '0.5rem' }}>{hackathon.title}</h3>
                  
                  <div style={{ display: 'flex', gap: '1rem', color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1.5rem' }}>
                    <span>📅 {hackathon.date}</span>
                    <span>🏆 {hackathon.prize}</span>
                  </div>
                  
                  <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '2rem' }}>
                    {hackathon.tags.map(tag => (
                      <span key={tag} style={{ 
                        background: 'rgba(99, 102, 241, 0.1)', 
                        color: 'var(--primary)',
                        padding: '0.2rem 0.6rem', 
                        borderRadius: '4px',
                        fontSize: '0.8rem'
                      }}>
                        {tag}
                      </span>
                    ))}
                  </div>
                  
                  <div style={{ display: 'flex', gap: '0.5rem', flexDirection: 'column' }}>
                    <button 
                      className="btn btn-primary" 
                      onClick={() => handleApply(hackathon.id, hackathon.url)}
                      disabled={loadingAction === hackathon.id || hackathon.status !== "Recommended"}
                    >
                      {loadingAction === hackathon.id ? 'Launching Agent...' : (hackathon.status !== "Recommended" ? hackathon.status : 'Agent Auto-Apply ⚡')}
                    </button>
                    
                    {(hackathon.status === "Drafting" || hackathon.status === "Synced to Calendar") && (
                       <button 
                         className="btn btn-outline" 
                         onClick={() => handleCalendarSync(hackathon)}
                       >
                         📅 Sync to Google Calendar
                       </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'profile' && (
           /* ... existing profile jsx ... */
           <div className="glass-panel animate-fade-in" style={{ padding: '3rem', maxWidth: '800px', margin: '0 auto' }}>
             <h2 style={{ marginBottom: '2rem' }}>Agent Configuration Profile</h2>
             <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
               The Auto-Apply Agent uses this data to fill out your hackathon submissions.
             </p>
             <div style={{ display: 'grid', gap: '1.5rem' }}>
               <div><label className="input-label">Full Name</label><input type="text" className="input-field" defaultValue="Anant" /></div>
               <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                 <div><label className="input-label">GitHub URL</label><input type="text" className="input-field" defaultValue="github.com/anant" /></div>
                 <div><label className="input-label">LinkedIn URL</label><input type="text" className="input-field" defaultValue="linkedin.com/in/anant" /></div>
               </div>
               <div><label className="input-label">Technical Skills</label><input type="text" className="input-field" defaultValue="React, Node.js, Python, TypeScript, LangChain" /></div>
               <div><label className="input-label">Bio</label><textarea className="input-field" rows={4} defaultValue="I love building autonomous AI agents." /></div>
               <button className="btn btn-primary" style={{ marginTop: '1rem', justifySelf: 'start' }}>Save Profile</button>
             </div>
           </div>
        )}
      </main>
    </div>
  );
}

export default App;
