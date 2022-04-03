import { createSlice } from '@reduxjs/toolkit'
import { concat } from 'lodash/fp'

export const likedSlice = createSlice({
  name: 'liked',
  initialState: {
    items: [], 
  },
  reducers: {
    addLiked: (state, action) => {
      state.items = concat(state.items)(action.payload.id);
    },
    setLiked: (state, action) => {
      state.items = action.payload.map( x => x.object );
    },
  },
})

export const { addLiked, setLiked } = likedSlice.actions

export default likedSlice.reducer
