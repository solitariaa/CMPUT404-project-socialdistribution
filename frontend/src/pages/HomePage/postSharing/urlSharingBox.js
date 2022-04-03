import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import CheckIcon from '@mui/icons-material/Check';


export default function UrlSharingBox({post, alertSuccess}) {

 /* State Hook For Button type */
 const [active,setActive]=React.useState(false);
 const handleActive = () => {setActive(true)};
  return (
      
    <Box sx={{pl:3}}>
        <TextField
          disabled
          id="outlined-disabled"
          defaultValue={post.id}
          sx={{width: "75%"}}
        />
        <Button sx={{ml:1, mb: 2, width: "20%", height:55}} variant={"outlined"} startIcon={active? <CheckIcon/> :  <ContentCopyIcon />} onClick={() =>  {navigator.clipboard.writeText(post.id); handleActive();}}>
        Copy
      </Button>
    
    </Box>
  );
}