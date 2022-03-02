import * as React from 'react';
import CreatePost from './createPost/CreatePost';
import ProfileSection from './profile/profileSection';
import FeedCard from './mainFeed/FeedCard';
import LogoutIcon from '@mui/icons-material/Logout';
import axios from 'axios';
import Tab from '@mui/material/Tab';
import TabContext from '@mui/lab/TabContext';
import TabList from '@mui/lab/TabList';
import TabPanel from '@mui/lab/TabPanel';
import { useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { getInbox } from '../../services/posts';
import { useState, useEffect } from 'react';
import { logout } from '../../redux/profileSlice';
import { set, concat, findIndex } from 'lodash/fp';
import { Alert, Snackbar, Drawer, Box, AppBar, Toolbar, Typography, Divider, Paper, IconButton, Grid } from '@mui/material';


const drawerWidth = 400;


export default function HomePage() {

    /* Redux Dispatcher */
    const dispatch = useDispatch();

    /* State Hook For Tab Values */
    const [value, setValue] = React.useState('1');

    /* State Hook For Displaying Alerts */
    const [openAlert, setOpenAlert] = useState({isOpen: false, message: "", severity: "error"})
    const alertSuccess = msg => setOpenAlert({isOpen: true, message: msg, severity: "success"})
    const alertError = msg => setOpenAlert({isOpen: true, message: msg, severity: "error"})
    const handleCloseAlert = () => setOpenAlert(set('isOpen', false, openAlert));

    /* A State Hook For Storing The Window Width */
    const [windowWidth, setWindowWidth] = useState(window.innerWidth)

    /* State Hook For Inbox */
    const [inbox, setInbox] = useState([]);
    const addToFeed = item => setInbox(concat([item])(inbox));
    const removeFromFeed = item => setInbox(inbox.filter( x => x.id !== item.id));
    const updateFeed = (item) => {
        const index = findIndex(x => x.id === item.id)(inbox);
        setInbox(inbox.map((x, i) => i === index ? item : x));
    }

    /* Hook handle function for Tab values */
    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    /* State Hook For Inbox */
    const userID = useSelector( state => state.profile.url );


    /* We Use This To Listen To Changes In The Window Size */
    useEffect( () => { 
        const windowResizeCallback = () => { setWindowWidth(window.innerWidth) };
        window.addEventListener('resize', windowResizeCallback);
        return () => { window.removeEventListener('resize', windowResizeCallback) };
     });

    
    const navigate = useNavigate();
    

    /* Hook For Navigating To The Home Page */
    const goToLogin = () => navigate("/login/")


    /* Logout Functionality */
    const onLogout = () => {
      axios.post("/api/authors/logout/", {}, {headers: {"Authorization": "Token " + localStorage.getItem("token")}})
        .then( _ => {
            dispatch(logout());
            goToLogin();
         } )
        .catch( err => console.log(err) );
    }

    /* Get Inbox From Server */
    useEffect( () => {
        getInbox(userID)
            .then( res => setInbox(res.data.items) )
            .catch( err => console.log(err) )
            .finally( () => console.log(inbox) )
    }, [] );

    

    
    

  return (
    <Box sx={{ display: 'flex', paddingTop: "50px" }}>
        <Snackbar
            sx={{width: "60%", pt:6}} spacing={2}
            anchorOrigin={{horizontal: "center", vertical: "top"}}
            open={openAlert.isOpen}
            autoHideDuration={2500}
            onClose={handleCloseAlert}>
            <Alert severity={openAlert.severity}>{openAlert.message}</Alert>
        </Snackbar>
        <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
            <Toolbar sx={{ flexWrap: 'wrap' }}>
            <Typography variant="h5" noWrap component="div"> Social Distribution </Typography>
            <IconButton
                onClick={onLogout}
                id="account-icon"
                size="large"
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                color="inherit"
                sx={{marginLeft: "auto"}} >
                <LogoutIcon sx={{ fontSize: "36px" }}/>
            </IconButton>
            </Toolbar>
        </AppBar>
        <Drawer
            sx={{ width: drawerWidth, flexShrink: 0, '& .MuiDrawer-paper': { width: drawerWidth, boxSizing: 'border-box', }, }}
            variant="permanent"
            anchor="left" >
            <Toolbar />
            <Divider />
            <ProfileSection alertSuccess={alertSuccess} alertError={alertError} /> 
        </Drawer>
        <Box component="main" sx={{ flexGrow: 1, p: 0, marginTop: "15px", width: (windowWidth - drawerWidth) + "px"}}>
            <CreatePost alertSuccess={alertSuccess} alertError={alertError} addToFeed={addToFeed} />
            
            <Box sx={{ width: '100%', typography: 'body1' }}>
                <TabContext value={value}>
                    <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                    <TabList onChange={handleChange} aria-label="lab API tabs example" centered>
                        <Tab label="Main Stream" value="1" />
                        <Tab label="My Stream" value="2" />
                        <Tab label="Github Activity" value="3" />
                    </TabList>
                    </Box>
                    <TabPanel value="1">
                        <Paper sx={{p:0}}>
                            {inbox.map((post) => (
                                post.unlisted === false ?
                                (<Grid item xs={12}> 
                                    <FeedCard post={post} isOwner={post.author.id === userID} fullWidth={true} alertError={alertError} alertSuccess={alertSuccess} updateFeed={updateFeed} removeFromFeed={removeFromFeed} /> 
                                </Grid>): null
                            ))}
                        </Paper>
                    </TabPanel>
                    <TabPanel value="2">
                        <Paper sx={{p:0}}>
                            {inbox.map((post) => (
                                post.author.id === userID ?
                                (<Grid item xs={12}> 
                                    <FeedCard post={post} isOwner={post.author.id === userID} fullWidth={true} alertError={alertError} alertSuccess={alertSuccess} updateFeed={updateFeed} removeFromFeed={removeFromFeed} /> 
                                </Grid>): null
                            ))}
                        </Paper>
                    </TabPanel>
                    <TabPanel value="3">
                        Item Three
                    </TabPanel>
                </TabContext>
            </Box>
            


            

        </Box>
    </Box>
  );
}