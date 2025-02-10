import React from 'react';
import { FolderPlus, List } from 'lucide-react';

interface SidebarProps {
  onNavigate: (route: string) => void;
  currentRoute: string;
}

export function Sidebar({ onNavigate, currentRoute }: SidebarProps) {
  const menuItems = [
    { icon: <FolderPlus size={20} />, text: 'Add Research', route: 'add' },
    { icon: <List size={20} />, text: 'View Results', route: 'results' },
  ];

  return (
    <div className="w-64 bg-gray-800 min-h-screen p-4">
      <div className="space-y-2">
        {menuItems.map((item) => (
          <button
            key={item.route}
            onClick={() => onNavigate(item.route)}
            className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
              currentRoute === item.route
                ? 'bg-blue-600 text-white'
                : 'text-gray-300 hover:bg-gray-700'
            }`}
          >
            {item.icon}
            <span>{item.text}</span>
          </button>
        ))}
      </div>
    </div>
  );
}