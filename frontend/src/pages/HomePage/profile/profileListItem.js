import * as React from 'react';
import { ListItemButton, Avatar, ListItemText, ListItemAvatar } from '@mui/material';

export default function ProfileListItem(props) {
    return (
        <ListItemButton sx={{ pl: 3 }}>
            <ListItemAvatar>
                <Avatar alt={props.displayName} src={props.profileImage} />
            </ListItemAvatar>
            <ListItemText primary={props.displayName} />
        </ListItemButton>
    );
}