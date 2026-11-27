import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Header from './components/Header.tsx';
import Sidebar from './components/Sidebar.tsx';
import MainContentShell from './components/MainContentShell.tsx';

// 24 Operating Modules Views
import DashboardView from './views/DashboardView.tsx';
import GovernanceView from './views/GovernanceView.tsx';
import CRMView from './views/CRMView.tsx';
import FinanceView from './views/FinanceView.tsx';
import HRMSView from './views/HRMSView.tsx';
import PMOView from './views/PMOView.tsx';
import SDLCView from './views/SDLCView.tsx';
import ProcurementView from './views/ProcurementView.tsx';
import GuardrailsView from './views/GuardrailsView.tsx';
import ISOStandardsView from './views/ISOStandardsView.tsx';
import AICloudView from './views/AICloudView.tsx';
import AgenticAIView from './views/AgenticAIView.tsx';
import OperationsView from './views/OperationsView.tsx';
import CryptoToolsView from './views/CryptoToolsView.tsx';
import InfrastructureView from './views/InfrastructureView.tsx';
import SecOpsView from './views/SecOpsView.tsx';
import VaultView from './views/VaultView.tsx';
import StrategyView from './views/StrategyView.tsx';
import AnalyticsView from './views/AnalyticsView.tsx';
import InternalSupportView from './views/InternalSupportView.tsx';
import ITSMView from './views/ITSMView.tsx';
import TeamsView from './views/TeamsView.tsx';
import SharePointView from './views/SharePointView.tsx';
import TrainingView from './views/TrainingView.tsx';

// 3 Dedicated Portals Views
import EmployeePortalView from './views/EmployeePortalView.tsx';
import ClientPortalView from './views/ClientPortalView.tsx';
import VendorPortalView from './views/VendorPortalView.tsx';

import GenericModuleView from './views/GenericModuleView.tsx';
import { ALL_NAV_ITEMS } from './types/modules.ts';

export default function App() {
  const navigate = useNavigate();
  const location = useLocation();

  const pathModule = location.pathname.replace(/^\//, '');
  const [activeModule, setActiveModule] = useState(pathModule || 'dashboard');
  const [isOpenMobile, setIsOpenMobile] = useState(false);
  const [persona, setPersona] = useState('director@asperion.in');

  useEffect(() => {
    if (pathModule && pathModule !== activeModule) {
      setActiveModule(pathModule);
    }
  }, [pathModule]);

  const handleSelectModule = (target: string) => {
    setActiveModule(target);
    navigate(`/${target === 'dashboard' ? '' : target}`);
  };

  const currentMeta = ALL_NAV_ITEMS.find((m) => m.target === activeModule) || ALL_NAV_ITEMS[0];

  const renderActiveView = () => {
    switch (activeModule) {
      // 24 Operating Modules
      case 'dashboard':
      case '':
        return <DashboardView onNavigate={(mod: string) => handleSelectModule(mod)} />;
      case 'governance':
        return <GovernanceView />;
      case 'crm':
        return <CRMView />;
      case 'finance':
        return <FinanceView />;
      case 'hrms':
        return <HRMSView />;
      case 'pmo':
        return <PMOView />;
      case 'sdlc':
        return <SDLCView />;
      case 'procurement':
        return <ProcurementView />;
      case 'guardrails':
        return <GuardrailsView />;
      case 'iso-standards':
        return <ISOStandardsView />;
      case 'ai-cloud':
        return <AICloudView />;
      case 'agentic-ai':
        return <AgenticAIView />;
      case 'operations':
        return <OperationsView />;
      case 'crypto-tools':
        return <CryptoToolsView />;
      case 'infrastructure':
        return <InfrastructureView />;
      case 'secops':
        return <SecOpsView />;
      case 'vault':
        return <VaultView />;
      case 'strategy':
        return <StrategyView />;
      case 'analytics':
        return <AnalyticsView />;
      case 'internal-support':
        return <InternalSupportView />;
      case 'itsm':
        return <ITSMView />;
      case 'teams':
        return <TeamsView />;
      case 'sharepoint':
        return <SharePointView />;
      case 'training':
        return <TrainingView />;

      // 3 Dedicated Portals
      case 'portal-employee':
        return <EmployeePortalView />;
      case 'portal-client':
        return <ClientPortalView />;
      case 'portal-vendor':
        return <VendorPortalView />;

      default:
        return <GenericModuleView moduleMeta={currentMeta} endpoint={currentMeta.endpoint} />;
    }
  };

  return (
    <div className="flex flex-col h-screen overflow-hidden bg-slate-50 font-sans">
      <Header
        onToggleMobileSidebar={() => setIsOpenMobile(!isOpenMobile)}
        persona={persona}
        onSwitchPersona={setPersona}
        onNavigate={handleSelectModule}
      />
      <div className="flex flex-1 overflow-hidden relative">
        <Sidebar
          navItems={ALL_NAV_ITEMS}
          activeModule={activeModule}
          onSelectModule={handleSelectModule}
          isOpenMobile={isOpenMobile}
          onCloseMobile={() => setIsOpenMobile(false)}
        />
        <MainContentShell
          category={currentMeta.category}
          moduleTitle={currentMeta.label}
          onOpenCommandPalette={() => alert('Command Palette (Ctrl+K)')}
          onTriggerSelfHeal={() => alert('Self-Healing Diagnostic initiated...')}
        >
          {renderActiveView()}
        </MainContentShell>
      </div>
    </div>
  );
}
