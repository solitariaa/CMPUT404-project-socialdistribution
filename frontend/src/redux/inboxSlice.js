import { createSlice } from '@reduxjs/toolkit'
import { concat, findIndex, omit } from 'lodash/fp'

export const inboxSlice = createSlice({
  name: 'inbox',
  initialState: {
    items: [], 
  },
  reducers: {
    pushToInbox: (state, action) => {
      state.items = concat(state.items)(omit(["commentsSrc"])(action.payload)).sort((a, b) => Date.parse(b.published) - Date.parse(a.published));
    },
    setInbox: (state, action) => {
      state.items = action.payload.map(omit(["commentsSrc"]));
    },
    removeFromInbox: (state, action) => {
      state.items = state.items.filter( x => x.id !== action.payload.id);
    }, 
    updateInboxItem: (state, action) => {
      const index = findIndex(x => x.id === action.payload.id)(state.items);
      state.items = state.items.map((x, i) => i === index ? action.payload : x);
    }, 
  },
})

export const { pushToInbox, setInbox, removeFromInbox, updateInboxItem } = inboxSlice.actions

export default inboxSlice.reducer
