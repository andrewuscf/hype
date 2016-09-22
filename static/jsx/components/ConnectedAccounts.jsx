'use strict';
import React from 'react';


const ConnectedAccounts = React.createClass({
  propTypes: {
    accounts: React.PropTypes.object.isRequired,
    username: React.PropTypes.string.isRequired
  },

  getConnnections() {
    const accounts = this.props.accounts;
    return (
      <div>
        {accounts.facebook ?
          <i className="fa fa-facebook fa-2x hgreen social-account-icon"/> :
          <i className="fa fa-facebook fa-2x social-account-icon"/>
        }
        {accounts.spotify ?
          <i className="fa fa-spotify fa-2x hgreen social-account-icon"/> :
          <i className="fa fa-spotify fa-2x social-account-icon"/>
        }
        {accounts.instagram ?
          <i className="fa fa-instagram fa-2x hgreen social-account-icon"/> :
          <i className="fa fa-instagram fa-2x social-account-icon"/>
        }
        {accounts.google ?
          <i className="fa fa-google-plus fa-2x hgreen social-account-icon"/> :
          <i className="fa fa-google-plus fa-2x social-account-icon"/>
        }
      </div>
    )
  },

  render() {

    return (
      <div className="row">
        {(CURRENT_USER == this.props.username) ?
          <a href="/accounts/social/connections/">
            {this.getConnnections()}
          </a>
          : this.getConnnections()
        }
      </div>
    );
  }
});

export default ConnectedAccounts;

