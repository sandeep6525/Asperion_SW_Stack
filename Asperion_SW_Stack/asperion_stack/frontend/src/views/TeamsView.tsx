// @ts-ignore
import { loadTeams } from '../utils/dataLoaders.js';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export const TeamsView: React.FC = () => {
  useEffect(() => {
    try {
      loadTeams();
    } catch (e) {
      console.error('Error in loadTeams:', e);
    }
  }, []);

  return (
    <div className="w-full">
      <section id="view-teams" className="module-view ">
                {/* Balanced Two-Column Enterprise Communications Header */}
                <div className="mb-5 grid grid-cols-1 lg:grid-cols-12 gap-4 bg-slate-900 p-5 sm:p-6 rounded-2xl border border-slate-800 text-white shadow-md">
                    {/* Main Content Area (~67% width on desktop) */}
                    <div className="lg:col-span-8 flex flex-col justify-between gap-4">
                        <div className="flex items-start sm:items-center gap-4">
                            <div className="w-12 h-12 rounded-xl bg-slate-950 border border-cyan-500/30 p-1.5 flex items-center justify-center shrink-0 shadow-sm">
                                <img src="/static/img/logo.png" alt="Asperion Brand" className="w-full h-full object-contain" />
                            </div>
                            <div className="min-w-0">
                                <h2 className="text-lg sm:text-2xl font-bold text-white tracking-tight">
                                    Asperion Teams &amp; Enterprise Communications Hub
                                </h2>
                                <p className="text-xs sm:text-sm text-slate-300 mt-1 leading-relaxed">
                                    Unified workspace collaboration: Departmental channels, 1:1 direct messaging, live virtual conference huddles, interactive document embedding &amp; autonomous Sentinel AI Bot.
                                </p>
                            </div>
                        </div>
                        <div className="flex flex-wrap items-center gap-2 pt-1">
                            <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-slate-950 text-indigo-300 border border-indigo-500/30">ISO 27001 AUDIT READY</span>
                            <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-slate-950 text-cyan-300 border border-cyan-500/30">SENTINEL AI BOT ACTIVE</span>
                            <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-slate-950 text-emerald-300 border border-emerald-500/30">VIRTUAL HUDDLES &amp; SCREENSHARE</span>
                            <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-slate-950 text-purple-300 border border-purple-500/30">DOCUMENT EMBEDS</span>
                        </div>
                    </div>

                    {/* Right-Side Information & Controls Panel (~33% width on desktop) */}
                    <div className="lg:col-span-4 bg-slate-950/80 rounded-xl border border-slate-800 p-4 flex flex-col justify-between gap-3.5">
                        <div className="flex items-center justify-between gap-2 pb-2.5 border-b border-slate-800/80">
                            <div className="flex items-center gap-2 text-xs text-slate-300">
                                <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse shrink-0"></span>
                                <span className="font-semibold text-slate-200">My Status:</span>
                            </div>
                            <select id="teams-my-presence-select" onChange={() => {}} className="bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1 text-xs text-emerald-400 font-semibold focus:outline-none focus:ring-1 focus:ring-cyan-500">
                                <option value="ONLINE" selected>🟢 Available (HQ)</option>
                                <option value="IN_MEETING">🟡 In Meeting</option>
                                <option value="FOCUS_DND">🔴 Focus Mode (DND)</option>
                                <option value="AWAY">⚪ Away</option>
                            </select>
                        </div>
                        <div className="grid grid-cols-2 gap-2.5">
                            <button onClick={() => {}} className="w-full px-3 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs rounded-lg transition shadow-sm flex items-center justify-center gap-1.5">
                                <i className="fa-solid fa-headset"></i> Instant Huddle
                            </button>
                            <button onClick={() => {}} className="w-full px-3 py-2 bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs rounded-lg transition shadow-sm flex items-center justify-center gap-1.5">
                                <i className="fa-solid fa-plus-circle"></i> New Channel
                            </button>
                        </div>
                    </div>
                </div>

                {/* 4 KPI Metrics Cards */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3.5 mb-5">
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-400 mb-1">
                            <span className="text-[10px] font-bold uppercase tracking-wider">Active Channels</span>
                            <i className="fa-solid fa-hashtag text-indigo-500"></i>
                        </div>
                        <div id="teams-stat-channels" className="text-xl font-black text-slate-900 mt-1">9 Channels</div>
                        <div className="text-[10px] text-slate-500 mt-0.5">Public, DMs & War Rooms</div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-400 mb-1">
                            <span className="text-[10px] font-bold uppercase tracking-wider">Team Presence</span>
                            <i className="fa-solid fa-users text-emerald-500"></i>
                        </div>
                        <div id="teams-stat-online" className="text-xl font-black text-emerald-600 mt-1">6 Online</div>
                        <div className="text-[10px] text-emerald-600 font-semibold mt-0.5">Verified Active Roster</div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-400 mb-1">
                            <span className="text-[10px] font-bold uppercase tracking-wider">Messages Dispatched</span>
                            <i className="fa-solid fa-comments text-blue-500"></i>
                        </div>
                        <div id="teams-stat-messages" className="text-xl font-black text-slate-900 mt-1">--</div>
                        <div className="text-[10px] text-slate-500 mt-0.5">Today across all threads</div>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div className="flex items-center justify-between text-slate-400 mb-1">
                            <span className="text-[10px] font-bold uppercase tracking-wider">Virtual Huddles & War Rooms</span>
                            <i className="fa-solid fa-tower-broadcast text-purple-500"></i>
                        </div>
                        <div id="teams-stat-huddles" className="text-xl font-black text-purple-700 mt-1">1 Active</div>
                        <div className="text-[10px] text-purple-600 font-semibold mt-0.5">Live Audio & Screen Share</div>
                    </div>
                </div>

                {/* Main Teams Two-Column Layout */}
                <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col md:flex-row h-[720px]">
                    {/* Left Sidebar Rail: Channels, DMs, War Rooms & Roster */}
                    <div className="w-full md:w-80 bg-slate-900 text-slate-300 flex flex-col border-r border-slate-800 shrink-0">
                        {/* Search & Fast Filters */}
                        <div className="p-3.5 border-b border-slate-800">
                            <div className="relative">
                                <i className="fa-solid fa-magnifying-glass absolute left-3 top-2.5 text-slate-500 text-xs"></i>
                                <input id="teams-search-channels" onInput={() => {}} type="text" placeholder="Jump to channel or person..." className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-8 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500" />
                            </div>
                        </div>

                        {/* Scrollable Channels & DMs List */}
                        <div className="flex-1 overflow-y-auto p-3 space-y-4 text-xs">
                            {/* Section: Departmental Channels */}
                            <div>
                                <div className="flex items-center justify-between text-[10px] font-bold uppercase tracking-wider text-slate-400 px-2 mb-1.5">
                                    <span className="flex items-center gap-1.5"><i className="fa-solid fa-layer-group text-indigo-400"></i> Channels</span>
                                    <button onClick={() => {}} className="hover:text-white transition p-0.5" title="Add Channel"><i className="fa-solid fa-plus"></i></button>
                                </div>
                                <div id="teams-channels-list" className="space-y-0.5">
                                    {/* Populated dynamically by app.js */}
                                </div>
                            </div>

                            {/* Section: Direct Messages */}
                            <div>
                                <div className="flex items-center justify-between text-[10px] font-bold uppercase tracking-wider text-slate-400 px-2 mb-1.5">
                                    <span className="flex items-center gap-1.5"><i className="fa-solid fa-user-group text-emerald-400"></i> Direct Messages</span>
                                </div>
                                <div id="teams-dms-list" className="space-y-0.5">
                                    {/* Populated dynamically by app.js */}
                                </div>
                            </div>

                            {/* Section: Team Live Presence */}
                            <div className="pt-2 border-t border-slate-800">
                                <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400 px-2 mb-2">
                                    <i className="fa-solid fa-satellite-dish text-cyan-400 mr-1"></i> Live Team Presence (${6})
                                </div>
                                <div id="teams-presence-roster" className="space-y-1.5 px-1">
                                    {/* Populated dynamically by app.js */}
                                </div>
                            </div>
                        </div>

                        {/* User Profile Card in Left Rail */}
                        <div className="p-3 bg-slate-950/80 border-t border-slate-800 flex items-center justify-between text-xs">
                            <div className="flex items-center gap-2.5 min-w-0">
                                <div className="w-8 h-8 rounded-full bg-indigo-600 text-white font-bold flex items-center justify-center text-xs shrink-0 relative">
                                    V
                                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 border-2 border-slate-950 absolute -bottom-0.5 -right-0.5"></span>
                                </div>
                                <div className="min-w-0">
                                    <div className="font-bold text-white truncate text-xs">Director Varadi Vijay</div>
                                    <div className="text-[10px] text-slate-400 truncate">Founder &bull; Bangalore HQ</div>
                                </div>
                            </div>
                            <button onClick={() => {}} className="w-7 h-7 rounded-lg bg-slate-800 hover:bg-indigo-600 text-slate-300 hover:text-white flex items-center justify-center transition" title="Start Virtual Huddle">
                                <i className="fa-solid fa-headset text-xs"></i>
                            </button>
                        </div>
                    </div>

                    {/* Right Conversation Workspace Pane */}
                    <div className="flex-1 flex flex-col bg-white overflow-hidden">
                        {/* Channel Header Bar */}
                        <div className="p-3.5 border-b border-slate-200 flex items-center justify-between bg-slate-50/70">
                            <div className="flex items-center gap-3 min-w-0">
                                <div id="teams-channel-avatar-icon" className="w-9 h-9 rounded-xl bg-indigo-100 text-indigo-700 flex items-center justify-center font-bold text-base shrink-0">
                                    #
                                </div>
                                <div className="min-w-0">
                                    <div className="flex items-center gap-2">
                                        <h3 id="teams-current-channel-name" className="font-bold text-slate-900 text-sm truncate">#engineering-devops</h3>
                                        <span id="teams-current-channel-type" className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 text-blue-800">PUBLIC</span>
                                    </div>
                                    <p id="teams-current-channel-topic" className="text-xs text-slate-500 truncate">Architecture RFCs & Sprint Delivery</p>
                                </div>
                            </div>
                            <div className="flex items-center gap-2">
                                <button onClick={() => {}} id="teams-btn-active-huddle" className="px-3 py-1.5 bg-purple-50 hover:bg-purple-100 text-purple-700 border border-purple-200 rounded-lg text-xs font-bold transition flex items-center gap-1.5 shadow-sm">
                                    <i className="fa-solid fa-headset animate-pulse text-purple-600"></i> Huddle Active (Join)
                                </button>
                                <button onClick={() => {}} className="px-2.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold transition" title="Ask Sentinel AI Bot">
                                    <i className="fa-solid fa-robot text-cyan-600 mr-1"></i> Bot
                                </button>
                                <button onClick={() => {}} className="px-2.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold transition" title="Refresh Feed">
                                    <i className="fa-solid fa-rotate text-xs"></i>
                                </button>
                            </div>
                        </div>

                        {/* Pinned Announcement Banner (if any) */}
                        <div id="teams-pinned-banner" className="hidden px-4 py-2 bg-amber-50 border-b border-amber-200 flex items-center justify-between text-xs text-amber-900">
                            <div className="flex items-center gap-2 truncate">
                                <i className="fa-solid fa-thumbtack text-amber-600"></i>
                                <span className="font-bold">Pinned:</span>
                                <span id="teams-pinned-text" className="truncate">Announcement summary...</span>
                            </div>
                            <button onClick={() => {}} className="text-amber-700 hover:text-amber-900 text-[10px] font-semibold underline shrink-0 ml-2">Unpin</button>
                        </div>

                        {/* Scrollable Message Stream */}
                        <div id="teams-messages-container" className="flex-1 overflow-y-auto p-4 space-y-3.5 bg-slate-50/30">
                            {/* Injected dynamically by app.js */}
                        </div>

                        {/* Message Composer Bar */}
                        <div className="p-3 bg-white border-t border-slate-200">
                            <form onSubmit={(e) => e.preventDefault()} className="space-y-2">
                                {/* Formatting & Attachment Action Bar */}
                                <div className="flex items-center justify-between text-xs text-slate-500">
                                    <div className="flex items-center gap-1.5">
                                        <button type="button" onClick={() => {}} className="p-1 hover:text-slate-800 hover:bg-slate-100 rounded" title="Bold">
                                            <i className="fa-solid fa-bold text-xs"></i>
                                        </button>
                                        <button type="button" onClick={() => {}} className="p-1 hover:text-slate-800 hover:bg-slate-100 rounded" title="Italic">
                                            <i className="fa-solid fa-italic text-xs"></i>
                                        </button>
                                        <button type="button" onClick={() => {}} className="p-1 hover:text-slate-800 hover:bg-slate-100 rounded" title="Code Block">
                                            <i className="fa-solid fa-code text-xs"></i>
                                        </button>
                                        <span className="text-slate-300">|</span>
                                        {/* Quick Embed Dropdown */}
                                        <select id="teams-quick-embed-select" onChange={() => {}} className="text-[11px] border border-slate-200 rounded px-2 py-0.5 bg-slate-50 text-slate-700 font-medium">
                                            <option value="">📎 Attach Official System Document...</option>
                                            <option value="OFFER_LETTER">📄 Offer Letter (HR-ONB-01: Siddharth)</option>
                                            <option value="PURCHASE_ORDER">📦 Purchase Order (PO-2026-001: AWS)</option>
                                            <option value="INCIDENT_WAR_ROOM">🛡️ CERT-In Incident (INC-2026-0881)</option>
                                            <option value="BOARD_RESOLUTION">⚖️ Board Resolution (ADT/RES/2026/001)</option>
                                        </select>
                                    </div>
                                    <div className="flex items-center gap-1.5">
                                        <span className="text-[10px] text-slate-400 font-mono">Press <strong>Enter</strong> to send</span>
                                    </div>
                                </div>

                                {/* Text Input & Send Button */}
                                <div className="flex items-center gap-2">
                                    <input id="teams-message-input" type="text" autoComplete="off" required placeholder="Type a message, mention @sentinel, or enter /status, /kpi, /certin..." className="flex-1 px-3.5 py-2.5 border border-slate-300 rounded-xl text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white" />
                                    <button type="submit" className="px-5 py-2.5 bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white font-bold text-xs rounded-xl transition shadow flex items-center gap-1.5 shrink-0">
                                        <i className="fa-solid fa-paper-plane"></i> Send
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </section>

            {/* 14B. Asperion SharePoint & Enterprise Knowledge Hub View */}
    </div>
  );
};

export default TeamsView;
