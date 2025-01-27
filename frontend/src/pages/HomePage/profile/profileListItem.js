import * as React from 'react';
import { ListItemButton, Avatar, ListItemText, ListItemAvatar } from '@mui/material';
import DeleteFollowingDialog from './deleteFollowingDialog';
import { useDispatch } from 'react-redux';
import { useState } from 'react';
import { pushToInbox } from '../../../redux/inboxSlice';
import PrivatePostDialog from '../createPost/PrivatePostDialog';
import FollowRequestDialog from '../../../Components/FollowRequestDialog';

export default function ProfileListItem({type, author, profile, removeProfile, alertError, alertSuccess}) {

    const dispatch = useDispatch();

    const [open, setOpen] = useState(false);
    const handleOpen = () => setOpen(true);
    const handleClose = () => setOpen(false);

    const [openPostDialog, setOpenPostDialog] = React.useState(false);
    const handleClickOpen = () => setOpenPostDialog(true); 
    const handleClickClose = () =>  setOpenPostDialog(false);

    const [openFollowDialog, setOpenFollowDialog] = React.useState(false);
    const clickOpenFollowDialog = () => { setOpenFollowDialog(true); console.log("HASDOINOINOIN") }
    const closeFollowDialog = () =>  setOpenFollowDialog(false);
    
    /* Add A New Item To The Inbox */
    const addToFeed = item => dispatch(pushToInbox(item));

    return (
        <div>
            <ListItemButton sx={{ pl: 3 }} onClick={type === "friends" ? handleClickOpen : (type === "authors" ? clickOpenFollowDialog : handleOpen)}>
                <ListItemAvatar>
                    <Avatar alt={profile.displayName} src={profile.profileImage} />
                </ListItemAvatar>
                <ListItemText primary={profile.displayName} />
            </ListItemButton>
            {type === "following" && <DeleteFollowingDialog author={author} following={profile} alertSuccess={alertSuccess} alertError={alertError} open={open} handleClose={handleClose} removeFollowing={removeProfile} />}
            {type === "friends" && <PrivatePostDialog recipient={profile} open={openPostDialog} profile={author} onClose={handleClickClose} alertError={alertError} alertSuccess={alertSuccess} addToFeed={addToFeed} />}
            {type === "authors" && <FollowRequestDialog  authorToFollow={profile} alertSuccess={alertSuccess} alertError={alertError} open={openFollowDialog} handleClose={closeFollowDialog} />}
        </div>
    );
}