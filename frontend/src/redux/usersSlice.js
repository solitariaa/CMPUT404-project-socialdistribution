import { createSlice } from '@reduxjs/toolkit'

export const usersSlice = createSlice({
  name: 'users',
  initialState: {
    items: [], 
  },
  reducers: {
    setUsers: (state, action) => {
      state.items = action.payload.map(x => { return {id: x.id, displayName: x.displayName, profileImage: x.profileImage, url: x.url} });
    },
  },
})

export const { setUsers } = usersSlice.actions

export default usersSlice.reducer
