import * as constants from '../constants/EventsConstants';

const initialState = {
  myEvents: null,
  similarInterests: []
};

export default function FriendsEventsReducers(state = initialState, action) {
  switch (action.type) {
    case constants.LOAD_EVENTS:
      return {
        similarInterests: state.similarInterests,
        myEvents: action.data
      };
    
    case constants.ADD_RELATED:
      return {
        myEvents: state.myEvents,
        similarInterests: state.similarInterests.concat(action.data)
      };


    default:
      return state
  }
}
