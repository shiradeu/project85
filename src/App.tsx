import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Sidebar } from './components/Sidebar';
import { ResearchForm } from './components/ResearchForm';
import { ResearchResults } from './components/ResearchResults';
import { LogIn } from 'lucide-react';

axios.defaults.withCredentials = true;

export default function App() {
  const [user, setUser] = useState(null);
  const [currentRoute, setCurrentRoute] = useState('add');

  useEffect(() => {
   // checkUser();
  }, []);

  const checkUser = async () => {
    try {
      const { data } = await axios.get('http://localhost:5176/api/user');
      setUser(data);
    } catch (error) {
      console.error('Error checking user:', error);
    }
  };

  // if (!user) {
 //    return (
 //     <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
   //      <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
    //      <h1 className="text-2xl font-bold mb-6">Research Management System</h1>
    //       <a
    //         href="http://localhost:3000/auth/google"
    //         className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
   //        >
    //       <LogIn className="mr-2 h-5 w-5" />
    //         Sign in with Google
  //        </a>
   //     </div>
   //    </div>
  //  );
   //}

  return (
    <div className="flex min-h-screen bg-gray-100">
      <Sidebar onNavigate={setCurrentRoute} currentRoute={currentRoute} />
      <main className="flex-1 p-8">
        {currentRoute === 'add' ? <ResearchForm /> : <ResearchResults />}
      </main>
    </div>
  );
}