import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';

import Dashboard from './pages/Dashboard';
import NewAnalysis from './pages/NewAnalysis';
import AnalysisResults from './pages/AnalysisResults';
import StandardsExplorer from './pages/StandardsExplorer';
import StandardsGraph from './pages/StandardsGraph';
import TenderHistory from './pages/TenderHistory';
//import MockProcurementPortal from './pages/MockProcurementPortal';
import Reports from './pages/Reports';
import SettingsAbout from './pages/SettingsAbout';

export default function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 font-sans">
        <Header />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/new-analysis" element={<NewAnalysis />} />
            <Route path="/results" element={<AnalysisResults />} />
            <Route path="/explorer" element={<StandardsExplorer />} />
            <Route path="/graph" element={<StandardsGraph />} />
            <Route path="/history" element={<TenderHistory />} />
            {/* <Route path="/portal" element={<MockProcurementPortal />} /> */}
            <Route path="/reports" element={<Reports />} />
            <Route path="/settings" element={<SettingsAbout />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}
