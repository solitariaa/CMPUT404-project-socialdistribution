import * as React from 'react';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Collapse from '@mui/material/Collapse';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import { styled } from '@mui/material/styles';
import { ReactMarkdown } from 'react-markdown/lib/react-markdown';
import Box from '@mui/material/Box';

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

export default function UnlistedFeed({post}) {

  return (
    <Card sx={{m: "1px"}}>
    <CardHeader
      avatar={ 
        <AvatarContainer >
          <Avatar src={post.author.profileImage} sx={{ width: 64, height: 64,  }} aria-label="recipe" />
          <Typography variant="caption" display="block" gutterBottom sx={{paddingTop: "5px"}}>{post.author.displayName}</Typography>
        </AvatarContainer>
      }
      title={<Typography variant='h6'>{post.title}</Typography>}
      subheader={
        <span>
          <Typography variant='subheader'>{post.description}</Typography><br/>
          <Typography variant='subheader'>{isoToHumanReadableDate( post.published )}</Typography>
        </span> }
      disableTypography={true}
    />
    <CardContent>
      {(post.contentType === "text/plain")&&<Box sx={{width: "100%", px: "20px"}}>
        {post.content.split("\n").map((p, index) => <Typography key={index} paragraph> {p} </Typography>)}
      </Box>}
      {(post.contentType === "text/markdown")&&<Box sx={{width: "100%", px: "20px"}}>
        <ReactMarkdown components={{img: PostImage}}>{post.content}</ReactMarkdown>
      </Box>}
      {post.contentType.includes("image")&&<Box sx={{width: "100%", px: "20px"}}>
        <img src={post.content} width="100%" alt={post.title}/>
      </Box>}
    </CardContent>

</Card>
  );
}
