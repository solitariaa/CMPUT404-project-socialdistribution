import * as React from 'react';
import { ListItemButton, Avatar, ListItemText, ListItemAvatar, Collapse, Divider, List, ListItemIcon, Typography } from '@mui/material';
import ProfileListItem from './profileListItem';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import { useSelector, useDispatch } from 'react-redux';
import { width } from '@mui/system';

export default function ProfileList(props) {
    const showingCount = 5;
    const profileImage = useSelector(state => state.profile.profileImage);

    const handleCollapse = () => {
        return (<Collapse in={props.isListOpen} timeout="auto" unmountOnExit>
            <List style={style.list} component="div" disablePadding>
                {props.profiles.slice(showingCount).map((profile, index) => (
                    <ProfileListItem key={index} displayName={profile.userName} profileImage={profile.profileImage} />
                ))}
            </List>
        </Collapse>
        )
    }

    const style = {
        title: {
            pl: 2,
            textTransform: 'uppercase',
            justifyContent: 'center',
            alignItems: 'center'
        },
        count: {
            display: 'inline',
            ml: 1,
        },
        listHeader: {
            // background: '#f5f5f5'
        },
        expendIcon: {
            width: 40
        }
    };

    return (
        <List>
            <ListItemText sx={style.title}>{props.title}
                <Typography sx={style.count}>{props.profiles.length}</Typography>
            </ListItemText>
            {props.profiles.slice(0, showingCount).map((profile, index) => (
                <ProfileListItem key={index} displayName={profile.userName} profileImage={profile.profileImage} />))}

            {props.profiles.length > showingCount && handleCollapse()}
            <ListItemButton onClick={props.handleCollapse} sx={style.listHeader}>
                {props.isListOpen ? <ExpandLess sx={style.expendIcon} /> : <ExpandMore sx={style.expendIcon} />}
                <ListItemText primary={'Show ' + (props.profiles.length - showingCount) + ' ' + (props.isListOpen ? 'Less' : 'More')} />

            </ListItemButton>
        </List>
    );
}