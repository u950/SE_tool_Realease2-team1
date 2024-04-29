import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Interactions from './graph_interactions';

const DisplayGraph = () => {
    const { path_name } = useParams();
    const [dependencies, setDependencies] = useState(null);


    useEffect(() => {
        const fetchDependencies = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/get_dependencies', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        directory: path_name,
                    }),
                });
                if (!response.ok) throw new Error('Failed to fetch dependencies');
                const data = await response.json();
                setDependencies(data);
            } catch (error) {
                console.error("Fetching dependencies failed:", error);
            }
        };

        if (path_name) {
            fetchDependencies();
        }
    }, [path_name]);

    return (
        <div>
            <h2 style={{marginLeft: "500px"}}>Dependencies for: {path_name}</h2>
            {dependencies && <Interactions data={dependencies} />}
        </div>
    );
};

export default DisplayGraph;