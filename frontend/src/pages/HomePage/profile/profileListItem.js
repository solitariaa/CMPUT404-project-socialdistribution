import * as React from 'react';
import { useState } from 'react';
import { ListItemButton, Avatar, ListItemText, ListItemAvatar, ListItem } from '@mui/material';
import ProfilePrivateMessage from './profilePrivateMessage';
import { set, concat } from 'lodash/fp';
import Box from '@mui/material/Box';
import { setInboxInStorage, getInboxFromStorage } from '../../../LocalStorage/inbox';
import { getAuthorFromStorage, setAuthorInStorage  } from '../../../LocalStorage/profile';
import DeleteFollowingDialog from './deleteFollowingDialog';
import { useSelector } from 'react-redux';
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
import IconButton from '@mui/material/IconButton';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import MoreVertIcon from '@mui/icons-material/MoreVert';


export default function ProfileListItem({type, author, profile, removeProfile, alertError, alertSuccess, addToFeed}) {
    const [open, setOpen] = React.useState(false);
    const [anchorEl, setAnchorEl] = React.useState(null);
    const [appear, setAppear] = React.useState(false);

    const openMenu = Boolean(anchorEl);
    const handleMenuClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    const handleMenuClose = () => {
        setAnchorEl(null);
    };
    const handleUnfollowOpen = () => {
        setOpen(true);
    };
    const handleClose = () => {
        setOpen(false);
    };
    const appearClose = () => {
        setAppear(false);
    };
    const handleSendClick = () => {
      setAppear(true);
    };


    return (
        <Box>
        <ListItem sx={{ pl: 4 }} >
            <ListItemAvatar>
                <Avatar alt={profile.displayName} src={profile.profileImage} />
            </ListItemAvatar>
            <ListItemText primary={profile.displayName} />
            <IconButton
                aria-label="more"
                id="long-button"
                aria-controls={openMenu ? 'long-menu' : undefined}
                aria-expanded={openMenu ? 'true' : undefined}
                aria-haspopup="true"
                onClick={handleMenuClick}
            >
                <MoreVertIcon />
            </IconButton>
            <Menu
                id="long-menu"
                MenuListProps={{
                'aria-labelledby': 'long-button',
                }}
                anchorEl={anchorEl}
                open={openMenu}
                onClose={handleMenuClose}
                PaperProps={{
                style: {
                    maxHeight: 100,
                    width: '20ch',
                },
                }}
            >
                <MenuItem key={"CRPost"} onClick={handleSendClick}>
                    Send Post
                </MenuItem>
                {type === "following" && <MenuItem key={"IMGPost"} onClick={handleUnfollowOpen}>
                    Unfollow
                </MenuItem>}
            </Menu>
        </ListItem>
        <ProfilePrivateMessage open={appear} onClose={appearClose} profile={profile} alertError={alertError} alertSuccess={alertSuccess} addToFeed={addToFeed} />
        {type === "following" && <DeleteFollowingDialog author={author} following={profile} alertSuccess={alertSuccess} alertError={alertError} open={open} handleClose={handleClose} removeFollowing={removeProfile}/>}
        </Box>
        );
    }

        