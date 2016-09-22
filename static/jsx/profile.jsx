'use strict';
import {bindActionCreators} from 'redux';
import * as ProfileActions from './actions/ProfileActions';
import {Provider, connect} from 'react-redux';
import React from 'react';
import ReactDOM from 'react-dom';

import ProfileStore from './stores/ProfileStore';

import ConnectedAccounts from './components/ConnectedAccounts';
import InterestSection from './components/InterestSection';
import LoadingView from './components/LoadingView';
import UserProfilePhoto from './components/UserProfilePhoto';


// Redux Store Setup
function mapStateToProps(state) {
  return state;
}
function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(ProfileActions, dispatch)
  }
}

//const CSRF_TOKEN = $.cookie('csrftoken');


let ProfilePanelView = React.createClass({
  componentDidMount() {
    this.props.actions.loadUserProfile();
  },

  render() {
    if (!this.props.user) {
      return (<div><LoadingView /></div>)
    } else {
      const user = this.props.user;
      console.log(user);
      return (
        <div>
          <div className="col-sm-3">
            <a href="/users" className="pull-left profile-avatar">
              <UserProfilePhoto avatar_url={user.profile.avatar_url}/>
            </a>
          </div>
          <div className="col-sm-6">
            <span className="profile-first-last">
              {user.first_name} { user.last_name }
            </span>
              {(user.is_active) ?
                <i className="fa fa-check-square"/> :
                <i className="fa fa-exclamation-circle"/>
              }
            <span className="row">AKA ({ user.username })</span>
            <ConnectedAccounts accounts={user.connected} username={user.username} />
            {(CURRENT_USER != user.username) ?
              <a href="/">
                <button type="button" className="btn btn-success">Send me a message</button>
              </a> :
              null
            }
            <br />
          </div>
          <br />

          <div className="col-sm-12">
            <div className="panel panel-default">
              <div className="panel-body">
                { user.profile.bio }
                {(CURRENT_USER != user.username) ?
                  <a href="{% url 'settings' %}" className="pull-right">Change</a> :
                  null
                }
              </div>
            </div>
          </div>

          <div className="col-sm-12">
            <ul className="list-group">
              <li className="list-group-item text-right"><span className="pull-left"><strong className="">Events
                Attended</strong></span> 0
              </li>
              <li className="list-group-item text-right">
          <span className="pull-left">
            <strong className="">Hype</strong>
          </span> 10
              </li>
              <li className="list-group-item text-right">
          <span className="pull-left">
            <strong>Posts</strong>
          </span> 12
              </li>
            </ul>
          </div>

          <div className="col-sm-12">
            <InterestSection interests={user.interests}/>
          </div>
        </div>
      )
    }
  }
});

ProfilePanelView = connect(
  mapStateToProps,
  mapDispatchToProps
)(ProfilePanelView);


ReactDOM.render(
  <Provider store={ProfileStore}>
    <ProfilePanelView />
  </Provider>
  ,
  document.getElementById('profile-jsx'));

