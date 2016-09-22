'use strict';
import _ from 'lodash';
import React from 'react';


const InterestSection = React.createClass({
  propTypes: {
    interests: React.PropTypes.array.isRequired,
  },

  render() {
    let interests;
    interests = this.props.interests.map((interest, i) => {
      if (interest.images.length > 0) {
        return (
          <div className="col-lg-3 col-sm-3 col-xs-6 text-center" key={i}>
            <span>{_.trunc(interest.name, {'length': 20, 'separator': ' '})}</span>
            <a href={interest.images[0].url} className="thumbnail text-center">
              <img src={interest.images[0].url} className="img-responsive interest-thumbnail"/>
            </a>
          </div>
        )
      }
    });

    return (
      <div className="panel panel-default">
        <div className="panel-heading">{this.props.type}</div>
        <div className="panel-body">
          {interests}
        </div>
      </div>
    );
  }
});


export default InterestSection;

