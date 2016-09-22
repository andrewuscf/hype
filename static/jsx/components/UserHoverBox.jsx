'use strict';
import React from 'react';

import InterestsModal from './InterestsModal';


const UserHoverBox = React.createClass({
  propTypes: {
    user: React.PropTypes.object.isRequired,
    getRelatedInterests: React.PropTypes.func.isRequired,
    similarInterests: React.PropTypes.array.isRequired
  },

  getInitialState() {
    return {
      isOpen: false
    }
  },

  onMouseOver() {
    if (!_.findWhere(this.props.similarInterests, {'username': this.props.user.username})) {
      this.props.getRelatedInterests(this.props.user.id);
      console.log('hit');
    }
    this.setState({
      isOpen: true
    })
  },

  onMouseLeave() {
    this.setState({
      isOpen: false
    })
  },

  render() {
    const user = this.props.user;
    const similarUser = _.findWhere(this.props.similarInterests, {'username': user.username});
    console.log(similarUser)
    return (
      <div>
        {(similarUser && this.state.isOpen) ? <InterestsModal user={similarUser} />: null}
        <a href={'/user/' + user.username}
           onClick={this.onMouseOver} onTouchStart={this.onMouseOver}>
          <img src={user.avatar_url} width="80"/>
        </a>
      </div>
    )
  }
});


export default UserHoverBox;

