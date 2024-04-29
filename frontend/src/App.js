import React, { useState } from 'react';
import {useNavigate} from 'react-router-dom'
import Graph from './graph'

function App() {
  const [repoUrl, setRepoUrl] = useState("");
  const [repoName, setRepoName] = useState("");
  const [message, setMessage] = useState("");
  const [isLoading, setLoading] = useState(false);
  const navigate = useNavigate();
  const [files, setFiles]= useState([])
  const [path_name, setPath] = useState()

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage('')
    setLoading(true);
    setFiles([])
    setPath('')
    try {
      const response = await fetch('http://localhost:5000/download_repo', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          repo_url: repoUrl,
          repo_name: repoName,
        }),
      });
      // if (data.repo_name){
      //   navigate(`/success/${data.repo_name}`);// redirecton to view files 
      // }
      const data = await response.json()

      if(data.error)
        setMessage(data.error)
      else if (data.repo_name) {
        setFiles(data.files || ["erorr loading files"])
        setPath(data.repo_name)
      }
    } catch (error) {
      console.error('Error:', error);
      setMessage('Failed to clone the repository.');
    }finally{
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>MERN Repo Analyser</h1>
        { isLoading ? ( <div className='spinner'></div>
        ) : (
          <form onSubmit={handleSubmit}>
        <label>
          Repository URL:
          <input
            type="text"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            required
          />
        </label>
        <br />
        <label>
          Repository Name (optional):
          <input
            type="text"
            value={repoName}
            onChange={(e) => setRepoName(e.target.value)}
          />
        </label>
        <br />
        <button type="submit">Clone Repository</button>
      </form>
        )}
      {message && <p>{message}</p>}
      <div className='fileList'>
        {files.length > 0 && (
            <h3>Repository : '{path_name}'  Cloned Successfully</h3>
        )}
      </div>
       <div>
       {path_name && (
          <div>
            <button onClick={() => navigate(`/dependency/${path_name}`)}>
              View Dependencies
            </button>
          </div>
        )}
       </div>
    </div>
    
  );
}



export default App;
