'use strict';
import { createStore, applyMiddleware, combineReducers } from 'redux';
import thunk from 'redux-thunk';
import FriendsEventsReducers from '../reducers/EventsReducers';

const createStoreWithMiddleware = applyMiddleware(
  thunk
)(createStore);

export default createStoreWithMiddleware(FriendsEventsReducers);
