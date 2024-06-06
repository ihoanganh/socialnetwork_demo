import React, {useState, useEffect} from "react";
import axios from "axios";
import {Button, message, Select} from "antd"; 

const { Option } = Select;

const PostGet = () => {
    const [posts, setPosts] = useState([]);

    useEffect(() => {
        const fetchPost =  async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/posts/');
                setPosts(response.data);
            } catch (error) {
                console.error("Error fetching post", error);
            }
        };
        fetchPost();
    }, []);

    return (
      <div>
      <h1>Post List</h1>
      <ul>
        {posts.map(post => (
          <li key={post.id}>
            <strong>Title:</strong> {post.title}, <strong>User ID:</strong> {post.user}, <strong>Published Date:</strong> {post.date}
          </li>
        ))}
      </ul>
    </div>
    )

};
export {PostGet};



const PostForm = () => {
  const [title, setTitle] = useState('');
  const [slug, setSlug] = useState('');
  const [user, setUser] = useState('');
  const handleSubmit = async (e) => {
      e.preventDefault();
      try {
          const response = await axios.post('http://127.0.0.1:8000/api/posts/', { title, slug,user });
          console.log('Post created:', response.data);
          // Thực hiện các hành động bổ sung sau khi tạo bài viết thành công
      } catch (error) {
          console.error('Error creating post:', error);
          // Xử lý lỗi nếu cần
      }
  };

  return (
      <form onSubmit={handleSubmit}>
          <div>
              <label htmlFor="title">Title:</label>
              <input
                  type="text"
                  id="title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
              />
          </div>
          <div>
              <label htmlFor="slug">Slug:</label>
              <textarea
                  id="slug"
                  value={slug}
                  onChange={(e) => setSlug(e.target.value)}
              />
          </div>
          <div>
              <label htmlFor="user">User:</label>
              <textarea
                  id="user"
                  value={user}
                  onChange={(e) => setUser(e.target.value)}
              />
          </div>
          <button type="submit">Create Post</button>
      </form>
  );
};

export {PostForm};


const PostUpdate = () => {
  const [posts, setPosts] = useState([]);
  const [id, setPostId] = useState();
  const [users, setUsers] = useState([]);
  const [userId, setUserId] = useState();
  const [title, setTitle] = useState('');
  const [slug, setSlug] = useState('');
  const [visibility, setVisibility] = useState('');
  const [active, setActive] = useState('');
  const [image, setImage] = useState(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/posts/');
        if (Array.isArray(response.data)) {
          setPosts(response.data);
        } else {
          console.error('Expected an array of posts');
        }
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    };

    fetchPosts();


    const fetchUsers = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/user/');
        if (Array.isArray(response.data)) {
          setUsers(response.data);
        } else {
          console.error('Expected an array of users');
        }
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };

    fetchUsers();
  }, []);
  const handleVisibilityChange = (e) => {
    setVisibility(e.target.value);
  };
  const handleActiveChange = (e) => {
    setActive(e.target.value);
  };
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setImage(selectedFile);
  };
  const handlePostSelect = async (postId) => {
    setPostId(postId)
    console.log(`Selected Post ID: ${postId}`);
  };
  const handleUserSelect = (userId) => {
    setUserId(userId);
    console.log(`Selected User ID: ${userId}`);
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('title', title);
    formData.append('slug', slug);
    formData.append('user', userId);
    formData.append('visibility', visibility);
    formData.append('active', active);
    if (image) {
      formData.append('image', image);
    }

    try {
      const response = await axios.put(`http://127.0.0.1:8000/api/posts/${id}/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('Post updated:', response.data);
    } catch (error) {
      console.error('Error updating post:', error);
    }
  };

  return (
      <form onSubmit={handleSubmit}>
        
        <div>
          <div>
            <label htmlFor="post">Select Post:</label>
            <select
              id="post"
              onChange={(e) => handlePostSelect(e.target.value)}
            >
              <option value="">Select a Post</option>
              {Array.isArray(posts) && posts.map(post => (
                <option key={post.id} value={post.id}>
                  {post.id}
                </option>
              ))}
            </select>
          </div>
          {id && (
            <div>
              <p>Selected Post ID: {id}</p>
            </div>
          )}
        </div>
        <div>
          <div>
            <label htmlFor="user">Select User:</label>
            <select id="user" onChange={(e) => handleUserSelect(e.target.value)}>
              <option value="">Select a user</option>
              {Array.isArray(users) && users.map(user => (
                <option key={user.id} value={user.id}>
                  {user.username}
                </option>
              ))}
            </select>
          </div>
        </div>
          <div>
              <label htmlFor="title">Title:</label>
              <textarea
                  id="title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
              />
          </div>
          <div>
              <label htmlFor="slug">Slug:</label>
              <textarea
                  id="slug"
                  value={slug}
                  onChange={(e) => setSlug(e.target.value)}
              />
          </div>
          <div>
              <label htmlFor="visibility">Visibility:</label>
              <select
              className="selectpicker mt-2 story"
              id="visibility"
              value={visibility}
              onChange={handleVisibilityChange}
            >
              <option value="Everyone">Everyone</option>
              <option value="Only Me">Only Me</option>
            </select>
          </div>
          <div>
              <label htmlFor="active">Active:</label>
              <select
              className="selectpicker mt-2 story"
              id="active"
              value={active}
              onChange={handleActiveChange}
            >
              <option value="True">True</option>
              <option value="False">False</option>
            </select>
          </div>
          <div>
            <label htmlFor="file">Image:</label>
            <input
              type="file"
              id="image"
              onChange={handleFileChange}
            />
          </div>
          <button type="submit">Update Post</button>
      </form>
  );
};
export {PostUpdate};


const PostDelete = () => {
  const [posts, setPosts] = useState([]);
  const [id, setPostId] = useState(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/posts/');
        if (Array.isArray(response.data)) {
          setPosts(response.data);
        } else {
          console.error('Expected an array of posts');
        }
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    };

    fetchPosts();
  }, []);

  const handDeletePost = async () => {
    
    if (!id) {
      message.error("Please select a post to delete")
      return;
    }

    try {
      const response = await axios.delete(`http://127.0.0.1:8000/api/posts/${id}/`);
      message.success("Post deleted successfully");
      console.log("Post deleted:", response.data);
      //loại bo bài viết đã bị xoá trong danh sách
      setPosts(posts.filter(post => post.id !== id))
      //đặt lại id thành null
      setPostId(null)
    } catch (error) {
      console.log('Error deleting post:', error);
      message.error('Failed to delete post.')
    }
  };
  return (
    
    <div>
      <div style={{ marginBottom: '16px' }}>
        <label htmlFor="post">Select Post:</label>
        <Select
          id="post"
          style={{ width: '200px' }}
          onChange={(value) => setPostId(value)}
          placeholder="Select a Post"
        >
          {posts.map(post => (
            <Option key={post.id} value={post.id}>{post.id}</Option>
          ))}
        </Select>
      </div>
      {id && (
        <div style={{ marginBottom: '16px' }}>
          <p>Selected Post ID: {id}</p>
        </div>
      )}
      <Button type="primary" danger onClick={handDeletePost}>Delete Post</Button>
    </div>
  )
};


export {PostDelete}