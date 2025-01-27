import { createSlice } from '@reduxjs/toolkit'
import { concat } from 'lodash/fp'

export const friendsSlice = createSlice({
  name: 'friends',
  initialState: {
    items: [], 
  },
  reducers: {
    addFollower: (state, action) => {
      const data = {id: action.payload.id, displayName: action.payload.displayName, profileImage: action.payload.profileImage, url: action.payload.url}
      state.items = concat(state.items)(data).sort((a, b) => a.displayName - b.displayName);
    },
    setFollowers: (state, action) => {
      state.items = action.payload.map(x => { return {id: x.id, displayName: x.displayName, profileImage: x.profileImage, url: x.url} });
    },
    removeFollower: (state, action) => {
      state.items = state.items.filter(x => x.id !== action.payload.id);
    },
  },
})

export const { addFollower, setFollowers, removeFollower } = followerSlice.actions

export default followerSlice.reducer
