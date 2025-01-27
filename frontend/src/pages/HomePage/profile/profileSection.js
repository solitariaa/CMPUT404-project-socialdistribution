import * as React from 'react';
import Paper from '@mui/material/Paper';
import { Avatar, Typography, Box, Grid, Link, CardHeader, CardContent, IconButton, ListItemButton, Divider } from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import EditIcon from '@mui/icons-material/Edit'
import ProfileEditModal from './profileEditModal';
import ProfileList from './ProfileList';
import { intersectionBy } from 'lodash/fp';
import { removeFollowing as removeFollowingReducer } from "../../../redux/followingsSlice"



export default function ProfileSection({alertError, alertSuccess}) {
  const [isModalOpen, setOpen] = React.useState(false);

  const dispatch = useDispatch();

  /* Hook For Author */
  const author = useSelector(state => state.profile);

  /* Hook For Followers */
  const followers = useSelector(state => state.followers.items);

  /* Hook For Following */
  const following = useSelector(state => state.following.items);
  const removeFollowing = (following) => dispatch(removeFollowingReducer(following));

  /* Hook For All Users */
  const allUsers = useSelector(state => state.users.items);

  const handleModalOpen = () => setOpen(true);
  const handleModalClose = () => setOpen(false);

  const user_id = useSelector(state => state.profile.id);
  const displayName = useSelector(state => state.profile.displayName);
  const github = useSelector(state => state.profile.github);
  const profileImage = useSelector(state => state.profile.profileImage);
  const userURL = useSelector(state => state.profile.url);

  const style = {
    editIcon: {
      position: 'absolute',
      right: 10,
      top: 10

    }
  };

  return (
    <Paper component="main" sx={{ display: 'flex', overflow: 'visible', flexDirection: 'column', evaluation: 2, border: '1px solid lightgrey', boxShadow: 1, borderRadius: 1, }} >

      <Box sx={{ position: 'relative', padding: "25px 0 20px 0", display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: "center" }} >
        <IconButton aria-label="settings" onClick={handleModalOpen} sx={style.editIcon}>
          <EditIcon />
        </IconButton>
        <Avatar src={author.profileImage} sx={{ width: "100px", height: "100px" }} />
        <Typography variant='h5' sx={{ padding: "10px" }}>{displayName}</Typography>
        <Typography variant='subtitle1'>{github}</Typography>
      </Box>
      <Divider />
      <ProfileList type="friends" profiles={intersectionBy(x => x["id"])(following)(followers)} title="Friends" author={author} removeProfile={removeFollowing} alertError={alertError} alertSuccess={alertSuccess} />
      <Divider />
      <ProfileList type="following" profiles={following} title="Following" author={author} removeProfile={removeFollowing} alertError={alertError} alertSuccess={alertSuccess} />
      <Divider />
      <ProfileList type="followers" title='Followers' profiles={followers} alertError={alertError} alertSuccess={alertSuccess} />
      <Divider />
      <ProfileList type="authors" title='Authors' profiles={allUsers} alertError={alertError} alertSuccess={alertSuccess} />

      <ProfileEditModal alertSuccess={alertSuccess} isOpen={isModalOpen} onClose={handleModalClose} />
    </Paper >
  );
}