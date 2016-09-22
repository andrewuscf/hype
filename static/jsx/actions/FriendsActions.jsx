import * as types from '../constants/FriendsConstants';

export function getNearUsers() {
  return dispatch => {
    return $.getJSON('/api/v1/user/near/').then(
      result => dispatch({type: types.LOAD_USERS, data: result})
    )
  };
}