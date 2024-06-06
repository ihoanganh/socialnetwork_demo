// import React, {useState, useEffect} from 'react';
// import { PostGet, PostForm, PostUpdate, PostDelete } from './components/MyPost';
// import { UserGet, UserPost, UserUpdate, UserDelete} from './components/MyUser';
// import { Layout, Menu } from 'antd';
// import './App.css'


// const { Header, Content } = Layout;

// function App() {
//   return (
//     <div>
//     <h1 className='App-header'>User API</h1>
//     <nav className="navbar">
//       <ul className="navbar-nav">
//         <li className="nav-item">
//           <a href="#" className="nav-link">Home</a>
//         </li>
//         <li className="nav-item">
//           <a href="#" className="nav-link">About</a>
//         </li>
//         <li className="nav-item">
//           <a href="#" className="nav-link">Contact</a>
//         </li>
//         <li className="nav-item">
//           <a href="#" className="nav-link">Delete</a>
//         </li>
//       </ul>
//     </nav>
//     <div className='content'>
//       <UserGet />
//     </div>
    
//   </div>
    
//   );
// }

// export default App;
import React, { Component } from "react";
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
} from "react-router-dom";
import "./App.css";
// import { PostGet, PostForm, PostUpdate, PostDelete } from './components/MyPost';
import { UserGet, UserPost, UserUpdate, UserDelete} from './components/MyUser';

class App extends Component {
    render() {
        return (
            <Router>
                <div className="App">
                    <ul className="App-header">
                        <li>
                            <Link to="/">GET</Link>
                        </li>
                        <li>
                            <Link to="/post">
                               POST
                            </Link>
                        </li>
                        <li>
                            <Link to="/update">
                                UPDATE
                            </Link>
                        </li>
                        <li>
                            <Link to="/delete">
                                DELETE
                            </Link>
                        </li>
                    </ul>
                    <Routes>
                        <Route
                            path="/"
                            element={<UserGet />}
                        ></Route>
                        <Route
                            path="/post"
                            element={<UserPost />}
                        ></Route>
                        <Route
                            path="/update"
                            element={<UserUpdate />}
                        ></Route>
                        <Route
                            path="/delete"
                            element={<UserDelete />}
                        ></Route>
                    </Routes>
                </div>
              </Router>
        );
    }
}

export default App;