import * as types from '../constants/EventsConstants';

export function upcomingEvents() {
  return dispatch => {
    return $.getJSON('/api/v1/user/events/created/').then(
      result => dispatch({type: types.LOAD_EVENTS, data: result})
    )
  };
}


export function getRelatedInterests(related_id) {
  return dispatch => {
    return $.getJSON(`/api/v1/user/related/${related_id}/`).then(
      result => dispatch({type: types.ADD_RELATED, data: result})
    )
  };
}