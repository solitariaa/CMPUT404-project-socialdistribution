import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import Card from '@mui/material/Card';
import Paper from '@mui/material/Paper';
import CardMedia from '@mui/material/CardMedia';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';
import Collapse from '@mui/material/Collapse';



/*
 * Description: Detail view for each prize which allows user to purchase the prize
 */ 
export default function IMGPostDialog(props) {

  const [image, setImage] = React.useState(null)
  const [expanded, setExpanded] = React.useState(false);
  const handleExpandClick = () => {
      setExpanded(true);
    };
  const onImageChange = (event) => {
      if (event.target.files && event.target.files[0]) {
        handleExpandClick()
        setImage(URL.createObjectURL(event.target.files[0]));
      }
     }

  console.log("hanlde close: ", props.open)


return (

    
    <Dialog open={props.open} onClose={props.onClose} fullWidth maxWidth="md" sx={{borderRadius: "15px"}}>
        <DialogTitle>Creating Image Post</DialogTitle>
        <DialogContent>
          <Box >
          <Box component="form" noValidate>
            <Grid container>
            <Paper sx={{width: "100%", mt:2}}>
                <Box sx={{width: "100%", p:1}}>
                <TextField
                  id="outlined-multiline-flexible"
                  label="Post Title"
                  multiline
                  maxRows={4}
                  sx={{width: "100%"}}
                />
                  </Box>
              </Paper>
              <Paper sx={{width: "100%", mt:2}}>
                <Box sx={{width: "100%", p:1}}>
                <TextField
                  id="outlined-multiline-flexible"
                  label="Post Description"
                  multiline
                  maxRows={4}
                  sx={{width: "100%"}}
                />
                  </Box>
              </Paper>
              <Paper sx={{display: "grid", mt: 2, width: "100%"}}>
                    <Card fullWidth>
                        <Collapse in={expanded} timeout="auto" unmountOnExit>
                        <CardMedia
                            component="img"
                            height={image?image.clientHeight:0}
                            image={image}
                            alt="Preview"
                            sx={{borderRadius:2 }}
                        />
                        </Collapse>
                    </Card>

                    <Button variant="contained"
                        component="label"
                        sx={{marginTop: "5px"}}
                        fullWidth
                        > Upload Prize Image
                            <input id='image' onChange={onImageChange} type="file" label="fileUpload" name="image" hidden/>
                        </Button>
                        
                     </Paper>
              <Paper sx={{width: "100%", mt:2}}>
              <Box sx={{width: "100%", pt:2, pl:1}}>
                  <FormGroup>
                    <FormControlLabel control={<Switch/>} label="Private Post (Not select this switch button means your post will be public)" />
                    <FormControlLabel control={<Switch/>} label="Unlisted" />
                    <FormControlLabel control={<Switch/>} label="Markdown Content Type (Otherwise plain text)" />
                  </FormGroup>
                </Box>
              </Paper>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Post it now?
            </Button>
          </Box>
          </Box>
          </DialogContent>
      </Dialog>
    
  );
}