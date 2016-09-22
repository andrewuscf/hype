'use strict';
import React from 'react';


const InterestsModal = React.createClass({
  propTypes: {
    user: React.PropTypes.object.isRequired,
  },

  render() {
    const user = this.props.user;
    return (
      <div className="modal-content interest-modal">
        <div className="modal-header">
          <button type="button" className="close" data-dismiss="modal">&times;</button>
          <h4 className="modal-title">{user.username}</h4>
        </div>
        <div className="modal-body">
          <p>Some text in the modal.</p>
        </div>
        <div className="modal-footer">
          <button type="button" className="btn btn-default" data-dismiss="modal">Close</button>
        </div>
      </div>

    )
  }
});


export default InterestsModal;

