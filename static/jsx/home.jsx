'use strict';
import {bindActionCreators} from 'redux';
import * as EventsActions from './actions/EventsActions';
import {Provider, connect} from 'react-redux';
import React from 'react';
import ReactDOM from 'react-dom';

import EventsStore from './stores/EventsStore';

import EventPanel from './components/EventPanel';


// Redux Store Setup
function mapStateToProps(state) {
  return state;
}
function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(EventsActions, dispatch)
  }
}

//const CSRF_TOKEN = $.cookie('csrftoken');


let HomeView = React.createClass({
  componentDidMount() {
    this.props.actions.upcomingEvents();
  },

  render() {
    if (this.props.myEvents) {
      if (this.props.myEvents.length > 0) {
        const events = this.props.myEvents.map((event, i) => {
          return (
            <EventPanel 
              event={event} key={i} 
              getRelatedInterests={this.props.actions.getRelatedInterests}
              similarInterests={this.props.similarInterests}/>
          )
        });
        return (
          <div>
            <div className="col-xs-12">
              {events}
            </div>
          </div>
        )
      } else {
        return (
          <div className="no-events">
            You have not events!
          </div>
        )
      }
    } else {
      return (<div>LOADING...</div>)
    }
  }
});

HomeView = connect(
  mapStateToProps,
  mapDispatchToProps
)(HomeView);


ReactDOM.render(
  <Provider store={EventsStore}>
    <HomeView />
  </Provider>,
  document.getElementById('home-jsx'));