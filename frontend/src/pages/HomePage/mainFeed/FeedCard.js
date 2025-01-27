import * as React from 'react';
import { styled } from '@mui/material/styles';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Collapse from '@mui/material/Collapse';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ShareIcon from '@mui/icons-material/Share';
import Box from '@mui/material/Box';
import CommentIcon from '@mui/icons-material/Comment';
import Grid from '@mui/material/Grid';
import CommentCard from '../comment/CommentCard';
import { getComments } from '../../../Services/comments';
import EditPostDialog from './EditPostDialog';
import DeletePostDialog from './DeletePostDialog';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import EditIMGDialog from "./EditIMGDialog"
import AddCommentsDialog from "../comment/addCommentDialog"
import Button from '@mui/material/Button';
import { ReactMarkdown } from 'react-markdown/lib/react-markdown';
import { concat } from 'lodash/fp';
import { createPostLikes, saveLiked} from '../../../Services/likes';
import FollowRequestDialog from '../../../Components/FollowRequestDialog';
import { getAuthorFromStorage } from '../../../LocalStorage/profile';
import { set } from 'lodash/fp';
import SharingDialog from "../postSharing/sharingDialog";
import SharingUnlistedDialog from "../postSharing/sharingUnlistedDialog";
import rehypeRaw from 'rehype-raw'
import { Chip } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { addLiked } from '../../../redux/likedSlice';
import { updateInboxItem } from '../../../redux/inboxSlice';
import { update } from 'lodash/fp';

const AvatarContainer = styled('div')({display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", width: "125px"});

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

const ExpandMore = styled((props) => {
  const { expand, ...other } = props;
  return <IconButton {...other} />;
})(({ theme, expand }) => ({
  transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
  marginLeft: 'auto',
  transition: theme.transitions.create('transform', {
    duration: theme.transitions.duration.shortest,
  }),
}));

function CardButtons({isOwner, handleColor, expanded, handleExpandClick, handleLikes, color, handleSharingDialogClickOpen, handleSharingUnlistedOpen, post}) {
  return (
      <CardActions disableSpacing>
          <IconButton aria-label="like" onClick={handleLikes} >
            <FavoriteIcon color={color} />
          </IconButton>
          <IconButton aria-label="share" onClick={post.unlisted !== true ? handleSharingDialogClickOpen:handleSharingUnlistedOpen}>
            <ShareIcon />
          </IconButton>
          <div sx={{pr:8}}>
            <ExpandMore expand={expanded} onClick={handleExpandClick} aria-expanded={expanded} aria-label="show more" >
              <CommentIcon/>
            </ExpandMore>
          </div>
          <span style={{marginLeft: "auto", marginRight: "10px"}}>
          <Chip variant="outlined" key={-1} label={"Likes: " + post.likeCount} color="primary" sx={{margin: "5px 10px 0 0", padding: "2px", fontSize: "0.8rem"}} ></Chip>
          {post.categories.map( (category, index) => ( <Chip key={index} variant='outlined' label={"Category: " + category} sx={{margin: "5px 10px 0 0", padding: "2px", fontSize: "0.8rem"}} ></Chip>))}
          </span>
      </CardActions>
  )
}


export default function FeedCard({post, alertError, alertSuccess, updateFeed, removeFromFeed}) {
  const dispatch = useDispatch();

  /* State Hook For Expanding The Comments */
  const [expanded, setExpanded] = React.useState(false);
 
  /* State Hook For Colour Scheme */
  const [color, setColor] = React.useState("grey");

  /* State Hook For Likes */
  const allLikes = useSelector( state => state.liked.items );

  /* State Hook For Current User */
  const profile = useSelector( state => state.profile );

  /* Boolean Indicating Whether Or Not The Post Is Owned By The Current User */
  const isOwner = post.author.id === profile.url

  // /* State Hook For likes */
  const handleLikes = () => {
    if (! allLikes.includes(post.id)) {
      createPostLikes(post, set("id")(profile.url)(profile))
        .then( _ => {
          const data = {
              "summary": `${profile.displayName} Likes Your Post!`,         
              "type": "Like",
              "author": set("id")(profile.url)(profile),    
              "object": post.id
          };
          return saveLiked(profile, data);
        } )
        .then( _ => { 
          dispatch(updateInboxItem( update("likeCount")(x => x + 1)(post) ));
          dispatch( addLiked(post) );
          alertSuccess("Success: Created New Like!");
          setColor("secondary");
        })
        .catch( err => {console.log(err)
          alertError("Error: Could Not Create Like!");
        });
    }
  }

  /* State Hook For Opening Edit Post Dialog */
  const [editOpen, setEditOpen] = React.useState(false);
  const closeEditDialog = () => setEditOpen(false);
  const openEditDialog = () => {
    setAnchorEl(undefined);
    setMenuOpen(false);
    setEditOpen(true);
  }

  /* State Hook For Opening Edit IMG Post Dialog */
  const [editIMGOpen, setEditIMGOpen] = React.useState(false);
  const closeEditIMGDialog = () => setEditIMGOpen(false);
  const openEditIMGDialog = () => setEditIMGOpen(true);

  /* State Hook For Opening Delete Post Dialog */
  const [deleteOpen, setDeleteOpen] = React.useState(false);
  const closeDeleteDialog = () => setDeleteOpen(false);
  const openDeleteDialog = () => {
    setAnchorEl(undefined);
    setMenuOpen(false);
    setDeleteOpen(true);
  };

  /* State Hook For Opening Follow Request Dialog */
  const [followOpen, setFollowOpen] = React.useState(false);
  const closeFollowDialog = () => setFollowOpen(false);
  const openFollowDialog = () => setFollowOpen(post.author.id !== getAuthorFromStorage().id);

  /* State Hook For Comments */
  const [comments, setComments] = React.useState([]);
  const removeComment = comment => setComments(comments.filter(x => x.id !== comment.id));
  const editComment = comment => setComments(comments.map(x => x.id === comment.id ? comment : x))
  const likeComment = commentID => setComments( comments.map( comment => comment.id === commentID ? update("likeCount")(x => x + 1)(comment) : comment ) );

  /* State Hook For Menu (edit/remove) */
  const [anchorEl, setAnchorEl] = React.useState(undefined);
  const [menuOpen, setMenuOpen] = React.useState(false);

  /* State Hook For Adding comment*/
  const [addCMOpen, setaddCMOpen] = React.useState(false);

  /* State Hook For Opening of Share post dialog*/
  const [openSharingDialog, setSharingDialogOpen] = React.useState(false);

  /* State Hook For Opening of Share unlisted post dialog*/
  const [openSharUnlistedDialog, setSharUnlistedDialogOpen] = React.useState(false);

  /* Hook handler For Menu (edit/remove) */
  const handleClick = event => { 
    setAnchorEl(event.currentTarget);
    setMenuOpen(true);
  }
  const handleClose = () => { 
    setMenuOpen(false);
    setAnchorEl(null);
  }

  /* Hook handler For Share post dialog (open/close) */
  const handleSharingDialogClickOpen = () => {
    setSharingDialogOpen(true);
  };

  const handleSharingDialogClose = () => {
    setSharingDialogOpen(false);
  };

  /* Hook handler For Share post dialog (open/close) */
  const handleSharingUnlistedOpen = () => {
    setSharUnlistedDialogOpen(true);
  };

  const handleSharingUnlistedDialogClose = () => {
    setSharUnlistedDialogOpen(false);
  };
  
  const handleColor = (event) =>setColor("secondary");

  const handleAddCMClickOpen = () => setaddCMOpen(true);

  const handleAddCMClose = () => setaddCMOpen(false);


  /* This Runs When The Button To Show Comments Is Clicked */
  const handleExpandClick = () => {
    getComments(post)
      .then( res => { 
        console.log(res.data);
        console.log(res.headers)
        setComments(res.data.comments ? res.data.comments : []);
        setExpanded(!expanded);
      })
      .catch( err => console.log(err) );
  };
  
  /* This Runs When The alllikes and post.id has changed */
  React.useEffect( () => {
    setColor(allLikes.includes(post.id) ? "secondary" : "grey");
  }, [post.id, allLikes] );

  return (
    <Card sx={{m: "1px"}}>
      <CardHeader
        avatar={ 
          <AvatarContainer onClick={() => openFollowDialog() } >
            <Avatar src={post.author.profileImage} sx={{ width: 64, height: 64,  }} aria-label="recipe" />
            <Typography variant="caption" display="block" gutterBottom sx={{paddingTop: "5px"}}>{post.author.displayName}</Typography>
          </AvatarContainer>
        }
        title={ <Typography variant='h6'>{post.title}</Typography> }
        action={
          <IconButton aria-label="settings" onClick={handleClick}>
            {isOwner ? 
            <MoreVertIcon />
            : <></>} 
          </IconButton>
        }
        subheader={
          <span>
            <Typography variant='subheader'>{post.description}</Typography><br/>
            <Typography variant='subheader'>{isoToHumanReadableDate( post.published )}</Typography><br/>
          </span> 
          }
        disableTypography={true}
      />
      <CardContent>
        {(post.contentType === "text/plain")&&<Box sx={{width: "100%", px: "20px"}}>
          {post.content.split("\n").map((p, index) => <Typography key={index} paragraph> {p} </Typography>)}
        </Box>}
        {(post.contentType === "text/markdown")&&<Box sx={{width: "100%", px: "20px"}}>
          <ReactMarkdown rehypePlugins={[rehypeRaw]}  components={{img: PostImage}}>{post.content}</ReactMarkdown>
        </Box>}
        {post.contentType.includes("image")&&<Box sx={{width: "100%", px: "20px"}}>
          <img src={post.content} width="100%" alt={post.title}/>
        </Box>}
      </CardContent>
      <CardButtons isOwner={isOwner} handleColor={handleColor} expanded={expanded} handleExpandClick={handleExpandClick} handleLikes = {handleLikes} color={color} handleSharingDialogClickOpen={handleSharingDialogClickOpen} handleSharingUnlistedOpen={handleSharingUnlistedOpen} post={post}/>
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>
          {comments.map((comment, index) => ( 
          <Grid key={index} item xs={12}> 
            <CommentCard post={post} allLikes={allLikes} profile={profile} isOwner={profile.url === comment.author.id && profile.host === post.author.host} removeComment={removeComment} editComments={editComment} likeComment={likeComment} comment={comment} alertSuccess={alertSuccess} alertError={alertError} fullWidth="true" /> 
          </Grid>))}
          <Grid item xs={12} sx={{marginTop: "8px"}}>
            <Card fullwidth="true" sx={{maxHeight: 200, mt:"1%"}}>
            <Button disableElevation={false} sx={{minHeight: "100px", fontSize: "1.15rem"}}  onClick={handleAddCMClickOpen} fullWidth>Add Comment</Button>
            </Card>
          </Grid>
        </CardContent>
      </Collapse>
        <Menu id="basic-menu" anchorEl={anchorEl} open={menuOpen} onClose={handleClose} >
          {((post.contentType === "text/markdown") || (post.contentType === "text/plain"))&&<MenuItem onClick={openEditDialog}>Edit</MenuItem>}
          {post.contentType.includes("image")&&<MenuItem onClick={openEditIMGDialog}>Edit</MenuItem>}
          <MenuItem onClick={openDeleteDialog}>Remove Post</MenuItem>
        </Menu>
      <DeletePostDialog post={post} alertSuccess={alertSuccess} alertError={alertError} open={deleteOpen} handleClose={closeDeleteDialog} removeFromFeed={removeFromFeed} />
      <EditPostDialog post={post} open={editOpen} onClose={closeEditDialog} alertError={alertError} alertSuccess={alertSuccess} updateFeed={updateFeed} />
      <EditIMGDialog post={post} open={editIMGOpen} onClose={closeEditIMGDialog} alertError={alertError} alertSuccess={alertSuccess} updateFeed={updateFeed} />
      <AddCommentsDialog open={addCMOpen} handleAddCMClose={handleAddCMClose} post={post} setComments={setComments} alertSuccess={alertSuccess} alertError={alertError}></AddCommentsDialog>
      <FollowRequestDialog  authorToFollow={post.author} onClose={closeFollowDialog} alertSuccess={alertSuccess} alertError={alertError} open={followOpen} handleClose={closeFollowDialog} />
      <SharingDialog open ={openSharingDialog} onClose={handleSharingDialogClose} post={post} alertSuccess={alertSuccess} alertError={alertError}></SharingDialog>
      <SharingUnlistedDialog open ={openSharUnlistedDialog} onClose={handleSharingUnlistedDialogClose} post={post} alertSuccess={alertSuccess} alertError={alertError}></SharingUnlistedDialog>
    </Card>
  );
}