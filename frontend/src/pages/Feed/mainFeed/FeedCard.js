import * as React from 'react';
import { styled } from '@mui/material/styles';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardMedia from '@mui/material/CardMedia';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Collapse from '@mui/material/Collapse';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import { red } from '@mui/material/colors';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ShareIcon from '@mui/icons-material/Share';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import CommentIcon from '@mui/icons-material/Comment';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import CommentCard from '../comment/CommentCard';

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

export default function FeedCard(props) {
  const [image, setImage] = React.useState("")
  const [expanded, setExpanded] = React.useState(false);
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [color, setColor] = React.useState("grey");
  const [show, setShow] = React.useState(false);
  const open = Boolean(anchorEl);
  // if (props.feedData.ImgUrl !== "") {
  //   setImage(props.feedData.ImgUrl)
  // }
  
  
  const handleColor = (event) =>{
    setColor("secondary")
  }
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  React.useEffect(()=>{
      if (props.feedData !== undefined){
          setImage(props.feedData ? props.feedData.ImgUrl : undefined)
      }
      if(image !== undefined && image !== ""){
        setShow(true)
      }
  }, [props.feedData, image])

  // console.log(props.feedData[0].author.displayName.charAt(0))
  console.log("waht is :", image)
  return (
    <Card sx={{m: "1px"}}>
      <CardHeader
        avatar={
          <Avatar sx={{ bgcolor: red[500] }} aria-label="recipe"> {props.feedData.author.displayName.charAt(0)} </Avatar>
        }
        action={
          <IconButton aria-label="settings" onClick={handleClick}>
            <MoreVertIcon id="setting-button" aria-controls={open ? 'setting-menu' : undefined} aria-haspopup="true" aria-expanded={open ? 'true' : undefined} />
          </IconButton>
        }
        title={props.feedData.title}
        subheader={props.feedData.published}
      />
      <Menu
        id="setting-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'setting-button',
        }}
      >
        <MenuItem onClick={handleClose}>Edit</MenuItem>
        {/* <MenuItem onClick={handleClose}>Options</MenuItem> */}
      </Menu>
      <CardContent>
        <Paper sx={{width: "100%", mt:1}}>
          <Box sx={{width: "100%", p:1}}>
            <Typography variant="body2" color="text.secondary">
              {props.feedData.description}
            </Typography>
          </Box>
        </Paper>
        <Paper sx={{width: "100%", mt:2}}>
            <Box sx={{width: "100%", p:1}}>
              <Typography paragraph>
                {props.feedData.content}
              </Typography>
          </Box>
        </Paper>
      </CardContent>
      {/* <button onClick={() => setShow(prev => !prev)}>Click</button> */}
      {show && <Box>
        <CardMedia
        component="img"
        image={image}
        alt="Feed Image"
      />
        </Box>}
      
      <CardActions disableSpacing>
        <IconButton aria-label="like">
          <FavoriteIcon color = {color} onClick={handleColor}/>
        </IconButton>
        <IconButton aria-label="share">
          <ShareIcon />
        </IconButton>
        <IconButton aria-label="comment">
          <CommentIcon />
        </IconButton>
        <ExpandMore
          expand={expanded}
          onClick={handleExpandClick}
          aria-expanded={expanded}
          aria-label="show more"
        >
          <ExpandMoreIcon />
        </ExpandMore>
      </CardActions>
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>
          <CommentCard>

          </CommentCard>
        </CardContent>
      </Collapse>
    </Card>
  );
}