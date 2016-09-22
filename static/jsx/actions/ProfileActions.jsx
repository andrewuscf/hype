import * as types from '../constants/ProfileConstants';

export function loadUserProfile() {
  return dispatch => {
    return $.getJSON(`/api/v1/user/info/${PROFILE_USER}`).then(
      result => dispatch({type: types.LOAD_DATA, data: result})
    )
  };
}