import * as constants from '../constants/ProfileConstants';

const initialState = {
  user: null
};

export default function FavoriteReducers(state = initialState, action) {
  switch (action.type) {
    case constants.LOAD_DATA:
      return {
        user: action.data
      };


    default:
      return state
  }
}
