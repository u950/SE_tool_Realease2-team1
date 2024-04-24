import React from "react";
import App from "./App";
import {BrowserRouter,Routes, Route} from 'react-router-dom'
import DisplayGraph from './Get_depenpendency'
import NetworkGraph from './graph'

function Main() {
    return(
        <div>
            <BrowserRouter>
                <Routes>
                    <Route path="/dependency/:path_name" element={<DisplayGraph/>}/>
                    <Route path="/" element={<App/>}/>
                    <Route path="/graph/:path_name" element={<NetworkGraph/>}/>
                </Routes>
            </BrowserRouter>
        </div>
    )
}

export default Main;