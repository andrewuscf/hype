'use strict';
import React from 'react';


const UserProfilePhoto = React.createClass({
  propTypes: {
    avatar_url: React.PropTypes.string.isRequired
  },

  render() {
    return (
      <img className="img-responsive user-photo" src={this.props.avatar_url}/>
    );
  }
});

export default UserProfilePhoto;

