import * as React from 'react';
import { Modal, Typography, Box, Button, TextField, Stack, Container, Grid } from '@mui/material';
import { styled } from '@mui/material/styles';
import Badge from '@mui/material/Badge';
import Avatar from '@mui/material/Avatar';
import AddCircleSharpIcon from '@mui/icons-material/AddCircleSharp';
import { useSelector, useDispatch } from 'react-redux';
import { profileEdit } from '../../../redux/profileSlice';
import { editProfile, editGitHub } from '../../../Services/profile';
import Paper from '@mui/material/Paper';

const style = {
    textField: { minWidth: '100%' },
    box: {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        minWidth: '40rem',
        minHeight: '20vh',
        bgcolor: 'background.paper',
        boxShadow: 24,
        p: 4,
        borderRadius: 5, 
    },
    avatar: {
        width: 70,
        height: 70, 
        marginLeft: "10%", 
    },
    addIcon: {
        width: 30,
        height: 30,
        fill: 'green'
    },
    buttonContainer: {
        marginTop: '2rem',
        marginLeft: 'auto'
    }
};

const SmallAvatar = styled(Avatar)(({ theme }) => ({
    width: 30,
    height: 30,
    border: `2px solid ${theme.palette.background.paper}`,
}));


export default function ProfileEditModal(props) {
    const profile = useSelector(state => state.profile);
    const displayName = useSelector(state => state.profile.displayName);
    const userID = useSelector(state => state.profile.id);
    const profileImage = useSelector(state => state.profile.profileImage);
    const github = useSelector(state => state.profile.github);
    const dispatch = useDispatch();

    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        const imageChanged = (image !== null);

        if (imageChanged) {
            const imageData = data.get('img');
            const reader = new FileReader();
            reader.readAsDataURL(imageData)
            reader.onload = () => { 
                editProfile(profile, reader.result, data.get('github'))
                    .then( values => {
                        console.log(values[1].data) ;
                        dispatch(profileEdit(values[1].data));
                        window.location.reload(false);
                    })
                    .catch( err => console.log(err) );
            }
        } else {
            editGitHub(profile.url, data.get('github'))
                .then( res => {
                    console.log(res.data) ;
                    dispatch(profileEdit(res.data));
                })
                .catch( err => console.log(err) )
                .finally( props.onClose );
        }
    }

    const [image, _setImage] = React.useState(null);

    const onImageChange = (event) => {
        if (event.target.files && event.target.files[0]) {
            _setImage(URL.createObjectURL(event.target.files[0]));
        }
    };

    const cleanup = () => {
        _setImage(null);
    };

    const cancelChanges = () => {
        cleanup();
        props.onClose();
    }

    return (
        <Modal
            open={props.isOpen}
            onClose={cancelChanges}
            aria-labelledby="modal-profile-edit"
            aria-describedby="modal-profile-editing"
        >
            <Box sx={style.box} component="form" noValidate onSubmit={handleSubmit}>
                <Typography sx={{ fontWeight: 'bold', marginBottom: '2rem' }} id="modal-modal-title" variant="h4" component="h2">
                    Edit Profile
                </Typography>
                <Paper sx={{width:"100%", height:100, p:2}}>
                <Grid container spacing={0} justifyContent="center" direction='row' alignItems='center'>
                    
                    <Grid item xs={3} >

                        <Badge
                            component="label"
                            overlap="circular"
                            anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                            badgeContent={
                                <AddCircleSharpIcon sx={style.addIcon} />
                            }
                        >
                            <Avatar alt={displayName} src={image ? image : profileImage} sx={style.avatar} />
                            <input
                                accept='image/*'
                                hidden
                                type='file'
                                id='profile-image-upload'
                                name='img'
                                onChange={onImageChange}
                            />
                        </Badge></Grid>

                    <Grid item xs={9}>
                        <TextField
                            id='github'
                            name="github"
                            label="Github Link"
                            defaultValue={github}
                            sx={style.textField}
                        />
                    </Grid>
                </Grid >
                </Paper>

                <Stack spacing={1} sx={style.buttonContainer}>
                    <Button variant='contained' type='submit'>Save</Button>
                    <Button variant='outlined' onClick={cancelChanges}>Cancel</Button>
                </Stack>

            </Box >
        </Modal >
    )
}