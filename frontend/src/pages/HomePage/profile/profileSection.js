import * as React from 'react';
import Paper from '@mui/material/Paper';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';
import { Avatar, Container, Typography, Box, Grid, Link, CardHeader, CardContent, IconButton, ListItemButton } from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import EditIcon from '@mui/icons-material/Edit'
import ProfileEditModal from './profileEditModal';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import ProfileList from './profileList'



export default function ProfileSection(props) {
  const [isModalOpen, setOpen] = React.useState(false);
  const [isFollowingOpen, setFollowingOpen] = React.useState(true);
  const [isFollowerOpen, setFollowerOpen] = React.useState(true);
  const handleFollowing = () => {
    setFollowingOpen(!isFollowingOpen);
  };
  const handleFollower = () => {
    setFollowerOpen(!isFollowerOpen);
  };

  const handleModalOpen = () => setOpen(true);
  const handleModalClose = () => setOpen(false);

  const user_id = useSelector(state => state.profile.id);
  const displayName = useSelector(state => state.profile.displayName);
  const github = useSelector(state => state.profile.github);
  const profileImage = useSelector(state => state.profile.profileImage);
  const userURL = useSelector(state => state.profile.url);
  const testingProfiles = Array(10).fill(null).map((e, i) => ({ userName: 'User ' + (i + 1), profileImage: profileImage }));

  const style = {
    editIcon: {
      position: 'absolute',
      right: 10,
      top: 10

    }
  };

  return (
    // <Paper component="main" sx={{display: 'flex', minHeight: "100vh", flexDirection: 'column', evaluation: 2, border: '1px solid lightgrey', boxShadow: 1, borderRadius: 1, }} >
    //   <Box sx={{ padding: "45px 0 25px 0", display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: "center" }}>
    //     <Avatar src={profileImage} sx={{ width: "100px", height: "100px" }} />
    //     <Typography variant='h4' sx={{padding: "15px"}}>{displayName}</Typography>
    //     <Typography variant='subtitle1'>{github}</Typography>
    //   </Box>
    // </Paper>

    <Paper component="main" sx={{ display: 'flex', overflow: 'visible', flexDirection: 'column', evaluation: 2, border: '1px solid lightgrey', boxShadow: 1, borderRadius: 1, }} >

      <Box sx={{ position: 'relative', padding: "25px 0 20px 0", display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: "center" }} >
        <IconButton aria-label="settings" onClick={handleModalOpen} sx={style.editIcon}>
          <EditIcon />
        </IconButton>
        <Avatar src={profileImage} sx={{ width: "100px", height: "100px" }} />
        <Typography variant='h5' sx={{ padding: "10px" }}>{displayName}</Typography>
        <Typography variant='subtitle1'>{github}</Typography>
      </Box>

      {/* Old following section */}
      {/* <CardContent>
        <Grid container sx={{ alignItems: 'center', justifyContent: "center" }} spacing={2}>
          <Grid item><Link onClick={handleModalOpen} href='#' underline='none'>15</Link> following</Grid>
          <Grid item><Link onClick={handleModalOpen} href='#' underline='none'>30</Link> followers</Grid>
        </Grid>
      </CardContent> */}

      <Divider />
      <ProfileList title='Following' profiles={testingProfiles} handleCollapse={handleFollowing} isListOpen={isFollowingOpen} />
      <Divider />
      <ProfileList title='Followers' profiles={testingProfiles} handleCollapse={handleFollowing} isListOpen={isFollowingOpen} />

      <ProfileEditModal alertSuccess={props.alertSuccess} isOpen={isModalOpen} onClose={handleModalClose} />
    </Paper >
  );
}
