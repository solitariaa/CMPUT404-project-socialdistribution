import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import FavoriteIcon from '@mui/icons-material/Favorite';
import IconButton from '@mui/material/IconButton';
import Button from '@mui/material/Button';
import EditCommentDialog from './EditCommentDialog';

export default function CommentCard(props) {
  /* Hook For Like icon color */
  const [color, setColor] = React.useState("grey");
  /* Hook For comment edit dialog */
  const [open, setOpen] = React.useState(false);

  const handleColor = (event) =>{
    setColor("secondary")
  }

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };
  

  return (
    <Card fullwidth sx={{maxHeight: 200, mt:"1%"}}>
      <Grid container direction={'row'} spacing={5}>
        <Grid item xl={11} md={11} sm={10} xs={10}>
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            {props.commentData.comment}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {props.commentData.published}
          </Typography>
        </CardContent>
        </Grid>
        <Grid item xl={1} md={1} sm={2} xs={2}>
          <IconButton aria-label="like">
            <FavoriteIcon color = {color} onClick={handleColor}/>
          </IconButton>
          <Button variant="outlined" onClick={handleClickOpen}>
            Open form dialog
          </Button>
        </Grid>
      </Grid>
      <EditCommentDialog open={open} handleClose={handleClose}></EditCommentDialog>
    </Card>
  );
}