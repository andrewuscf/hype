'use strict';
import { bindActionCreators } from 'redux';
import * as FriendsEventsActions from './actions/EventsActions';
import { Provider, connect } from 'react-redux';
import React from 'react';

import EventNav from './components/EventNav';

import EventPanel from './components/EventPanel';



// Redux Store Setup
function mapStateToProps(state) {
  return state;
}
function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(FriendsEventsActions, dispatch)
  }
}


let HomeView = React.createClass({
  componentDidMount() {
    this.props.actions.upcomingEvents();
  },

  render() {
    if (this.props.myEvents) {
      console.log(this.props.myEvents);
      const events = this.props.myEvents.map((event, i) => {
        return (<EventPanel event={event} key={i}/>)
      });
      return (
        <div>
          <EventNav />
          <div className="col-sm-6">
            My Events:
            {events}
          </div>
        </div>
      )
    } else {
      return (<div>LOADING...</div>)
    }
  }
});

export default HomeView = connect(
  mapStateToProps,
  mapDispatchToProps
)(HomeView);
