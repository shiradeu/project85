import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Loader2 } from 'lucide-react';
import graphc from '../images/graphc.png'; // Import the image using a relative path
import grapha from '../images/grapha.jpeg'; // Import the image using a relative path
import graphb from '../images/graphb.jpeg'; // Import the image using a relative path

interface ResearchData {
  _id: string;
  title: string;
  description: string;
  category: string;
  notes: string;
  createdAt: string;
  file1Path?: string;
  file2Path?: string;
}

export function ResearchResults() {
  const [loading, setLoading] = useState(true);
  const [results, setResults] = useState<ResearchData[]>([]);
  const [expandedResultId, setExpandedResultId] = useState<string | null>(null);

  useEffect(() => {
    fetchResults();
  }, []);

  const fetchResults = async () => {
    try {
      const { data } = await axios.get('http://localhost:3000/api/research');
      setResults(data);
    } catch (error) {
      console.error('Error:', error);
      alert('Error fetching research data');
    } finally {
      setLoading(false);
    }
  };

  const toggleExpand = (id: string) => {
    setExpandedResultId((prevId) => (prevId === id ? null : id));
  };

  const getTextStyle = (index: number) => {
    if (index >= 1 && index <= 4) return 'text-green-600';
    if (index >= 5 && index <= 8) return 'text-orange-600';
    if (index >= 9 && index <= 12) return 'text-red-600';
    return '';
  };

  const renderNumberedText = () => {
    return (
      <div>
        <h4 className="text-lg font-semibold text-gray-900">Research Insights:</h4>
        {Array.from({ length: 12 }, (_, i) => {
          const lineNumber = i + 1;
          const letter =  "relation between " +  String.fromCharCode(96 + lineNumber)+" and " + String.fromCharCode(98 + lineNumber);
          return (
            <p key={lineNumber} className={`text-sm font-medium ${getTextStyle(lineNumber)}`}>
              {lineNumber}. {letter}
            </p>
          );
        })}

      </div>
    );
  };

  const renderGraphs = () => {
    return (
      <div>
        <h4 className="text-lg font-semibold text-gray-900">Research Visual Insights Graphs:</h4>
        <div className="grid grid-cols-3 gap-2">
        <img src={grapha} alt="Example" style={{ width: '300px', height: 'auto' }} />
        <img src={graphb} alt="Example" style={{ width: '300px', height: 'auto' }} />
        <img src={graphc} alt="Example" style={{ width: '300px', height: 'auto' }} />
             </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="animate-spin h-8 w-8 text-blue-600" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6">Research Results</h2>
      <div className="space-y-6">
        {results.map((result) => {
          const isExpanded = expandedResultId === result._id;

          return (
            <div
              key={result._id}
              className={`bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow ${
                isExpanded ? 'border border-blue-500' : ''
              }`}
            >
              <h3 className="text-xl font-semibold text-gray-900">{result.title}</h3>
              <p className="text-sm text-gray-500 mt-1">
                Category: {result.category} • Added on{' '}
                {new Date(result.createdAt).toLocaleDateString()}
              </p>
              <p className="mt-3 text-gray-700">
                {isExpanded ? result.description : `${result.description.slice(0, 100)}...`}
              </p>
              {isExpanded && (
                <div className="mt-3">
                  {renderNumberedText()}
                  <div className="mt-6">{renderGraphs()}</div>
                  <div>
                  <p className="text-sm mt-4">
        <a
          href="http://localhost:3000/full-conclusions-document"
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-600 hover:text-blue-800"
        >
          For the full conclusions document
        </a>
      </p>
                  </div>
                </div>
                
              )}
              {result.notes && isExpanded && (
                <div className="mt-3">
                  <h4 className="font-medium text-gray-900">Notes:</h4>
                  <p className="text-gray-700">{result.notes}</p>
                </div>
              )}
              {(result.file1Path || result.file2Path) && isExpanded && (
                <div className="mt-3">
                  <h4 className="font-medium text-gray-900">Attached Files:</h4>
                  <div className="mt-2 space-y-1">
                    {result.file1Path && (
                      <div className="text-blue-600 hover:text-blue-800">
                        <a
                          href={`http://localhost:3000/${result.file1Path}`}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          File 1
                        </a>
                      </div>
                    )}
                    {result.file2Path && (
                      <div className="text-blue-600 hover:text-blue-800">
                        <a
                          href={`http://localhost:3000/${result.file2Path}`}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          File 2
                        </a>
                      </div>
                    )}
                  </div>
                </div>
              )}
              <button
                onClick={() => toggleExpand(result._id)}
                className="mt-4 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700"
              >
                {isExpanded ? 'Collapse' : 'Expand'}
              </button>
            </div>
          );
        })}
        {results.length === 0 && (
          <p className="text-center text-gray-500">No research data found.</p>
        )}
      </div>
    </div>
  );
}