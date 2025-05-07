import '@mantine/core/styles.css';

import { MantineProvider} from '@mantine/core';
import Welcome from './components/welcome';
import Home from './pages/home';
import About from './pages/about';

import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Profile from './pages/profile';
import Login from './pages/login';

function App() {

  return (
    <MantineProvider>
      <Router>
        <Link to='/' style={{marginRight: 20}}>Home</Link>
        <Link to='/profile' style={{marginRight: 20}}>Profile</Link>
        <Link to='/about' style={{marginRight: 20}}>About</Link>
        <Link to='/login'>Login</Link>
        {/* <Welcome /> */}
        
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/profile' element={<Profile />} />
          <Route path='/about' element={<About />} />
          <Route path='/login' element={<Login />} />
        </Routes>
      </Router>
    </MantineProvider>
  )
}

export default App
