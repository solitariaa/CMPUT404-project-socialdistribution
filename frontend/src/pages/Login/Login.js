import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Snackbar from '@mui/material/Snackbar';
import { Alert } from '@mui/material';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import axios from 'axios';
import { set } from 'lodash/fp';
import { useNavigate } from 'react-router-dom';
import {  useDispatch } from 'react-redux';
import { login } from '../../redux/profileSlice';
import { setInbox } from '../../redux/inboxSlice';
import { getFollowers, getFollowing } from '../../services/followers';
import { getInbox } from '../../services/posts';
import { setAuthorInStorage, getAuthorFromStorage } from '../../LocalStorage/profile';
import { setInboxInStorage, getInboxFromStorage } from '../../LocalStorage/inbox';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { setFollowers } from '../../redux/followersSlice';
import { setFollowing } from '../../redux/followingsSlice'

function Copyright(props) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © Social Distribution ' + new Date().getFullYear()}
    </Typography>
  );
}

export default function LoginPage() {

  /* Hook For Navigating To The Home Page */
  const navigate = useNavigate();
  const goToHome = () => navigate("/homepage")

  const [openAlert, setOpenAlert] = React.useState({isOpen: false, message: "", severity: "error"})
  const showError = msg => setOpenAlert({isOpen: true, message: msg, severity: "error"})
  const handleCloseAlert = () => setOpenAlert(set('isOpen', false, openAlert));

  const dispatch = useDispatch();

  /* Callback For Logging In The User */
  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    /* Authenticate */
    if (data.get("password") && data.get("displayName")) {
      axios.post("/api/authors/login/", data)
        .then((res) => {

          /* Set User Credentials */
          dispatch(login(res.data.author));
          setAuthorInStorage(res.data.author);
          localStorage.setItem("token", res.data.token);
          console.log(getAuthorFromStorage());

          Promise.all([getInbox(res.data.author.url), getFollowers(res.data.author.url), getFollowing(res.data.author.url)])
            .then( values => {
              console.log(values[0].data);
              console.log(values[1].data);
              console.log(values[2].data);
              setInboxInStorage(values[0].data.items);
              dispatch(setFollowers(values[1].data.items));
              dispatch(setFollowing(values[2].data.items));
              goToHome();
          })
        })
        .catch( err => showError(err.response.data.error ? err.response.data.error : "Error Logging In!") );
    } else {
      showError("Username And Password Required!")
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: "center", height: "100vh"}}>
      <Snackbar
        sx={{width: "60%", pt:6}} spacing={2}
        anchorOrigin={{horizontal: "center", vertical: "top"}}
        open={openAlert.isOpen}
        autoHideDuration={2500}
        onClose={handleCloseAlert}>
        <Alert severity={openAlert.severity}>{openAlert.message}</Alert>
      </Snackbar>
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', maxWidth: "400px" }} >
        <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}> <LockOutlinedIcon /> </Avatar>
        <Typography component="h1" variant="h5"> Sign In </Typography>
        <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                name="displayName"
                required
                fullWidth
                id="displayName"
                label="Username"
                autoFocus
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="new-password"
              />
            </Grid>
          </Grid>
          <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }} > Sign In </Button>
          <Grid container justifyContent="center">
            <Grid item>
              <Link href="#/register" variant="body2"> New user? Create an account </Link>
            </Grid>
          </Grid>
        </Box>
      </Box>
      <span style={{position: "absolute", bottom: "35px"}}>
        <Copyright sx={{marginTop: "100px"}} />
      </span>
    </div>
  );
}