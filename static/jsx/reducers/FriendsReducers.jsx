import * as constants from '../constants/FriendsConstants';

const initialState = {
  nearUsers: null
};

export default function FriendsReducers(state = initialState, action) {
  switch (action.type) {
    case constants.LOAD_USERS:
      return {
        nearUsers: action.data
      };


    default:
      return state
  }
}
