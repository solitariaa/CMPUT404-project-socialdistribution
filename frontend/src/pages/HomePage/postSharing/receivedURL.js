import * as React from 'react';
import PropTypes from 'prop-types';
import Button from '@mui/material/Button';
import { styled } from '@mui/material/styles';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import GetAppIcon from '@mui/icons-material/GetApp';
import { getUnlistedPost } from "../../../Services/posts";
import UnlistedFeed from "./unlistedFeed";
import Collapse from '@mui/material/Collapse';

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
  '& .MuiDialogContent-root': {
    padding: theme.spacing(2),
  },
  '& .MuiDialogActions-root': {
    padding: theme.spacing(1),
  },
}));

const BootstrapDialogTitle = (props) => {
  const { children, onClose, ...other } = props;

  return (
    <DialogTitle sx={{ m: 0, p: 2 }} {...other}>
      {children}
      {onClose ? (
        <IconButton
          aria-label="close"
          onClick={onClose}
          sx={{
            position: 'absolute',
            right: 8,
            top: 8,
            color: (theme) => theme.palette.grey[500],
          }}
        >
          <CloseIcon />
        </IconButton>
      ) : null}
    </DialogTitle>
  );
};

BootstrapDialogTitle.propTypes = {
  children: PropTypes.node,
  onClose: PropTypes.func.isRequired,
};





export default function ReceivedURLDialogs({open, onClose, alertSuccess, alertError}) {
    //state hook for URL
    const[id, setId] = React.useState("");
    //state hook for unlisted post
    const[unlistedPost, setUnlistedPost] = React.useState({});
    //state hook for expand view
    const [expanded, setExpanded] = React.useState(false);

    const clickClose = () => {
      setExpanded(false);
      onClose();
    }

    //Handler for get post from URL
    const handleGet = () => {
        getUnlistedPost(id)
        .then( res => { 
            console.log(res.data);
            setUnlistedPost(res.data)
            setExpanded(true);
            alertSuccess("Success: Retrieved Post!");
        })
        .catch( err => {console.log(err) 
            alertError("Error: Could Not Retrieved Post!");
        });
      };

  return (
    <div>
      <BootstrapDialog onClose={clickClose} aria-labelledby="customized-dialog-title" open={open} fullWidth >
        <BootstrapDialogTitle id="customized-dialog-title" onClose={clickClose}> Retrieved Unlisted Post </BootstrapDialogTitle>
        <DialogContent dividers>
        <TextField id="outlined-basic" label="Input the URL here" variant="outlined" sx={{width:"80%"}} onChange={(e) => {setId(e.target.value)}}/>
        <Button variant="contained" endIcon={<GetAppIcon />} sx={{height: 56, width:"20%"}} onClick={handleGet}> Get </Button>
        </DialogContent>
        <Collapse in={expanded} timeout="auto" unmountOnExit>
            <UnlistedFeed post={unlistedPost} />
        </Collapse>
      </BootstrapDialog>
    </div>
  );
}
