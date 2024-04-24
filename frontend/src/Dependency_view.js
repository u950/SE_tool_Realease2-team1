import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const DisplayGraph = () => {
    const { path_name } = useParams();
    const [dependencies, setDependencies] = useState(null);

    useEffect(() => {
        const fetchDependencies = async () => {
            try{
                const response = await fetch('http://localhost:5000/get_dependencies', {
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
            }   catch (error) {
                console.error("Fetching dependencies failed:", error);
            }
        };

        if (path_name) {
            fetchDependencies();
        }
    }, [path_name]);

    return (
        <div>
            <h2>Dependencies for: {path_name}</h2> 
            <pre>{JSON.stringify(dependencies, null, 2)}</pre> {/* Displaying the dependencies in a preformatted text */}

        </div>
    );
};

export default DisplayGraph