import React, { useState, useRef } from 'react';
import axios from 'axios';
import { Loader2 } from 'lucide-react';
import { FaCog, FaTimes,FaDownload } from 'react-icons/fa'; // Import FaTimes
import Tooltip from '@mui/material/Tooltip';

//Tasks:
//Download button with file +design
//Preferences- different logic to update button
//Formatting validations(metadata file is correct struct)
export function ResearchForm() {
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: '',
    notes: '',
    file1: null,
    file2: null,
  });
  const [showPopup, setShowPopup] = useState(false);
  const [jsonInput, setJsonInput] = useState('{"title": "", "description": "", "category": "", "notes": ""}');
  const [jsonObject, setJsonObject] = useState({
    ANOVA: '5',
    PCA: '7',
    alg13: '1',
    alg41: '1',
  });

  const fileInput1Ref = useRef(null);
  const fileInput2Ref = useRef(null);

  const togglePopup = () => {
    setShowPopup(!showPopup);
  };

  const handleJsonChange = (e) => {
    const inputValue = e.target.value;
    setJsonInput(inputValue);
    try {
      setJsonObject(JSON.parse(inputValue));
    } catch (e) {
      console.error('Invalid JSON', e);
    }
  };

  const generateFormFields = () => {
    return Object.keys(jsonObject).map((key) => (
      <div key={key}>
        <label className="block text-sm font-medium text-gray-700">{key}</label>
        <input
          type="number"
          min="0"
          max="10"
          value={jsonObject[key]}
          onChange={(e) => handleFieldChange(key, e)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          required
        />
        {jsonObject[key] < 0 || jsonObject[key] > 10 ? (
          <p className="text-red-500 text-sm">Please enter a number between 0 and 10.</p>
        ) : null}
      </div>
    ));
  };

  const handleFieldChange = (key, e) => {
    const newValue = e.target.value;
    if (newValue >= 0 && newValue <= 10) {
      setJsonObject((prev) => ({
        ...prev,
        [key]: newValue,
      }));
    } else {
      console.error('Value must be between 0 and 10');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const form = new FormData();
      form.append('title', formData.title);
      form.append('description', formData.description);
      form.append('category', formData.category);
      form.append('notes', formData.notes);
      console.log(formData);

      if (formData.file1) form.append('file1', formData.file1);
      if (formData.file2) form.append('file2', formData.file2);
      console.log(form);

      await axios.post('http://localhost:3000/api/research', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setFormData({
        title: '',
        description: '',
        category: '',
        notes: '',
        file1: null,
        file2: null,
      });

      fileInput1Ref.current.value = '';
      fileInput2Ref.current.value = '';
      alert('Research data submitted successfully!');
    } catch (error) {
      console.error('Error:', error);
      alert('Error submitting research data');
    } finally {
      setLoading(false);
    }
  };
  const handleClean = () => {
    // Reset all form data
    setFormData({
      title: '',
      description: '',
      category: '',
      notes: '',
      file1: null,
      file2: null,
    });

    // Reset file input fields
    fileInput1Ref.current.value = '';
    fileInput2Ref.current.value = '';

    // Reset algorithm preferences
    setJsonObject({
      ANOVA: '5',
      PCA: '7',
      alg13: '1',
      alg41: '1',
    });

    // Reset JSON input
    setJsonInput('{"title": "", "description": "", "category": "", "notes": ""}');
  };

  // Handle File2 download
  const handleDownloadFile2 = () => {
    if (formData.file2) {
      alert(URL.createObjectURL(formData.file2))
      const url = URL.createObjectURL(formData.file2);
      const link = document.createElement('a');
      link.href = url;
      link.download = formData.file2.name; // Use the file name from the input field
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url); // Clean up the object URL
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6">Add Research Data</h2>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700">Title</label>
          <input
            type="text"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Description</label>
          <textarea
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            rows={3}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Category</label>
          <input
            type="text"
            value={formData.category}
            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Notes</label>
          <textarea
            value={formData.notes}
            onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            rows={3}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">File 1</label>
          <input
            ref={fileInput1Ref}
            type="file"
            onChange={(e) => setFormData({ ...formData, file1: e.target.files?.[0] || null })}
            className="mt-1 block w-full"
          />
        </div>

        <div>
  <div className="flex items-center space-x-4">
    <label className="text-sm font-medium text-gray-700">File 2</label>
  </div>

  <div className="flex items-center space-x-4 mt-2">
    <input
      ref={fileInput2Ref}
      type="file"
      onChange={(e) => setFormData({ ...formData, file2: e.target.files?.[0] || null })}
      className="block w-1/3" // Adjust the width as needed
    />
    {formData.file2 && (
          <Tooltip title="Download an example of metadata struct">

 <button
 
 type="button"
 onClick={handleDownloadFile2}  
 className="inline-flex items-center px-2 py-1 border border-gray-300 rounded-md shadow-sm text-xs font-medium text-gray-700 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
>
 <FaDownload   className="text-sm" /> {/* Install/download icon */}

 </button>
 </Tooltip>


    )}
    {/* Tooltip component */}
    
  </div>
</div>


        <div>
          <button type="button" onClick={togglePopup} style={styles.button}>
            <FaCog style={styles.icon} /> Edit Algorithm Preferences
          </button>

          {showPopup && (
            <div style={styles.popup}>
              <div style={styles.popupContent}>
                {/* Close icon */}
                <span
                  style={styles.closeIcon}
                  onClick={togglePopup}
                >
                  <FaTimes style={{ fontSize: '20px', cursor: 'pointer', color: '#007BFF' }} />
                </span>

                <div>
                  <h2 style={{ fontSize: '16px' }} className="text-2xl font-bold">
                    Algorithms preferences rank:
                  </h2>
                  <h6 style={{ fontSize: '10px' }} className="text-2xl">
                    (between 0-10)
                  </h6>
                  {generateFormFields()}
                </div>
                {/* Close button with margin */}
                <button
                  style={{ ...styles.button, padding: '5px 10px', marginTop: '10px' }}
                  onClick={togglePopup}
                >
                  Close
                </button>
              </div>
            </div>
          )}
        </div>      
        <div className="flex space-x-4">
        <button
            type="button"
            onClick={handleClean}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-gray-700 bg-gray-200 hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
          >
            Clean
          </button>
        <button
          type="submit"
          disabled={loading}
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          {loading ? <Loader2 className="animate-spin" /> : 'Submit Research'}
        </button>
        </div>      

      </form>
    </div>
  );
}

const styles = {
  button: {
    display: 'flex',
    alignItems: 'center',
    backgroundColor: '#007BFF',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    padding: '10px 20px',
    cursor: 'pointer',
  },
  icon: {
    marginRight: '8px',
  },
  popup: {
    position: 'fixed',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    width: '267px',
    height: 'auto',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  },
  popupContent: {
    backgroundColor: 'white',
    padding: '20px',
    textAlign: 'center',
    borderRadius: '5px',
    maxHeight: '80vh',
    overflowY: 'auto',
  },
  closeIcon: {
    position: 'absolute',
    top: '10px',
    right: '10px',
  },
};

