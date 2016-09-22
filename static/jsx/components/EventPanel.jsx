'use strict';
import _ from 'lodash';
import React from 'react';
import moment from 'moment';

import UserHoverBox from './UserHoverBox';


const EventPanel = React.createClass({
  propTypes: {
    event: React.PropTypes.object.isRequired,
    getRelatedInterests: React.PropTypes.func.isRequired,
    similarInterests: React.PropTypes.array.isRequired
  },

  getInitialState(){
    return {
      open: false
    }
  },

  toggleBody() {
    this.setState({
      open: !this.state.open
    });
  },

  render() {
    const event = this.props.event;
    const attendees = [];
    for (var x = 0; x < 5 || x < 6; x++) {
      if (event.attendees[x] !== undefined) {
        attendees.push(
          <UserHoverBox 
            key={x} user={event.attendees[x]} getRelatedInterests={this.props.getRelatedInterests}
            similarInterests={this.props.similarInterests}/>
        )
      }
    }
    const isAttending = (USER == event.creator.username || _.findWhere(event.attendees, {'username': USER}))
      ? true : false;

    const tags = [];
    for (var x = 0; x < 5 || x < 6; x++) {
      if (event.tags[x] !== undefined) {
        tags.push(<span key={x} className="event-tag-box">{event.tags[x].name}</span>)
      }
    }


    return (
      <div className="panel panel-default">
        <div className="event-heading">
          <div className="media">
            <a href={'/user/'+ event.creator.username} className="pull-left">
              <img src={event.image?event.image: event.creator.avatar_url} className="event-main-photo"/>
            </a>

            <div className="media-body">
              <a href="#" className="pull-right text-muted">
                <i className="icon-reply-all-fill fa fa-2x "/>
              </a>
              <a href={'/event/'+ event.id} className="event-title">{_.startCase(event.title)} </a>
              <div className="gray-text pull-right">
                {(!isAttending) ?
                  <div className="join-event pull-left btn">
                    <i className="fa fa-sign-in" aria-hidden="true"/> Join
                  </div> :
                  null
                }
                <div className="pull-right">
                  {moment(event.dateTime).format('MMMM Do')}
                  <p>{moment(event.dateTime).format('h:mm a')}</p>
                </div>
              </div>
              <div className="event-tags-section">
                {
                  (event.tags.length > 0) ? tags : null
                }
              </div>
              {(attendees.length > 0) ?
                <a className="gray-text" onClick={this.toggleBody} href="javascript:;">
                  Attending {this.state.open ?
                  <i className="fa fa-caret-up"/> :
                  <i className="fa fa-caret-down"/>
                }
                </a> : null
              }
            </div>
          </div>

        </div>
        {(this.state.open) ?
          <div className="panel-body event-panel-body">
            <div className="event-attendees">
              {attendees}
            </div>
          </div> : null
        }
      </div>
    )
  }
});


export default EventPanel;

