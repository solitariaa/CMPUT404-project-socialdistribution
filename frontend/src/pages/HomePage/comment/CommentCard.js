import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import FavoriteIcon from '@mui/icons-material/Favorite';
import IconButton from '@mui/material/IconButton';
import Button from '@mui/material/Button';
import { styled } from '@mui/material/styles';
import EditCommentDialog from './EditCommentDialog';
import EditIcon from '@mui/icons-material/Edit';
import { ReactMarkdown } from 'react-markdown/lib/react-markdown';
import DeleteCommentDialog from "./DeleteCommentDialog"
import Stack from '@mui/material/Stack';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import { Box } from '@mui/system';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { createCommentLikes, getCommentLikes, deleteCommentLikes } from '../../../Services/likes';
import { set } from 'lodash/fp';
import rehypeRaw from 'rehype-raw'

const PostImage = styled('img')({width: "100%"})

/* 
 * Takes the date formatted according to the ISO standard and returns the date formatted in the form "March 9, 2016 - 6:07 AM"
 */
function isoToHumanReadableDate(isoDate) {
  const date = new Date(isoDate);
  const dateFormat = new Intl.DateTimeFormat('en', { year: 'numeric', month: 'long', day: 'numeric' });
  const timeFormat = new Intl.DateTimeFormat('en', { hour: 'numeric', minute: 'numeric' });
  return dateFormat.format(date) + " - " + timeFormat.format(date);
}

export default function CommentCard({allLikes, profile, comment, alertSuccess, alertError, removeComment, editComments}) {
  /* Hook For Like icon color */
  const [color, setColor] = React.useState("grey");

  /* Hook For comment edit dialog */
  const [editOpen, setEditOpen] = React.useState(false);
  const handleEditClickOpen = () => setEditOpen(true);
  const handleEditClose = () => setEditOpen(false);

  /* Hook For comment delete dialog */
  const [deleteOpen, setDeleteOpen] = React.useState(false);
  const handleDelClickOpen = () => setDeleteOpen(true);
  const handleDelClose = () => setDeleteOpen(false);

  /* State Hook For Menu (edit/remove) */
  const [anchorEl, setAnchorEl] = React.useState(false);
  const closeAnchorEl = () => setAnchorEl(false);
  const openAnchorEl = () => setAnchorEl(true);

  // /* State Hook For likes */
  const [likes, setLikes] = React.useState(false);

  const handleColor = () => {
    const data = {
      type: "Like", 
      summary: profile.displayName + " likes your comment",
      context: "https://www.w3.org/ns/activitystreams",
      object: comment.id, 
      author_url: profile.id
    }
    if (color !== "grey"){
      deleteCommentLikes(comment, comment.id)
      .then( res => { 
        alertSuccess("Success: Deleted Like!");
        setColor("grey")
        setLikes(!likes)
      })
      .catch( err => {console.log(err)
        alertError("Error: Could Not Delete Like!");
      } );
    }else{
      createCommentLikes(comment, set("id")(profile.url)(profile))
      .then( res => { 
        alertSuccess("Success: Created New Like!");
        setColor("secondary")
        setLikes(!likes)
      })
      .catch( err => {console.log(err)
        alertError("Error: Could Not Create Like!");
      } );
    }
  }

  /* Hook handler For Menu (edit/remove) */
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  React.useEffect( () => {
    setColor(allLikes.map(x => x.object).includes(comment.id) ? "secondary" : "grey");
  }, [comment.id, allLikes] );

  return (
    <Card sx={{maxHeight: 200, mt:"1%"}}>
      <Grid container direction={'row'} spacing={12}>
        <Grid item xl={10} md={10}>
        <CardContent>
          <Stack direction="row" spacing={2}>
            <Typography gutterBottom variant="h6" component="div">
              {comment.author.displayName}
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{pt: 1}}>
              {isoToHumanReadableDate(comment.published)}
            </Typography>
          </Stack>
          {(comment.contentType === "text/plain")&&<Box sx={{width: "100%", px: 0}}>
            {comment.comment.split("\n").map((p, index) => <Typography key={index} paragraph> {p} </Typography>)}
          </Box>}
          {(comment.contentType === "text/markdown")&&<Box sx={{width: "100%", px: 0}}>
            <ReactMarkdown rehypePlugins={[rehypeRaw]} components={{img: PostImage}}>{comment.comment}</ReactMarkdown>
          </Box>}
        </CardContent>
        </Grid>
        <Grid item xl={1} md={1}>
        <Stack direction="row" spacing={1} sx={{pt:1}}>
          <IconButton aria-label="like" onClick={handleColor}>
            <FavoriteIcon color = {color}/>
          </IconButton>
          <IconButton aria-label="settings" onClick={handleClick}>
            <MoreVertIcon />
          </IconButton>
          </Stack>
        </Grid>
      </Grid>
      <Menu id="basic-menu" anchorEl={anchorEl} open={anchorEl} onClose={closeAnchorEl} MenuListProps={{ 'aria-labelledby': 'basic-button', }} >
          <MenuItem onClick={ () => { handleEditClickOpen(); closeAnchorEl(); } }>Edit</MenuItem>
          <MenuItem onClick={() => { handleDelClickOpen(); closeAnchorEl(); }}>Remove</MenuItem>
      </Menu>
      <EditCommentDialog open={editOpen} onClose={handleEditClose} comment={comment} alertSuccess={alertSuccess} alertError={alertError} editComments={editComments} />
      <DeleteCommentDialog comment={comment} alertSuccess={alertSuccess} alertError={alertError} open={deleteOpen} handleClose={handleDelClose} removeComment={removeComment} />
    </Card>
  );
}