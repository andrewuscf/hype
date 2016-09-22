'use strict';
import {bindActionCreators} from 'redux';
import * as FriendsActions from './actions/FriendsActions';
import {Provider, connect} from 'react-redux';
import React from 'react';
import ReactDOM from 'react-dom';

import FriendsStore from './stores/FriendsStore';


// Redux Store Setup
function mapStateToProps(state) {
  return state;
}
function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(FriendsActions, dispatch)
  }
}


let FriendsView = React.createClass({

  getInitialState() {
    return {
      myLocation: null,
      nearUsers: null,
    }
  },

  componentDidMount() {
    this.props.actions.getNearUsers();
  },


  render() {
    if (this.props.nearUsers) {
      return (
        <div>
          <div className="col-sm-6">
          </div>
        </div>
      )
    } else {
      return (<div>LOADING...</div>)
    }
  }
});

FriendsView = connect(
  mapStateToProps,
  mapDispatchToProps
)(FriendsView);


ReactDOM.render(
  <Provider store={FriendsStore}>
    <FriendsView />
  </Provider>,
  document.getElementById('find-friends-jsx'));