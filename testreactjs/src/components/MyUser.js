import React, {useEffect, useState} from "react";
import axios from "axios";
import { message, Select, Button } from "antd";
import './MyUser.css'
const { Option } = Select
// const UserGet = () => {
//     const [users, setUsers] = useState([])

//     useEffect (() => {
//         const fetchUser = async () => {
//             try {
//                 const response = await axios.get(`http://127.0.0.1:8000/api/user/`)
//                 setUsers(response.data)
//             } catch (error){
//                 console.error("Error fetching user ", error);
//             }
//         }
//         fetchUser()
//     }, [])

//     return (
//         <div className="GetUser"> 
//             <ul>
//                 {users.map(user => (
//                     <><hr></hr><li key={user.id}>
//                         {user.username && (
//                             <div>
//                                 <strong>Username:</strong> {user.username}
//                             </div>
//                         )}
//                         {user.full_name && (
//                             <div>
//                                 <strong>Full name:</strong> {user.full_name}
//                             </div>
//                         )}
//                         {user.email && (
//                             <div>
//                                 <strong>Email:</strong> {user.email}
//                             </div>
//                         )}
//                         {user.gender && (
//                             <div>
//                                 <strong>Gender:</strong> {user.gender}
//                             </div>
//                         )}
//                     </li></>
//                 ))}
                
//             </ul>
            
//         </div>
//     )
// }
const UserGet = () => {
    const [users, setUsers] = useState([]);
    const [searchId, setSearchId] = useState('');
    const [showUsers, setShowUsers] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');

    const fetchUsers = async (id = '') => {
        try {
            const url = id ? `http://127.0.0.1:8000/api/user/${id}/` : `http://127.0.0.1:8000/api/user/`;
            const response = await axios.get(url);
            setUsers(id ? [response.data] : response.data);
            setShowUsers(true);
            setErrorMessage('');
        } catch (error) {
            console.error("Error fetching users: ", error);
            setUsers([]);
            setShowUsers(false);
            setErrorMessage('ID không tồn tại. Vui lòng nhập lại.');
        }
    };

   

    const handleSearch = (e) => {
        e.preventDefault();
        if (searchId.trim() === '') {
            setErrorMessage('Vui lòng nhập ID hợp lệ.');
            setShowUsers(false);
            return;
        }
        fetchUsers(searchId);
    };

    return (
        <div className="GetUser">
            <form onSubmit={handleSearch}>
                <div>
                    <label htmlFor="searchId">User ID:</label>
                    <input
                        type="text"
                        id="searchId"
                        value={searchId}
                        onChange={(e) => setSearchId(e.target.value)}
                    />
                    <button type="submit">Search</button>
                    <button type="submit" onClick={() => fetchUsers()}>Get All</button>
                </div>
            </form>
            {errorMessage && <div className="error-message">{errorMessage}</div>}
            {showUsers && (
                <ul>
                    {users.map(user => (
                        <React.Fragment key={user.id}>
                            <hr />
                            <li>
                                {user.username && (
                                    <div className="form__row">
                                        <strong className="label">Username:</strong> {user.username}
                                    </div>
                                )}
                                {user.full_name && (
                                    <div className="form__row">
                                        <strong className="label">Full name:</strong> {user.full_name}
                                    </div>
                                )}
                                {user.email && (
                                    <div className="form__row">
                                        <strong className="label">Email:</strong> {user.email}
                                    </div>
                                )}
                                {user.gender && (
                                    <div className="form__row">
                                        <strong>Gender:</strong> {user.gender}
                                    </div>
                                )}
                            </li>
                        </React.Fragment>
                    ))}
                </ul>
            )}
        </div>
    );
};
export {UserGet}


const UserPost = () => {
    const [password, setPassword] = useState('')
    const [full_name, setFullname] = useState('')
    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [phone, setPhone] = useState(null)
    const [gender, setGender] = useState('')

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/user/',
            {password, full_name, username, email, phone, gender})
            message.success(`Created user ${response.data.full_name} successfully`)
            console.log("Post created", response.data);
        } catch (error){
            console.log("Error creating post: ", error);
        }
    }
    const handleGenderChange = (e) => {
        setGender(e.target.value)
        console.log("Gender selected:", e.target.value);
    }
    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="password">Password:</label>
                <input 
                    type="password" 
                    id="password" 
                    value={password} 
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
            </div>
            <div>
                <label htmlFor="full_name">Full name:</label>
                <input 
                    type="text" 
                    id="full_name" 
                    value={full_name} 
                    onChange={(e) => setFullname(e.target.value)}
                    required
                />
            </div>
            <div>
                <label htmlFor="username">Username:</label>
                <input 
                    type="text" 
                    id="username" 
                    value={username} 
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
            </div>
            <div>
                <label htmlFor="email">Email:</label>
                <input 
                    type="text" 
                    id="email" 
                    value={email} 
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
            </div>
            <div>
                <label htmlFor="phone">Phone:</label>
                <input 
                    type="number" 
                    id="phone" 
                    value={phone} 
                    onChange={(e) => setPhone(e.target.value)}
                    required
                />
            </div>
            <div>
              <label htmlFor="gender">Gender:</label>
              <select
              className="selectpicker mt-2 story"
              id="gender"
              value={gender}
              onChange={handleGenderChange}
            >
              <option value="True">Male</option>
              <option value="False">Female</option>
            </select>
          </div>
          <button type="submit">Create User</button>
        </form>
    )
}
export {UserPost}

// const UserUpdate = () => {
//     const [users, setUsers] = useState([]);
//     const [userId, setUserId] = useState();
//     const [password, setPassword] = useState('')
//     const [full_name, setFullname] = useState('')
//     const [username, setUsername] = useState('')
//     const [email, setEmail] = useState('')
//     const [phone, setPhone] = useState('')
//     const [gender, setGender] = useState('')

//     useEffect(() => {
//         const fetchUsers = async () => {
//             try {
//               const response = await axios.get('http://127.0.0.1:8000/api/user/');
//               if (Array.isArray(response.data)) {
//                 setUsers(response.data);
//               } else {
//                 console.error('Expected an array of users');
//               }
//             } catch (error) {
//               console.error('Error fetching users:', error);
//             }
//           };
      
//           fetchUsers();
//         }, []);

//         const handleUserSelect = (userId) => {
//             setUserId(userId);
//             console.log(`Selected User ID: ${userId}`);
//         };
//         const handleGenderChange = (e) => {
//             setGender(e.target.value)
//         }

//         const handleSubmit = async (e) => {
//             e.preventDefault()
//             const formData = new FormData()
//             formData.append('password', password)
//             formData.append('full_name', full_name)
//             formData.append('username', username)
//             formData.append('email', email)
//             formData.append('phonegender', phone)
//             formData.append('gender', gender)

//             try {
//                 const response = await axios.put(`http://127.0.0.1:8000/api/user/${userId}/`, formData, {
//                   headers: {
//                     'Content-Type': 'multipart/form-data',
//                   },
//                 });
//                 console.log('User updated:', response.data);
//               } catch (error) {
//                 console.error('Error updating user:', error);
//               }
//         }
        
//         return (
//         <form onSubmit={handleSubmit}>
//             <div>
//               <div>
//                 <label htmlFor="user">Select User:</label>
//                 <select id='user' onChange={(e)=> handleUserSelect(e.target.value)}>
//                   <option value="">Select a User</option>
//                   {Array.isArray(users) && users.map(user => (
//                   <option key={user.id} value={user.id}>{user.id}</option>
//                   ))}
//                 </select>
//               </div>
//               {userId && (
//               <div>
//                 <p>Selected User ID: {userId}</p>
//               </div>
//               )}
//             </div>
//             <div>
//               <label htmlFor="password">Password:</label>
//               <input type="password" id="password" value={password} onChange={(e)=> setPassword(e.target.value)}
//               />
//             </div>
//             <div>
//               <label htmlFor="full_name">Full name:</label>
//               <input type="text" id="full_name" value={full_name} onChange={(e)=> setFullname(e.target.value)}
//               />
//             </div>
//             <div>
//               <label htmlFor="username">Username:</label>
//               <input type="text" id="username" value={username} onChange={(e)=> setUsername(e.target.value)}
//               />
//             </div>
//             <div>
//               <label htmlFor="email">Email:</label>
//               <input type="text" id="email" value={email} onChange={(e)=> setEmail(e.target.value)}
//               />
//             </div>
//             <div>
//               <label htmlFor="phone">Phone:</label>
//               <input type="number" id="phone" value={phone} onChange={(e)=> setPhone(e.target.value)}
//               />
//             </div>
//             <div>
//               <label htmlFor="gender">Gender:</label>
//               <select className="selectpicker mt-2 story" id="gender" value={gender} onChange={handleGenderChange}>
//                 <option value="True">Male</option>
//                 <option value="False">Female</option>
//               </select>
//             </div>
//             <button type="submit">Update User</button>
          
//         </form>
//         )
// }
// export {UserUpdate}
const UserUpdate = () => {
    const [users, setUsers] = useState([]);
    const [userId, setUserId] = useState(null);
    const [password, setPassword] = useState(null);
    const [full_name, setFullname] = useState(null);
    const [username, setUsername] = useState(null);
    const [email, setEmail] = useState(null);
    const [phone, setPhone] = useState(null);
    const [gender, setGender] = useState(null);

    useEffect(() => {
        // Fetch users from API
        const fetchUsers = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/user/');
                setUsers(response.data);
            } catch (error) {
                console.log('Error fetching users: ', error);
            }
        };
        fetchUsers();
    }, []);

    const handleUserSelect = async (id) => {
        setUserId(id);
        if (id) {
            try {
                const response = await axios.get(`http://127.0.0.1:8000/api/user/${id}/`);
                const user = response.data;
                setPassword(user.password || '');
                setFullname(user.full_name || '');
                setUsername(user.username || '');
                setEmail(user.email || '');
                setPhone(user.phone || null);  // Allow null value
                setGender(user.gender || '');
            } catch (error) {
                console.log('Error fetching user: ', error);
            }
        } else {
            // Clear form if no user is selected
            setPassword(null);
            setFullname(null);
            setUsername(null);
            setEmail(null);
            setPhone(null);
            setGender(null);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.put(`http://127.0.0.1:8000/api/user/${userId}/`, {
                password, full_name, username, email, phone, gender
            });
            console.log('User updated', response.data);
            message.success(`Update ${response.data.full_name} successfully`)
        } catch (error) {
            console.log('Error updating user: ', error.response ? error.response.data : error.message);
        }
    };

    const handleGenderChange = (e) => {
        setGender(e.target.value);
        console.log('Gender selected:', e.target.value);
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="user">Select User:</label>
                <select id="user" onChange={(e) => handleUserSelect(e.target.value)}>
                    <option value="">Select a User</option>
                    {Array.isArray(users) && users.map(user => (
                        <option key={user.id} value={user.id}>{user.id}</option>
                    ))}
                </select>
            </div>
            {userId && (
                <div>
                    <p>Selected User ID: {userId}</p>
                </div>
            )}
            <div>
                <label htmlFor="password">Password:</label>
                <input
                    type="text"
                    id="password"
                    value={password || ''}
                    onChange={(e) => setPassword(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="full_name">Full name:</label>
                <input
                    type="text"
                    id="full_name"
                    value={full_name || ''}
                    onChange={(e) => setFullname(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="username">Username:</label>
                <input
                    type="text"
                    id="username"
                    value={username || ''}
                    onChange={(e) => setUsername(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="email">Email:</label>
                <input
                    type="text"
                    id="email"
                    value={email || ''}
                    onChange={(e) => setEmail(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="phone">Phone:</label>
                <input
                    type="number"
                    id="phone"
                    value={phone !== null ? phone : ''}
                    onChange={(e) => setPhone(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="gender">Gender:</label>
                <select
                    className="selectpicker mt-2 story"
                    id="gender"
                    value={gender || ''}
                    onChange={handleGenderChange}
                >
                    <option value="">Select Gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                </select>
            </div>
            <button type="submit">Update User</button>
        </form>
    );
};

export { UserUpdate };


const UserDelete= () => {
    const [users, setUsers] = useState([])
    const [userid, setUserid] = useState(null)

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/user/')
                if(Array.isArray(response.data)) {
                    setUsers(response.data)
                } else {
                    console.error("Expected an array of users");
                }
            } catch (error) {
                console.error("Error fetching users: ", error);
            }
        }

        fetchUser()
    }, [])

    const handleDeleteUser = async () => {
        if(!userid) {
            message.warning("Please select a user to delete")
            return
        }

        try {
            const response = await axios.delete(`http://127.0.0.1:8000/api/user/${userid}/`)
            message.success("User deleted successfully");
            console.log("User deleted:", response.data);
            setUsers(users.filter(user => user.id !== userid))
            setUserid(null)
        } catch (error){
            console.log('Error deleting user:', error);
            message.error('Failed to delete user.')
        }
    }
    return (
        <form>
      <div style={{ marginBottom: '16px' }}>
        <label htmlFor="user">Select User:</label>
        <Select
          id="user"
          style={{ width: '200px' }}
          onChange={(value) => setUserid(value)}
          placeholder="Select a Post"
        >
          {users.map(user => (
            <Option key={user.id} value={user.id}>{user.id}</Option>
          ))}
        </Select>
      </div>
      {userid && (
        <div style={{ marginBottom: '16px' }}>
          <p>Selected Post ID: {userid}</p>
        </div>
      )}
      <Button type="primary" danger onClick={handleDeleteUser}>Delete Post</Button>
    </form>
    )
}
export {UserDelete}