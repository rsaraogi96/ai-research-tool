import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from '@/components/layout/Layout';
import Dashboard from '@/pages/Dashboard';
import Browse from '@/pages/Browse';
import SearchPage from '@/pages/SearchPage';
import InstancePage from '@/pages/InstancePage';
import People from '@/pages/People';
import Companies from '@/pages/Companies';
import Analytics from '@/pages/Analytics';
import SettingsPage from '@/pages/SettingsPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/browse" element={<Browse />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="/instance/:id" element={<InstancePage />} />
          <Route path="/people" element={<People />} />
          <Route path="/companies" element={<Companies />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
